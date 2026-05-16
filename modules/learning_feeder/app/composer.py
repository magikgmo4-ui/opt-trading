from __future__ import annotations
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.proposition_engine.app.schema import Proposition
from modules.result_tracker.app.schema import TradeRecord

_WIN_FEEDBACK = "Positive reinforcement — setup worked as expected."
_LOSS_FEEDBACK = "Negative feedback — review entry/exit criteria and confidence calibration."
_NEUTRAL_FEEDBACK = "Neutral — breakeven outcome, no strong learning signal."


def compose_feedback(proposition: Proposition, trade_record: TradeRecord) -> str:
    """Compose structured feedback text for OpenClaw learning cycle."""
    outcome = trade_record.outcome
    feedback_line = {
        "win": _WIN_FEEDBACK,
        "loss": _LOSS_FEEDBACK,
        "breakeven": _NEUTRAL_FEEDBACK,
    }.get(outcome, _NEUTRAL_FEEDBACK)

    lines = [
        "=== LEARNING FEEDBACK ===",
        f"signal_id : {trade_record.signal_id}",
        f"ticker    : {trade_record.ticker}  action={trade_record.action}",
        f"entry     : {trade_record.entry_price}  →  close={trade_record.close_price}",
        f"outcome   : {outcome.upper()}",
        f"pnl       : gross={trade_record.gross_pnl:.4f}  net={trade_record.net_pnl:.4f}  fees={trade_record.fees:.4f}",
        f"size      : size_pct={trade_record.size_pct:.1%}  fill_qty={trade_record.fill_qty}",
        f"duration  : {trade_record.duration_s:.1f}s",
        f"confidence: {proposition.confidence:.2f}",
        f"rationale : {proposition.rationale}",
        f"feedback  : {feedback_line}",
    ]
    return "\n".join(lines)
