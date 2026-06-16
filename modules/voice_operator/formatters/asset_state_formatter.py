"""
Voice Operator — Asset State Formatter (PR8 extension, now using V2 templates).

Produces rich contextual analysis for individual assets
combining Market Thesis data with Executive Intelligence context.

Now delegates to the Presentation Templates Engine for cognitive-optimized output.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


DISPLAY_NAMES = {"XAU": "Or (Gold)", "SPCX": "SpaceX (SPCX)"}
SPOKEN_NAMES = {"XAU": "l'or", "SPCX": "SpaceX"}


def _gather_asset_state(symbol: str) -> Optional[Dict[str, Any]]:
    """Gather all data for a rich asset state analysis."""
    try:
        from modules.desk_pro.service.market_thesis_reader import get_market_thesis_or_build
        thesis = get_market_thesis_or_build(symbol.upper())
    except Exception:
        thesis = None

    executive = None
    if thesis:
        try:
            from modules.desk_pro.service.executive_reader import get_executive
            executive = get_executive()
        except Exception:
            pass

    reliability = None
    try:
        from modules.market_thesis.reliability_engine import evaluate_reliability
        rel = evaluate_reliability(symbol.upper())
        reliability = {"score": rel.reliability_score, "grade": rel.grade, "sample_size": rel.sample_size}
    except Exception:
        reliability = None

    return {
        "symbol": symbol.upper(),
        "thesis": thesis,
        "executive": executive,
        "reliability": reliability,
    }


def format_asset_state_spoken(symbol: str, data: Optional[Dict[str, Any]] = None) -> str:
    """Short natural French spoken summary — delegates to V2 template engine."""
    from modules.executive_intelligence.templates.asset_analysis import render_asset_analysis
    if data is None:
        data = _gather_asset_state(symbol)
    result = render_asset_analysis(symbol, data)
    return result["spoken_text"]


def format_asset_state_display(symbol: str, data: Optional[Dict[str, Any]] = None) -> str:
    """Full structured French display text — delegates to V2 template engine."""
    from modules.executive_intelligence.templates.asset_analysis import render_asset_analysis
    if data is None:
        data = _gather_asset_state(symbol)
    result = render_asset_analysis(symbol, data)
    return result["display_text"]
