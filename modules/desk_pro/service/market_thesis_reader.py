"""
DeskPro Market Thesis Reader — PR8.

Read-only bridge between DeskPro and the Market Thesis Engine.
No business logic. No computation. Pure pass-through.

Reads from the market_thesis module directly (same process).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def get_market_thesis(symbol: str) -> Optional[Dict[str, Any]]:
    """Get the latest market thesis for a symbol.

    Returns None if the thesis engine is unavailable or no thesis exists.
    """
    try:
        from modules.market_thesis.archive import load_latest
        thesis = load_latest(symbol.upper())
        if thesis is None:
            return None
        return thesis.model_dump(by_alias=True, mode="json")
    except Exception:
        return None


def get_market_thesis_summary() -> List[Dict[str, Any]]:
    """Get a summary of all 9 symbols (direction, confidence, one-liner)."""
    symbols = ["BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU"]
    items: List[Dict[str, Any]] = []
    for sym in symbols:
        thesis = get_market_thesis(sym)
        if thesis is not None:
            items.append({
                "symbol": sym,
                "direction": thesis.get("action", {}).get("direction", "unknown"),
                "confidence": thesis.get("confidence", 0),
                "prob_bull": thesis.get("probabilities", {}).get("bull", 33),
                "prob_bear": thesis.get("probabilities", {}).get("bear", 33),
                "one_liner": thesis.get("action", {}).get("voice_one_liner", ""),
                "freshness": thesis.get("freshness", {}).get("overall", "missing"),
                "thesis_id": thesis.get("metadata", {}).get("thesis_id"),
            })
        else:
            items.append({
                "symbol": sym,
                "direction": "unknown",
                "confidence": 0,
                "prob_bull": 33,
                "prob_bear": 33,
                "one_liner": f"{sym} : thèse non disponible.",
                "freshness": "missing",
                "thesis_id": None,
            })
    return items


def get_market_thesis_or_build(symbol: str) -> Optional[Dict[str, Any]]:
    """Get thesis, building it if not available on disk."""
    thesis = get_market_thesis(symbol)
    if thesis is not None:
        return thesis
    try:
        from modules.market_thesis.thesis_engine import build_thesis
        from modules.market_thesis.archive import save_all
        t = build_thesis(symbol.upper())
        save_all(t)
        return t.model_dump(by_alias=True, mode="json")
    except Exception:
        return None
