from __future__ import annotations
from dataclasses import dataclass, field
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.proposition_engine.app.schema import Proposition


@dataclass
class GateRequest:
    proposition: Proposition
    request_id: str = ""
    ticker: str = ""        # from NormalizedSignal.ticker; used in notification
    dry_run: bool = False
    require_operator: bool = True
    timeout_s: int = 60
    poll_interval_s: float = 2.0


@dataclass
class GateDecision:
    request_id: str
    signal_id: str
    verdict: str            # APPROVED | REJECTED | HOLD | NEEDS_REVIEW
    reason: str
    risk_status: str        # ALLOW | BLOCK | CAUTION
    risk_reason: str
    operator_approved: bool | None = None
    duration_ms: int = 0
    dry_run: bool = False
    meta: dict = field(default_factory=dict)
