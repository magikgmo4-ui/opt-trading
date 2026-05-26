from __future__ import annotations
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .schema import CloseRequest, TradeRecord

try:
    from modules.notification_dispatcher.app.dispatcher import NotificationDispatcher
    from modules.notification_dispatcher.app.events import PipelineEvent
    _DISPATCHER_AVAILABLE = True
except ImportError:
    _DISPATCHER_AVAILABLE = False

    class PipelineEvent:  # type: ignore  # minimal fallback when dispatcher unavailable
        def __init__(self, *, event_type, signal_id="", request_id="", payload=None):
            self.event_type = event_type
            self.signal_id = signal_id
            self.request_id = request_id
            self.payload = payload or {}

log = logging.getLogger("result_tracker")

_OUTCOME_EPSILON = 1e-8


def _epoch_to_iso(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat()


def _compute_pnl(
    action: str,
    entry: float,
    close: float,
    qty: float,
    fee_rate: float,
) -> tuple[float, float, float]:
    """Return (gross_pnl, net_pnl, fees)."""
    direction = 1.0 if action.upper() == "BUY" else -1.0
    gross = direction * (close - entry) * qty
    # round-trip taker fee: entry side + close side
    fees = (entry * qty * fee_rate) + (close * qty * fee_rate)
    net = gross - fees
    return round(gross, 8), round(net, 8), round(fees, 8)


def _outcome(net_pnl: float) -> str:
    if net_pnl > _OUTCOME_EPSILON:
        return "win"
    if net_pnl < -_OUTCOME_EPSILON:
        return "loss"
    return "breakeven"


class ResultTracker:
    def __init__(self, dispatcher=None):
        if dispatcher is not None:
            self.dispatcher = dispatcher
        elif _DISPATCHER_AVAILABLE:
            self.dispatcher = NotificationDispatcher()
        else:
            self.dispatcher = None

    def _notify(self, record: TradeRecord, dry_run: bool) -> dict:
        if self.dispatcher is None:
            return {"ok": False, "error": "no_dispatcher"}
        event = PipelineEvent(
            event_type="result_known",
            signal_id=record.signal_id,
            request_id=record.request_id,
            payload={
                "ticker": record.ticker,
                "side": record.action,
                "gross_pnl": record.gross_pnl,
                "net_pnl": record.net_pnl,
                "fees": record.fees,
                "duration": f"{record.duration_s:.1f}s",
            },
        )
        return self.dispatcher.dispatch(event, dry_run=dry_run)

    def track(self, req: CloseRequest) -> TradeRecord:
        t = req.trade_result
        now = time.time()

        close_ts = req.close_timestamp if req.close_timestamp > 0 else now
        opened_ts = req.opened_at if req.opened_at > 0 else (close_ts - t.duration_ms / 1000.0)
        duration_s = max(0.0, close_ts - opened_ts)

        gross, net, fees = _compute_pnl(
            t.action, t.fill_price, req.close_price, t.fill_qty, req.fee_rate
        )

        record = TradeRecord(
            trade_id=t.trade_id,
            request_id=t.request_id,
            signal_id=t.signal_id,
            ticker=t.ticker,
            action=t.action,
            entry_price=t.fill_price,
            close_price=req.close_price,
            fill_qty=t.fill_qty,
            size_pct=t.size_pct,
            sl=t.sl,
            tp=t.tp,
            gross_pnl=gross,
            net_pnl=net,
            fees=fees,
            duration_s=round(duration_s, 3),
            outcome=_outcome(net),
            opened_at=_epoch_to_iso(opened_ts),
            closed_at=_epoch_to_iso(close_ts),
            dry_run=req.dry_run,
        )

        notif = self._notify(record, dry_run=req.dry_run)
        record.meta["notif"] = notif

        log.info(
            "result_tracker trade_id=%s outcome=%s net_pnl=%.4f dry_run=%s",
            record.trade_id, record.outcome, record.net_pnl, req.dry_run,
        )

        return record
