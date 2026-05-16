from __future__ import annotations
import logging
import time
import uuid
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .schema import TradeRequest, TradeResult

try:
    from modules.execution_engine.adapters.paper import PaperAdapter
    _PAPER_AVAILABLE = True
except ImportError:
    _PAPER_AVAILABLE = False

try:
    from modules.notification_dispatcher.app.dispatcher import NotificationDispatcher
    from modules.notification_dispatcher.app.events import PipelineEvent
    _DISPATCHER_AVAILABLE = True
except ImportError:
    _DISPATCHER_AVAILABLE = False

log = logging.getLogger("trade_executor")

_GATE_APPROVED = "APPROVED"


class TradeExecutor:
    """
    Executes a trade proposition that has been APPROVED by the validation_gate.
    V1: paper adapter only — no live Bitget orders.
    """

    def __init__(self, dispatcher=None):
        if dispatcher is not None:
            self.dispatcher = dispatcher
        elif _DISPATCHER_AVAILABLE:
            self.dispatcher = NotificationDispatcher()
        else:
            self.dispatcher = None

        self._paper = PaperAdapter() if _PAPER_AVAILABLE else None

    def _paper_execute(self, req: TradeRequest) -> dict:
        if self._paper is None:
            return {"ok": False, "error": "paper_adapter_unavailable"}
        prop = req.proposition
        ticker = req.ticker or prop.signal_id
        order = {
            "symbol": ticker,
            "side": prop.action,
            "qty": prop.size_pct,
            "price": prop.entry,
            "sl": prop.sl,
            "tp": prop.tp,
        }
        return self._paper.execute_order(order)

    def _send_notification(self, result: TradeResult, dry_run: bool) -> dict:
        if self.dispatcher is None:
            return {"ok": False, "error": "no_dispatcher"}
        event = PipelineEvent(
            event_type="trade_executed",
            signal_id=result.signal_id,
            request_id=result.request_id,
            payload={
                "ticker": result.ticker,
                "side": result.action,
                "fill_price": result.fill_price,
                "fill_qty": result.fill_qty,
                "trade_id": result.trade_id,
            },
        )
        return self.dispatcher.dispatch(event, dry_run=dry_run)

    def execute(self, req: TradeRequest) -> TradeResult:
        if not req.request_id:
            req.request_id = str(uuid.uuid4())

        t0 = time.monotonic()
        ticker = req.ticker or req.proposition.signal_id
        prop = req.proposition

        # Gate must be APPROVED — hard invariant
        if req.gate_decision.verdict != _GATE_APPROVED:
            return TradeResult(
                request_id=req.request_id,
                signal_id=prop.signal_id,
                trade_id="",
                action=prop.action,
                ticker=ticker,
                fill_price=0.0,
                fill_qty=0.0,
                size_pct=prop.size_pct,
                sl=prop.sl,
                tp=prop.tp,
                status="rejected",
                reason=f"gate_not_approved: verdict={req.gate_decision.verdict}",
                duration_ms=int((time.monotonic() - t0) * 1000),
                dry_run=req.dry_run,
            )

        # Execute via paper adapter (V1 — no live Bitget)
        adapter_result = self._paper_execute(req)
        trade_id = f"paper_{ticker}_{uuid.uuid4().hex[:8]}"

        if not adapter_result.get("ok"):
            return TradeResult(
                request_id=req.request_id,
                signal_id=prop.signal_id,
                trade_id=trade_id,
                action=prop.action,
                ticker=ticker,
                fill_price=0.0,
                fill_qty=0.0,
                size_pct=prop.size_pct,
                sl=prop.sl,
                tp=prop.tp,
                status="error",
                reason=adapter_result.get("error", "adapter_error"),
                duration_ms=int((time.monotonic() - t0) * 1000),
                dry_run=req.dry_run,
                meta={"adapter": adapter_result},
            )

        fill_price = float(adapter_result.get("avg_price", prop.entry))
        fill_qty = float(adapter_result.get("filled_qty", prop.size_pct))
        status = "dry_run" if req.dry_run else "filled"

        result = TradeResult(
            request_id=req.request_id,
            signal_id=prop.signal_id,
            trade_id=trade_id,
            action=prop.action,
            ticker=ticker,
            fill_price=fill_price,
            fill_qty=fill_qty,
            size_pct=prop.size_pct,
            sl=prop.sl,
            tp=prop.tp,
            status=status,
            reason="paper_filled",
            duration_ms=int((time.monotonic() - t0) * 1000),
            dry_run=req.dry_run,
            meta={"adapter": adapter_result},
        )

        notif = self._send_notification(result, dry_run=req.dry_run)
        result.meta["notif"] = notif

        log.info(
            "trade_executor status=%s trade_id=%s ticker=%s action=%s fill=%.4f dry_run=%s",
            result.status, result.trade_id, ticker, prop.action, fill_price, req.dry_run,
        )

        return result
