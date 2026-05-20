#!/usr/bin/env python3
"""
E2E Dry-Run Pipeline - prouve le flux complet :
signal_router → proposition_engine → validation_gate → trade_executor
→ result_tracker → datasheet_writer → learning_feeder → LocalCMS

Sortie : JSON complet avec chaque étape + timestamps.
Aucun ordre live, aucun fichier écrit.
DRY_RUN=1 et PAPER_MODE=1 par défaut.
"""
from __future__ import annotations
import json
import logging
import sys
import time
import os
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


def check_lcms_endpoints() -> dict:
    results = {}
    for ep in ["/health", "/menu", "/menu/state", "/runtime/tmux"]:
        try:
            import urllib.request
            r = urllib.request.urlopen(f"http://127.0.0.1:8700{ep}", timeout=3)
            results[ep] = {"status": r.status, "ok": r.status == 200}
        except Exception as e:
            results[ep] = {"status": "unreachable", "ok": False, "error": str(e)}
    return results


def main() -> dict:
    t0 = time.time()
    report: dict[str, object] = {
        "pipeline": "E2E dry-run pipeline",
        "dry_run": DRY_RUN,
        "paper_mode": PAPER_MODE,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "steps": [],
    }

    # ── Step 1: signal_router ──────────────────────────────────────
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

    # ── Step 1b: desk_pro dry-run synthesis (fixture-only) ──────────
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

    # ── Step 1c: notification_dispatcher (dry-run) ──────────────────
    log.info("=== Step 1c: notification_dispatcher (dry-run) ===")
    from modules.notification_dispatcher.app.dispatcher import NotificationDispatcher
    from modules.notification_dispatcher.app.events import PipelineEvent

    dispatcher = NotificationDispatcher()
    dispatch_results = []
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

    # ── Step 2: proposition_engine ──────────────────────────────────
    log.info("=== Step 2: proposition_engine ===")
    from modules.proposition_engine.app.schema import PropositionRequest, NormalizedSignal as PropSignal
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

    # ── Step 3: validation_gate ────────────────────────────────────
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

    # ── Step 4: trade_executor ──────────────────────────────────────
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

    # ── Step 5: result_tracker ──────────────────────────────────────
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

    # ── Step 6: datasheet_writer ────────────────────────────────────
    log.info("=== Step 6: datasheet_writer ===")
    from modules.datasheet_writer.app.writer import DatasheetWriter

    write_result = DatasheetWriter().write(record, dry_run=DRY_RUN)
    report["steps"].append(step("6_datasheet_writer", write_result))
    log.info("dry_run=%s written=%s", write_result.dry_run, write_result.written)

    # ── Step 7: learning_feeder ─────────────────────────────────────
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

    # ── Step 8: LocalCMS verification ──────────────────────────────
    log.info("=== Step 8: LocalCMS endpoints ===")
    lcms = check_lcms_endpoints()
    report["localcms"] = lcms
    lcms_ok = all(v["ok"] for v in lcms.values())
    report["localcms_ok"] = lcms_ok
    log.info("LocalCMS reachable=%s", lcms_ok)

    return report


if __name__ == "__main__":
    report = main()
    print(json.dumps(report, indent=2, default=str))
    ok = report.get("all_ok", False)
    sys.exit(0 if ok else 1)
