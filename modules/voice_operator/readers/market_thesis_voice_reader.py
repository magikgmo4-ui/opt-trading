"""
Voice Operator — Market Thesis Reader (PR9).

Reads market theses from the DeskPro market_thesis_reader bridge.
No business logic. No recalculation. Pure pass-through.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def read_thesis_data(symbol: str) -> Optional[Dict[str, Any]]:
    """Get the latest thesis for a symbol.

    Returns None if unavailable.
    """
    try:
        from modules.desk_pro.service.market_thesis_reader import get_market_thesis_or_build
        return get_market_thesis_or_build(symbol.upper())
    except Exception:
        return None


def read_thesis_summary_data() -> List[Dict[str, Any]]:
    """Get summary of all 9 symbols."""
    try:
        from modules.desk_pro.service.market_thesis_reader import get_market_thesis_summary
        return get_market_thesis_summary()
    except Exception:
        return []
