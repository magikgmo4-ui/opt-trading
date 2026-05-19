from __future__ import annotations
from dataclasses import dataclass, field
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.proposition_engine.app.schema import Proposition
from modules.result_tracker.app.schema import TradeRecord


@dataclass
class FeedRequest:
    signal_id: str
    proposition: Proposition
    trade_record: TradeRecord
    request_id: str = ""
    dry_run: bool = True
    bridge_timeout_s: int = 90
    store_brick: bool = True    # persist to learning_bricks store


@dataclass
class FeedResult:
    request_id: str
    signal_id: str
    bridge_status: str      # ok | error | timeout | dry_run
    brick_stored: bool
    brick_id: str
    summary: str
    duration_ms: int = 0
    dry_run: bool = True
    meta: dict = field(default_factory=dict)
