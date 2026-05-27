from __future__ import annotations
import json
import logging
import re
import time
import uuid
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.strategy.adapter import validate_strategy_id, log_unknown_strategy_id_warning
from .schema import PropositionRequest, Proposition, BridgeCallError
from .engines import query_engines
from .builder_prompt import compose_prompt

log = logging.getLogger("proposition_engine")

try:
    from modules.openclaw_operator_bridge.app.bridge import OperatorBridge
    from modules.openclaw_operator_bridge.app.schema import BridgeRequest
except ImportError:
    OperatorBridge = None  # type: ignore
    BridgeRequest = None  # type: ignore


_DRY_RUN_STUB = {
    "action": "HOLD",
    "size_pct": 0.0,
    "entry": 0.0,
    "sl": None,
    "tp": None,
    "confidence": 0.0,
    "rationale": "dry_run — OpenClaw not called",
}


def _parse_proposition(text: str, signal_price: float) -> dict:
    """Extract JSON from OpenClaw response. Never raises."""
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return {
                "action": str(data.get("action", "HOLD")).upper(),
                "size_pct": float(data.get("size_pct", 0.0)),
                "entry": float(data.get("entry", signal_price)),
                "sl": float(data["sl"]) if data.get("sl") is not None else None,
                "tp": float(data["tp"]) if data.get("tp") is not None else None,
                "confidence": float(data.get("confidence", 0.0)),
                "rationale": str(data.get("rationale", text[:200])),
            }
    except Exception:
        pass
    return {
        "action": "HOLD",
        "size_pct": 0.0,
        "entry": signal_price,
        "sl": None,
        "tp": None,
        "confidence": 0.0,
        "rationale": text[:500] if text else "parse_failed",
    }


class PropositionEngine:
    def propose(self, request: PropositionRequest) -> Proposition:
        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        if not validate_strategy_id(request.signal.strategy_id):
            log_unknown_strategy_id_warning(request.signal.strategy_id, "proposition_engine")

        t0 = time.monotonic()
        engines_ctx: dict = {}

        try:
            engines_ctx = query_engines(request.signal)
        except Exception as exc:
            engines_ctx = {"error": str(exc)}

        if request.dry_run:
            stub = _DRY_RUN_STUB.copy()
            stub["entry"] = request.signal.price
            stub["sl"] = request.signal.sl
            stub["tp"] = request.signal.tp
            return Proposition(
                request_id=request.request_id,
                signal_id=request.signal.signal_id,
                **stub,
                engines_context=engines_ctx,
                duration_ms=int((time.monotonic() - t0) * 1000),
                dry_run=True,
                status="ok",
            )

        try:
            prompt = compose_prompt(request.signal, engines_ctx)
            bridge = OperatorBridge()
            br = BridgeRequest(
                action="evaluate",
                instruction=prompt,
                context=f"ticker={request.signal.ticker} side={request.signal.side}",
                request_id=request.request_id,
                timeout_s=request.timeout_s,
            )
            resp = bridge.send(br)

            duration_ms = int((time.monotonic() - t0) * 1000)

            if resp.status != "ok":
                parsed = _parse_proposition("", request.signal.price)
                parsed["rationale"] = f"bridge_error: {resp.error}"
                return Proposition(
                    request_id=request.request_id,
                    signal_id=request.signal.signal_id,
                    **parsed,
                    engines_context=engines_ctx,
                    duration_ms=duration_ms,
                    status="error",
                    error=resp.error,
                )

            parsed = _parse_proposition(resp.content, request.signal.price)
            return Proposition(
                request_id=request.request_id,
                signal_id=request.signal.signal_id,
                **parsed,
                engines_context=engines_ctx,
                duration_ms=duration_ms,
                status="ok",
            )

        except Exception as exc:
            duration_ms = int((time.monotonic() - t0) * 1000)
            return Proposition(
                request_id=request.request_id,
                signal_id=request.signal.signal_id,
                action="HOLD",
                size_pct=0.0,
                entry=request.signal.price,
                sl=request.signal.sl,
                tp=request.signal.tp,
                confidence=0.0,
                rationale=f"exception: {exc}",
                engines_context=engines_ctx,
                duration_ms=duration_ms,
                status="error",
                error=str(exc),
            )
