"""
Archive — PR5.

Persists generated theses to disk:
- history/{SYM}/{thesis_id}.json — full archive
- by_symbol/{SYM}/latest.json — latest thesis per symbol

Files are written under data/market_thesis/.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .models import MarketThesis

ARCHIVE_ROOT = Path(__file__).resolve().parents[2] / "data" / "market_thesis"


def ensure_dirs() -> None:
    """Create archive directory structure if it doesn't exist."""
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    (ARCHIVE_ROOT / "by_symbol").mkdir(exist_ok=True)
    (ARCHIVE_ROOT / "history").mkdir(exist_ok=True)


def save(thesis: MarketThesis) -> Path:
    """Save a thesis to the archive.

    Returns the path to the saved file.
    """
    ensure_dirs()

    sym_dir = ARCHIVE_ROOT / "history" / thesis.symbol
    sym_dir.mkdir(parents=True, exist_ok=True)

    path = sym_dir / f"{thesis.metadata.thesis_id}.json"
    path.write_text(thesis.model_dump_json(by_alias=True, indent=2))
    return path


def save_latest(thesis: MarketThesis) -> Path:
    """Save a thesis as the latest for its symbol.

    Returns the path to the saved file.
    """
    ensure_dirs()

    sym_dir = ARCHIVE_ROOT / "by_symbol" / thesis.symbol
    sym_dir.mkdir(parents=True, exist_ok=True)

    path = sym_dir / "latest.json"
    path.write_text(thesis.model_dump_json(by_alias=True, indent=2))
    return path


def save_all(thesis: MarketThesis) -> tuple[Path, Path]:
    """Save a thesis to both archive and latest."""
    hist_path = save(thesis)
    latest_path = save_latest(thesis)
    return hist_path, latest_path


def load_latest(symbol: str) -> Optional[MarketThesis]:
    """Load the latest thesis for a symbol.

    Returns None if no thesis exists.
    """
    path = ARCHIVE_ROOT / "by_symbol" / symbol / "latest.json"
    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text())
        return MarketThesis(**data)
    except Exception:
        return None


def load_history(symbol: str, limit: int = 30) -> List[MarketThesis]:
    """Load historical theses for a symbol, newest first.

    Args:
        symbol: Canonical symbol
        limit: Maximum number of theses to return

    Returns:
        List of MarketThesis, sorted by generated_at descending.
    """
    hist_dir = ARCHIVE_ROOT / "history" / symbol
    if not hist_dir.exists():
        return []

    files = sorted(hist_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    theses: List[MarketThesis] = []
    for f in files[:limit]:
        try:
            data = json.loads(f.read_text())
            theses.append(MarketThesis(**data))
        except Exception:
            continue

    return theses


def build_and_save(symbol: str) -> MarketThesis:
    """Build a thesis and persist it (archive + latest).

    Convenience wrapper — call from thesis_engine or CLI.
    """
    from .thesis_engine import build_thesis

    thesis = build_thesis(symbol)
    save_all(thesis)
    return thesis
