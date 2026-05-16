from __future__ import annotations
from dataclasses import dataclass, field
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.trade_executor.app.schema import TradeResult


@dataclass
class CloseRequest:
    trade_result: TradeResult
    close_price: float
    opened_at: float = 0.0   # epoch seconds; 0 = now - duration_ms
    close_timestamp: float = 0.0  # epoch seconds; 0 = now
    dry_run: bool = True
    fee_rate: float = 0.0006  # 0.06% taker per side


@dataclass
class TradeRecord:
    trade_id: str
    request_id: str
    signal_id: str
    ticker: str
    action: str           # BUY | SELL
    entry_price: float
    close_price: float
    fill_qty: float
    size_pct: float
    sl: float | None
    tp: float | None
    gross_pnl: float
    net_pnl: float
    fees: float
    duration_s: float
    outcome: str          # win | loss | breakeven
    opened_at: str        # ISO 8601
    closed_at: str        # ISO 8601
    dry_run: bool = True
    meta: dict = field(default_factory=dict)
