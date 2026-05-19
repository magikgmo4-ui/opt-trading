from __future__ import annotations
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.proposition_engine.app.schema import Proposition

MIN_CONFIDENCE: float = float(os.getenv("GATE_MIN_CONFIDENCE", "0.6"))
HIGH_CONFIDENCE: float = float(os.getenv("GATE_HIGH_CONFIDENCE", "0.8"))
KILL_SWITCH_ENV = "TRADING_KILL_SWITCH"

_BLOCKED_ACTIONS = frozenset({"HOLD", "SKIP"})


def check_risk(proposition: Proposition) -> tuple[str, str]:
    """Return (risk_status, reason): ALLOW | BLOCK | CAUTION."""
    if os.getenv(KILL_SWITCH_ENV):
        return "BLOCK", "kill_switch_active"

    if proposition.action.upper() in _BLOCKED_ACTIONS:
        return "BLOCK", f"action={proposition.action}"

    if proposition.status == "error":
        return "BLOCK", f"proposition_error: {proposition.error or 'unknown'}"

    if proposition.confidence < MIN_CONFIDENCE:
        return "BLOCK", f"confidence={proposition.confidence:.3f} < {MIN_CONFIDENCE}"

    if proposition.confidence >= HIGH_CONFIDENCE:
        return "ALLOW", f"confidence={proposition.confidence:.3f} >= {HIGH_CONFIDENCE}"

    return "CAUTION", f"confidence={proposition.confidence:.3f} in medium range [{MIN_CONFIDENCE},{HIGH_CONFIDENCE})"
