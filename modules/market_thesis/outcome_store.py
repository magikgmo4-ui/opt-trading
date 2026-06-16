"""
Outcome store — PR10.

Persists and loads ThesisOutcome records.
Storage: data/market_thesis/outcomes/by_symbol/{SYM}/{thesis_id}.json
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .outcome_models import ThesisOutcome

OUTCOME_ROOT = Path(__file__).resolve().parents[2] / "data" / "market_thesis" / "outcomes"


def ensure_dirs() -> None:
    OUTCOME_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTCOME_ROOT / "by_symbol").mkdir(exist_ok=True)


def save_outcome(outcome: ThesisOutcome) -> Path:
    """Persist an outcome to disk."""
    ensure_dirs()
    sym_dir = OUTCOME_ROOT / "by_symbol" / outcome.symbol
    sym_dir.mkdir(parents=True, exist_ok=True)
    path = sym_dir / f"{outcome.thesis_id}.json"
    path.write_text(outcome.model_dump_json(indent=2))
    return path


def load_outcome(symbol: str, thesis_id: str) -> Optional[ThesisOutcome]:
    """Load a single outcome by symbol and thesis_id."""
    path = OUTCOME_ROOT / "by_symbol" / symbol / f"{thesis_id}.json"
    if not path.exists():
        return None
    try:
        return ThesisOutcome(**json.loads(path.read_text()))
    except Exception:
        return None


def load_outcomes(symbol: str, limit: int = 100) -> List[ThesisOutcome]:
    """Load all outcomes for a symbol, newest first."""
    sym_dir = OUTCOME_ROOT / "by_symbol" / symbol
    if not sym_dir.exists():
        return []

    files = sorted(sym_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    outcomes: List[ThesisOutcome] = []
    for f in files[:limit]:
        try:
            outcomes.append(ThesisOutcome(**json.loads(f.read_text())))
        except Exception:
            continue
    return outcomes


def load_unresolved(symbol: str) -> List[ThesisOutcome]:
    """Load outcomes that haven't been fully resolved yet."""
    all_outcomes = load_outcomes(symbol, limit=200)
    return [o for o in all_outcomes if not o.resolved]


def count_outcomes(symbol: str) -> int:
    """Count total outcomes for a symbol."""
    sym_dir = OUTCOME_ROOT / "by_symbol" / symbol
    if not sym_dir.exists():
        return 0
    return len(list(sym_dir.glob("*.json")))
