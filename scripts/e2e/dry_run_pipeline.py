#!/usr/bin/env python3
"""
E2E Dry-Run Pipeline - prouve le flux complet :
signal_router → proposition_engine → validation_gate → trade_executor
→ result_tracker → datasheet_writer → learning_feeder → LocalCMS gate

Sortie : JSON complet avec chaque étape + timestamps.
Aucun ordre live, aucun fichier écrit.
DRY_RUN=1 et PAPER_MODE=1 par défaut.

LocalCMS gate (step 8) :
  default            : absence LocalCMS = WARN_SKIPPED, rc=0
  REQUIRE_LOCALCMS_E2E=1 : absence LocalCMS = BLOCKED, rc=1
  SKIP_LOCALCMS_E2E=1    : LocalCMS check sauté, rc=0
  LOCALCMS_URL           : URL custom (défaut http://127.0.0.1:8700)
"""
from __future__ import annotations
import json
import logging
import sys
import time
import os
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
log = logging.getLogger("e2e_dry_run_pipeline")

DRY_RUN = os.environ.get("DRY_RUN", "1") == "1"
PAPER_MODE = os.environ.get("PAPER_MODE", "1") == "1"

# ── LocalCMS gate configuration ──────────────────────────────────────────────
LOCALCMS_URL = os.environ.get("LOCALCMS_URL", "http://127.0.0.1:8700")
REQUIRE_LOCALCMS = os.environ.get("REQUIRE_LOCALCMS_E2E", "0") == "1"
SKIP_LOCALCMS = os.environ.get("SKIP_LOCALCMS_E2E", "0") == "1"

_LOCALCMS_ENDPOINTS = ["/health", "/menu", "/menu/state", "/runtime/tmux"]


@dataclass
class E2ELocalCMSGateResult:
    status: str  # PASS | WARN_SKIPPED | BLOCKED
    reason: str
    url: str
    mode: str    # default | require | skip


def check_localcms_available(url: str, timeout: float = 2.0) -> tuple[bool, str]:
    """Probe LocalCMS /health. Returns (reachable, error_msg). Never raises."""
    try:
        r = urllib.request.urlopen(f"{url}/health", timeout=timeout)
        return r.status == 200, ""
    except Exception as exc:
        return False, str(exc)


def classify_localcms_gate(
    require: bool | None = None,
    skip: bool | None = None,
    url: str | None = None,
) -> E2ELocalCMSGateResult:
    """Classify LocalCMS availability into a structured gate result.

    Parameters default to module-level env-derived values so the function is
    testable by passing explicit args without mutating the environment.
    """
    _require = REQUIRE_LOCALCMS if require is None else require
    _skip = SKIP_LOCALCMS if skip is None else skip
    _url = LOCALCMS_URL if url is None else url
    mode = "skip" if _skip else ("require" if _require else "default")

    if _skip:
        return E2ELocalCMSGateResult(
            status="WARN_SKIPPED",
            reason="SKIP_LOCALCMS_E2E=1 — LocalCMS check explicitly skipped",
            url=_url,
            mode=mode,
        )

    reachable, err = check_localcms_available(_url)

    if reachable:
        return E2ELocalCMSGateResult(
            status="PASS",
            reason="LocalCMS /health reachable",
            url=_url,
            mode=mode,
        )

    if _require:
        return E2ELocalCMSGateResult(
            status="BLOCKED",
            reason=f"REQUIRE_LOCALCMS_E2E=1 — LocalCMS not reachable at {_url}: {err}",
            url=_url,
            mode=mode,
        )

    # Default: LocalCMS is optional — WARN_SKIPPED does not affect rc
    return E2ELocalCMSGateResult(
        status="WARN_SKIPPED",
        reason=f"LocalCMS not reachable (optional in default mode): {err}",
        url=_url,
        mode=mode,
    )


def _check_lcms_endpoints_detail(url: str) -> dict:
    """Probe all LocalCMS endpoints for detail when gate=PASS."""
    results = {}
    for ep in _LOCALCMS_ENDPOINTS:
        try:
            r = urllib.request.urlopen(f"{url}{ep}", timeout=3)
            results[ep] = {"status": r.status, "ok": r.status == 200}
        except Exception as exc:
            results[ep] = {"status": "unreachable", "ok": False, "error": str(exc)}
    return results


# ── Pipeline helpers ──────────────────────────────────────────────────────────

def _to_serializable(obj: object) -> dict:
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "__dataclass_fields__"):
        from dataclasses import asdict
        d = asdict(obj)
        for key in ("proposition", "gate_decision", "trade_result",
                    "trade_record", "signal", "engines_context"):
            d.pop(key, None)
        return d
    if isinstance(obj, dict):
        return obj
    return {"value": str(obj)}


def step(name: str, result: object) -> dict:
    return {
        "step": name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "result": _to_serializable(result),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> dict:
    t0 = time.time()
    report: dict[str, object] = {
        "pipeline": "E2E dry-run pipeline",
        "dry_run": DRY_RUN,
        "paper_mode": PAPER_MODE,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "steps": [],
    }

    # ── Dispatcher setup (graceful fallback if requests not in env) ────────────
    class _NoOpDispatcher:
        def dispatch(self, *_, **__):
            return {"ok": False, "skipped": "dispatcher_unavailable"}

    try:
        from modules.notification_dispatcher.app.dispatcher import NotificationDispatcher
        from modules.notification_dispatcher.app.events import PipelineEvent
        dispatcher = NotificationDispatcher()
    except ImportError:
        dispatcher = _NoOpDispatcher()

        class PipelineEvent:  # type: ignore  # minimal fallback
            def __init__(self, *, event_type, payload=None, signal_id="", request_id=""):
                self.event_type = event_type
                self.payload = payload or {}
                self.signal_id = signal_id
                self.request_id = request_id

    dispatch_results: list = []

    # ── Step 1: signal_router ──────────────────────────────────────────────────
    log.info("=== Step 1: signal_router ===")
    from modules.signal_router.app.router import route

    raw_signal = {
        "engine": "e2e_dry_run",
        "signal": "BUY",
        "symbol": "BTCUSDT",
        "tf": "1h",
        "price": 65000.0,
        "tp": 68000.0,
        "sl": 63000.0,
        "reason": "E2E dry-run pipeline test",
        "strategy_id": "e2e_dry_run",
    }
    normalized = route(raw_signal)
    report["steps"].append(step("1_signal_router", normalized))
    log.info("signal_id=%s ticker=%s side=%s", normalized.signal_id, normalized.ticker, normalized.side)

    # ── Step 1b: desk_pro dry-run synthesis (fixture-only) ────────────────────
    log.info("=== Step 1b: desk_pro dry-run synthesis ===")
    from modules.desk_pro.dry_run import run_desk_pro_dry_run

    now_iso = datetime.now(timezone.utc).isoformat()
    capture_id = f"e2e_capture_{normalized.signal_id}"
    signal_event_v0 = {
        "engine": raw_signal["engine"],
        "signal": raw_signal["signal"],
        "symbol": raw_signal["symbol"],
        "tf": raw_signal["tf"],
        "price": raw_signal["price"],
        "tp": raw_signal["tp"],
        "sl": raw_signal["sl"],
        "reason": raw_signal["reason"],
        "_ts": now_iso,
    }
    visual_context = {
        "source": "e2e_fixture",
        "capture_id": capture_id,
        "symbol": raw_signal["symbol"],
        "timeframe": raw_signal["tf"],
        "captured_at": now_iso,
        "image_ref": "fixture://desk_pro/snapshot.png",
        "status": "ok",
    }
    desk_snapshot = {
        "symbol": raw_signal["symbol"],
        "tf": raw_signal["tf"],
        "snapshot_ts": now_iso,
        "path": "C:/fixtures/desk_pro_snapshot.png",
    }
    desk_pro_synthesis = run_desk_pro_dry_run(
        signal_event_v0,
        visual_context=visual_context,
        desk_snapshot=desk_snapshot,
    )
    report["steps"].append(step("1b_desk_pro_dry_run", desk_pro_synthesis))

    # ── Step 1c: notification_dispatcher (dry-run) ────────────────────────────
    log.info("=== Step 1c: notification_dispatcher (dry-run) ===")
    dispatch_results.append(
        dispatcher.dispatch(
            PipelineEvent(
                event_type="signal_received",
                payload={
                    "ticker": normalized.ticker,
                    "side": normalized.side,
                    "price": normalized.price,
                    "tf": normalized.tf,
                    "strategy_id": raw_signal.get("strategy_id", ""),
                    "strategy_version": raw_signal.get("strategy_version", ""),
                },
                signal_id=normalized.signal_id,
            ),
            dry_run=True,
        )
    )
    report["steps"].append(step("1c_notification_dispatcher_dry_run", {"dispatch": dispatch_results}))

    # ── Step 2: proposition_engine ────────────────────────────────────────────
    log.info("=== Step 2: proposition_engine ===")
    from modules.proposition_engine.app.schema import NormalizedSignal as PropSignal
    from modules.proposition_engine.app.schema import Proposition

    prop_signal = PropSignal.from_dict(normalized.to_dict())

    import uuid as _uuid

    def _simulated_dry_run_propose(signal_proto, signal_obj):
        rid = str(_uuid.uuid4())
        t0 = time.monotonic()
        engines_ctx = {}
        try:
            from modules.proposition_engine.app.engines import query_engines
            engines_ctx = query_engines(signal_obj)
        except Exception as exc:
            engines_ctx = {"error": str(exc)}
        stub = {
            "action": "BUY",
            "size_pct": 0.15,
            "entry": signal_obj.price,
            "sl": signal_obj.sl,
            "tp": signal_obj.tp,
            "confidence": 0.82,
            "rationale": "E2E dry-run simulated proposition (bridge not called)",
        }
        return Proposition(
            request_id=rid,
            signal_id=signal_obj.signal_id,
            **stub,
            engines_context=engines_ctx,
            duration_ms=int((time.monotonic() - t0) * 1000),
            dry_run=True,
            status="ok",
        )

    proposition = _simulated_dry_run_propose(PropSignal, prop_signal)
    report["steps"].append(step("2_proposition_engine", proposition))
    log.info("action=%s confidence=%s", proposition.action, proposition.confidence)

    dispatch_results.append(
        dispatcher.dispatch(
            PipelineEvent(
                event_type="proposition_generated",
                payload={
                    "ticker": normalized.ticker,
                    "action": proposition.action,
                    "entry": proposition.entry,
                    "sl": proposition.sl,
                    "tp": proposition.tp,
                    "confidence": proposition.confidence,
                    "rationale": proposition.rationale,
                    "strategy_id": raw_signal.get("strategy_id", ""),
                    "strategy_version": raw_signal.get("strategy_version", ""),
                },
                signal_id=normalized.signal_id,
                request_id=proposition.request_id,
            ),
            dry_run=True,
        )
    )

    # ── Step 3: validation_gate ───────────────────────────────────────────────
    log.info("=== Step 3: validation_gate ===")
    from modules.validation_gate.app.schema import GateRequest
    from modules.validation_gate.app.gate import ValidationGate

    gate_req = GateRequest(
        proposition=proposition,
        ticker=normalized.ticker,
        dry_run=DRY_RUN,
        require_operator=False,
    )
    decision = ValidationGate().gate(gate_req)
    report["steps"].append(step("3_validation_gate", decision))
    log.info("verdict=%s", decision.verdict)

    if decision.verdict != "APPROVED":
        log.warning("Gate REJECTED - stopping pipeline")
        report["stopped_at"] = "validation_gate_rejected"
        report["duration_s"] = round(time.time() - t0, 3)
        return report

    # ── Step 4: trade_executor ────────────────────────────────────────────────
    log.info("=== Step 4: trade_executor ===")
    from modules.trade_executor.app.schema import TradeRequest
    from modules.trade_executor.app.executor import TradeExecutor

    trade_req = TradeRequest(
        gate_decision=decision,
        proposition=proposition,
        ticker=normalized.ticker,
        dry_run=DRY_RUN,
    )
    trade_result = TradeExecutor().execute(trade_req)
    report["steps"].append(step("4_trade_executor", trade_result))
    log.info("status=%s fill_price=%s", trade_result.status, trade_result.fill_price)

    # ── Step 5: result_tracker ────────────────────────────────────────────────
    log.info("=== Step 5: result_tracker ===")
    from modules.result_tracker.app.schema import CloseRequest
    from modules.result_tracker.app.tracker import ResultTracker

    close_price = proposition.tp if proposition.tp else proposition.entry * 1.02
    close_req = CloseRequest(
        trade_result=trade_result,
        close_price=close_price,
        dry_run=DRY_RUN,
    )
    record = ResultTracker().track(close_req)
    report["steps"].append(step("5_result_tracker", record))
    log.info("outcome=%s net_pnl=%s", record.outcome, record.net_pnl)

    dispatch_results.append(
        dispatcher.dispatch(
            PipelineEvent(
                event_type="result_known",
                payload={
                    "ticker": normalized.ticker,
                    "side": normalized.side,
                    "gross_pnl": getattr(record, "gross_pnl", ""),
                    "net_pnl": getattr(record, "net_pnl", ""),
                    "duration": getattr(record, "duration_s", ""),
                    "fees": getattr(record, "fees", ""),
                    "strategy_id": raw_signal.get("strategy_id", ""),
                    "strategy_version": raw_signal.get("strategy_version", ""),
                },
                signal_id=normalized.signal_id,
                request_id=proposition.request_id,
            ),
            dry_run=True,
        )
    )

    # ── Step 6: datasheet_writer ──────────────────────────────────────────────
    log.info("=== Step 6: datasheet_writer ===")
    from modules.datasheet_writer.app.writer import DatasheetWriter

    write_result = DatasheetWriter().write(record, dry_run=DRY_RUN)
    report["steps"].append(step("6_datasheet_writer", write_result))
    log.info("dry_run=%s written=%s", write_result.dry_run, write_result.written)

    # ── Step 7: learning_feeder ───────────────────────────────────────────────
    log.info("=== Step 7: learning_feeder ===")
    from modules.learning_feeder.app.schema import FeedRequest
    from modules.learning_feeder.app.feeder import LearningFeeder

    feed_req = FeedRequest(
        signal_id=record.signal_id,
        proposition=proposition,
        trade_record=record,
        dry_run=DRY_RUN,
        store_brick=False,
    )
    feed_result = LearningFeeder().feed(feed_req)
    report["steps"].append(step("7_learning_feeder", feed_result))
    log.info("bridge_status=%s brick_stored=%s", feed_result.bridge_status, feed_result.brick_stored)

    report["duration_s"] = round(time.time() - t0, 3)
    report["completed_at"] = datetime.now(timezone.utc).isoformat()
    all_ok = all(
        s["result"].get("status") not in ("error", "timeout", "skipped")
        if isinstance(s["result"], dict)
        else True
        for s in report["steps"]
    )
    report["all_ok"] = all_ok

    # ── Step 8: LocalCMS gate ─────────────────────────────────────────────────
    log.info("=== Step 8: LocalCMS gate ===")
    lcms_gate = classify_localcms_gate()
    log.info("LocalCMS gate: status=%s mode=%s reason=%s",
             lcms_gate.status, lcms_gate.mode, lcms_gate.reason)

    # Backward-compat keys expected by existing tests
    if lcms_gate.status == "PASS":
        lcms_endpoints = _check_lcms_endpoints_detail(lcms_gate.url)
    else:
        lcms_endpoints = {
            ep: {"status": lcms_gate.status.lower(), "ok": False, "reason": lcms_gate.reason}
            for ep in _LOCALCMS_ENDPOINTS
        }
    report["localcms"] = lcms_endpoints
    report["localcms_ok"] = lcms_gate.status == "PASS"
    report["localcms_gate"] = {
        "status": lcms_gate.status,
        "reason": lcms_gate.reason,
        "url": lcms_gate.url,
        "mode": lcms_gate.mode,
    }
    report["e2e_status"] = "PASS" if all_ok and lcms_gate.status != "BLOCKED" else "FAIL"

    return report


if __name__ == "__main__":
    report = main()
    print(json.dumps(report, indent=2, default=str))
    all_ok = report.get("all_ok", False)
    gate_blocked = report.get("localcms_gate", {}).get("status") == "BLOCKED"
    sys.exit(0 if (all_ok and not gate_blocked) else 1)
