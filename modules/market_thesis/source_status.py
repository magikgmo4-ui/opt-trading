"""
Source status tracking — PR2.

Evaluates freshness, availability, and error state for each data source
consumed by the Market Thesis Engine. Never crashes on missing/invalid sources.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import FRESHNESS_THRESHOLDS


@dataclass
class SourceStatus:
    """Status of a single data source."""

    name: str
    contract: str
    path: Optional[str] = None

    state: str = "missing"  # fresh | warm | stale | expired | missing | error
    age_minutes: Optional[float] = None
    error_message: Optional[str] = None
    records_count: int = 0
    records_valid: int = 0
    records_filtered: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "contract": self.contract,
            "state": self.state,
            "age_minutes": self.age_minutes,
            "records_count": self.records_count,
            "records_valid": self.records_valid,
            "records_filtered": self.records_filtered,
            "error": self.error_message,
        }


@dataclass
class SourceStatusSet:
    """Collection of source statuses for a single symbol aggregation."""

    symbol: str
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    items: List[SourceStatus] = field(default_factory=list)
    overall_freshness: str = "missing"  # fresh | warm | stale | expired | missing

    @property
    def missing_sources(self) -> List[str]:
        return [s.name for s in self.items if s.state == "missing"]

    @property
    def stale_sources(self) -> List[str]:
        return [s.name for s in self.items if s.state in ("stale", "expired")]

    @property
    def error_sources(self) -> List[str]:
        return [s.name for s in self.items if s.state == "error"]

    @property
    def fresh_sources(self) -> List[str]:
        return [s.name for s in self.items if s.state in ("fresh", "warm")]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "generated_at": self.generated_at.isoformat(),
            "overall_freshness": self.overall_freshness,
            "sources": [s.to_dict() for s in self.items],
            "missing": self.missing_sources,
            "stale": self.stale_sources,
            "errors": self.error_sources,
            "fresh": self.fresh_sources,
        }


def evaluate_freshness(
    file_path: str | Path | None,
    data_ts: Optional[datetime] = None,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Evaluate the freshness state of a data source.

    Returns a dict with state, age_minutes, and error.

    Priority:
    1. data_ts (extracted from payload)
    2. file mtime (fallback)

    States:
    - fresh:  age <= 5 minutes
    - warm:   age <= 30 minutes
    - stale:  age <= 4 hours
    - expired: age > 4 hours
    - missing: file_path is None or does not exist
    - error:   file exists but is unreadable
    """
    if now is None:
        now = datetime.now(timezone.utc)

    if file_path is None:
        return {"state": "missing", "age_minutes": None, "error": None}

    path = Path(file_path) if isinstance(file_path, str) else file_path

    if not path.exists():
        return {"state": "missing", "age_minutes": None, "error": None}

    # Determine the best timestamp
    if data_ts is not None:
        ref_ts = data_ts
    else:
        try:
            mtime = os.path.getmtime(str(path))
            ref_ts = datetime.fromtimestamp(mtime, tz=timezone.utc)
        except OSError:
            return {"state": "error", "age_minutes": None, "error": "Cannot stat file"}

    # Ensure timezone-aware comparison
    if ref_ts.tzinfo is None:
        ref_ts = ref_ts.replace(tzinfo=timezone.utc)

    age_seconds = (now - ref_ts).total_seconds()
    age_minutes = age_seconds / 60.0

    if age_minutes <= 5:
        state = "fresh"
    elif age_minutes <= 30:
        state = "warm"
    elif age_minutes <= 240:
        state = "stale"
    else:
        state = "expired"

    return {
        "state": state,
        "age_minutes": round(age_minutes, 2),
        "error": None,
    }


def evaluate_overall_freshness(statuses: List[SourceStatus]) -> str:
    """Compute the overall freshness from a list of source statuses.

    Returns the worst state excluding 'error' and 'missing'.
    Only considers sources that are actually present.
    """
    present = [s for s in statuses if s.state not in ("missing", "error")]
    if not present:
        return "missing"

    states = [s.state for s in present]
    if "expired" in states:
        return "expired"
    if "stale" in states:
        return "stale"
    if "warm" in states:
        return "warm"
    return "fresh"
