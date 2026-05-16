from __future__ import annotations
from dataclasses import dataclass, field
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.proposition_engine.app.schema import Proposition
from modules.validation_gate.app.schema import GateDecision


@dataclass
class TradeRequest:
    gate_decision: GateDecision
    proposition: Proposition
    request_id: str = ""
    ticker: str = ""        # from NormalizedSignal.ticker
    dry_run: bool = True    # default True — safety; V1 always uses paper adapter


@dataclass
class TradeResult:
    request_id: str
    signal_id: str
    trade_id: str
    action: str             # BUY | SELL
    ticker: str
    fill_price: float
    fill_qty: float
    size_pct: float
    sl: float | None
    tp: float | None
    status: str             # filled | rejected | error | dry_run
    reason: str
    duration_ms: int = 0
    dry_run: bool = True
    meta: dict = field(default_factory=dict)
