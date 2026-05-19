#!/usr/bin/env python3
"""Botpress ↔ OpenClaw Adapter V1. Safety gate, intent routing, logging."""

import json, time, os, logging
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any

# ─── CONFIG (no secrets) ───
OPENCLAW_GATEWAY_URL = os.getenv("OPENCLAW_GATEWAY_URL", "http://localhost:8765")
OPENCLAW_TIMEOUT_MS = int(os.getenv("OPENCLAW_TIMEOUT_MS", "30000"))
RATE_LIMIT_MAX_PER_MIN = int(os.getenv("ADAPTER_RATE_LIMIT", "10"))
CIRCUIT_BREAKER_THRESHOLD = int(os.getenv("CIRCUIT_BREAKER_THRESHOLD", "3"))
CIRCUIT_BREAKER_WINDOW_S = int(os.getenv("CIRCUIT_BREAKER_WINDOW_S", "60"))
LOG_DIR = Path(os.getenv("ADAPTER_LOG_DIR", str(Path(__file__).parent / "logs")))

# ─── LOGGING ───
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "adapter.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("adapter")

# ─── SAFETY GATE ───
WHITELIST_INTENTS = {"screener", "analysis", "journal", "status", "help"}
BLOCKED_INTENTS = {"execute_trade", "git_push", "modify_production", "expose_secret"}
CONFIRM_INTENTS = {"backtest_run", "multi_scan"}

class SafetyGate:
    def __init__(self):
        self.blocked_count = 0

    def check(self, intent: str, params: Optional[Dict] = None) -> dict:
        if intent in BLOCKED_INTENTS:
            self.blocked_count += 1
            return {"allowed": False, "reason": f"Intent '{intent}' blocked: trading reel/modification non autorise V1"}

        if intent in WHITELIST_INTENTS:
            return {"allowed": True, "reason": "Whitelist intent"}

        if intent in CONFIRM_INTENTS:
            symbol_count = (params or {}).get("max_symbols", 0) or (params or {}).get("limit", 0)
            if symbol_count > 5:
                return {"allowed": False, "reason": f"Confirmation requise: >5 symbols ({symbol_count})", "needs_confirmation": True}
            return {"allowed": True, "reason": "Confirmed intent"}

        return {"allowed": False, "reason": f"Intent inconnu: '{intent}'. /help pour la liste."}


# ─── INTENT ROUTING ───
INTENT_TO_ACTION = {
    "screener": "market_scan",
    "analysis": "analyze_symbol",
    "journal": "query_journal",
    "status": "cockpit_status",
    "help": "static_help",
    "backtest_run": "run_backtest",
}

# ─── RATE LIMITER ───
class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = {}

    def check(self, user_id: str) -> bool:
        now = time.time()
        if user_id not in self.requests:
            self.requests[user_id] = []
        self.requests[user_id] = [t for t in self.requests[user_id] if now - t < 60]
        if len(self.requests[user_id]) >= RATE_LIMIT_MAX_PER_MIN:
            return False
        self.requests[user_id].append(now)
        return True


# ─── CIRCUIT BREAKER ───
class CircuitBreaker:
    def __init__(self):
        self.failures: list = []
        self.open = False

    def record_failure(self):
        now = time.time()
        self.failures.append(now)
        self.failures = [t for t in self.failures if now - t < CIRCUIT_BREAKER_WINDOW_S]
        if len(self.failures) >= CIRCUIT_BREAKER_THRESHOLD:
            self.open = True

    def record_success(self):
        self.open = False

    def is_open(self) -> bool:
        if self.open and time.time() - max(self.failures) > CIRCUIT_BREAKER_WINDOW_S:
            self.open = False
        return self.open


# ─── ADAPTER ───
@dataclass
class AdapterResponse:
    botpress_event_id: str
    status: str  # ok|error|timeout|blocked
    reply_text: str
    reply_data: dict = field(default_factory=dict)
    safety_check: str = "passed"
    trace_id: str = ""
    duration_ms: int = 0


class BotpressOpenClawAdapter:
    def __init__(self):
        self.safety = SafetyGate()
        self.rate_limiter = RateLimiter()
        self.circuit = CircuitBreaker()
        self.logs: list = []

    def process(self, request: dict) -> AdapterResponse:
        start = time.time()
        event_id = request.get("botpress_event_id", "unknown")
        intent = request.get("intent", "help")
        user_id = request.get("telegram_user_id", "unknown")
        params = request.get("parsed_params", {})

        # Rate limit
        if not self.rate_limiter.check(user_id):
            elapsed = int((time.time() - start) * 1000)
            return AdapterResponse(
                botpress_event_id=event_id,
                status="error",
                reply_text="Trop de requetes. Attends 30 secondes.",
                safety_check="blocked",
                trace_id=self._trace_id(event_id),
                duration_ms=elapsed,
            )

        # Safety gate
        safety = self.safety.check(intent, params)
        if not safety["allowed"]:
            elapsed = int((time.time() - start) * 1000)
            resp = AdapterResponse(
                botpress_event_id=event_id,
                status="blocked",
                reply_text=f"Action bloquee: {safety['reason']}",
                safety_check="blocked",
                trace_id=self._trace_id(event_id),
                duration_ms=elapsed,
            )
            self._log(request, resp)
            return resp

        # Circuit breaker
        if self.circuit.is_open():
            elapsed = int((time.time() - start) * 1000)
            return AdapterResponse(
                botpress_event_id=event_id,
                status="error",
                reply_text="Gateway en maintenance, reessaie dans 2 minutes.",
                safety_check="passed",
                trace_id=self._trace_id(event_id),
                duration_ms=elapsed,
            )

        # Route to Gateway
        action = INTENT_TO_ACTION.get(intent, "static_help")
        gateway_request = self._build_gateway_request(request, action)

        try:
            gateway_resp = self._call_gateway(gateway_request)
            self.circuit.record_success()
            elapsed = int((time.time() - start) * 1000)

            resp = AdapterResponse(
                botpress_event_id=event_id,
                status=gateway_resp.get("status", "ok"),
                reply_text=gateway_resp.get("result", {}).get("summary", "OK"),
                reply_data=gateway_resp.get("result", {}).get("data", {}),
                safety_check="passed",
                trace_id=gateway_resp.get("trace_id", ""),
                duration_ms=elapsed,
            )
        except TimeoutError:
            self.circuit.record_failure()
            elapsed = int((time.time() - start) * 1000)
            resp = AdapterResponse(
                botpress_event_id=event_id,
                status="timeout",
                reply_text="Analyse en cours, delai depasse. Je te tiens au courant.",
                safety_check="passed",
                trace_id=self._trace_id(event_id),
                duration_ms=elapsed,
            )
        except ConnectionError:
            self.circuit.record_failure()
            elapsed = int((time.time() - start) * 1000)
            resp = AdapterResponse(
                botpress_event_id=event_id,
                status="error",
                reply_text="Gateway inaccessible, reessaie plus tard.",
                safety_check="passed",
                trace_id=self._trace_id(event_id),
                duration_ms=elapsed,
            )

        self._log(request, resp)
        return resp

    def _build_gateway_request(self, req: dict, action: str) -> dict:
        return {
            "intent": action,
            "context": {
                "user_id": f"telegram_{req.get('telegram_chat_id', 'unknown')}",
                "symbol": req.get("parsed_params", {}).get("symbol", ""),
                "timeframe": req.get("parsed_params", {}).get("timeframe", ""),
            },
            "payload": {
                "query": req.get("original_message", ""),
                "attachments": [],
            },
            "options": {
                "dry_run": True,
                "max_symbols": 5,
                "timeout_ms": OPENCLAW_TIMEOUT_MS,
            },
        }

    def _call_gateway(self, request: dict) -> dict:
        import requests as r
        token = os.getenv("OPENCLAW_TOKEN", "")
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        resp = r.post(
            f"{OPENCLAW_GATEWAY_URL}/api/v1/execute",
            headers=headers,
            json=request,
            timeout=OPENCLAW_TIMEOUT_MS / 1000,
        )
        if resp.status_code >= 500:
            raise ConnectionError(f"Gateway error {resp.status_code}")
        return resp.json()

    def _trace_id(self, event_id: str) -> str:
        import uuid
        return f"trace-{event_id}-{uuid.uuid4().hex[:8]}"

    def _log(self, request: dict, response: AdapterResponse):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "botpress_event_id": request.get("botpress_event_id"),
            "telegram_user_id": request.get("telegram_user_id"),
            "intent": request.get("intent"),
            "gateway_status": response.status,
            "safety_status": response.safety_check,
            "trace_id": response.trace_id,
            "duration_ms": response.duration_ms,
        }
        self.logs.append(entry)
        log.info(json.dumps(entry, ensure_ascii=False))
