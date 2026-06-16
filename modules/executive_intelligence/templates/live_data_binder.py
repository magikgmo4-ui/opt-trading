"""
Live Data Binder — connects setup cards to real data sources.

Reads from:
  - market_metrics DC views → live price, OI, funding
  - signal_event DC views → CDP triggers (vwap_reclaim, orb_break, etc.)
  - reliability engine → risk_flags enrichment
  - cross-asset leaderboard → priority sorting

No broker. No trade execution. Read-only.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ── Live price from market_metrics ─────────────────────────────────────────

def get_live_price(symbol: str) -> Optional[float]:
    """Get live price from market_metrics DC views."""
    try:
        from modules.market_thesis.config import source_path_for_symbol
        path = source_path_for_symbol("market_metrics", symbol)
        if path and path.exists():
            data = json.loads(path.read_text())
            price = data.get("last_price") or (data.get("metrics", {}) or {}).get("price")
            if isinstance(price, (int, float)):
                return float(price)
    except Exception:
        pass
    return None


def get_live_metrics(symbol: str) -> Dict[str, Any]:
    """Get live derivatives metrics for a symbol."""
    try:
        from modules.market_thesis.config import source_path_for_symbol
        path = source_path_for_symbol("market_metrics", symbol)
        if path and path.exists():
            data = json.loads(path.read_text())
            metrics = data.get("metrics", {}) or {}
            return {
                "price": data.get("last_price") or metrics.get("price"),
                "open_interest": metrics.get("open_interest"),
                "funding_rate": metrics.get("funding_rate"),
                "long_short_ratio": metrics.get("long_short_ratio"),
                "liquidations_long": metrics.get("liquidations_long"),
                "liquidations_short": metrics.get("liquidations_short"),
                "freshness": data.get("freshness_state", "unknown"),
                "ts": data.get("metrics_ts"),
            }
    except Exception:
        pass
    return {}


# ── CDP triggers from signal_event ─────────────────────────────────────────

def get_active_cdp_triggers(symbol: str) -> List[Dict[str, Any]]:
    """Get active CDP triggers for a symbol."""
    triggers: List[Dict[str, Any]] = []
    try:
        from modules.market_thesis.config import source_path_for_symbol
        path = source_path_for_symbol("signal_event", symbol)
        if path and path.exists():
            data = json.loads(path.read_text())
            events = data if isinstance(data, list) else data.get("events", [])
            for evt in events if isinstance(events, list) else []:
                event_name = evt.get("event", "")
                ts_str = evt.get("timestamp") or evt.get("written_at") or ""
                triggers.append({
                    "event": event_name,
                    "source": evt.get("source", "cdp"),
                    "price": evt.get("price"),
                    "ts": ts_str,
                    "active": True,
                })
    except Exception:
        pass
    return triggers


# ── Reliability / risk enrichment ──────────────────────────────────────────

def get_reliability_context(symbol: str) -> Dict[str, Any]:
    """Get reliability stats for risk_flags enrichment."""
    try:
        from modules.market_thesis.reliability_engine import evaluate_reliability
        rel = evaluate_reliability(symbol)
        return {
            "score": rel.reliability_score,
            "grade": rel.grade,
            "sample_size": rel.sample_size,
        }
    except Exception:
        pass
    return {}


# ── Leaderboard position ───────────────────────────────────────────────────

def get_leaderboard_position(symbol: str) -> Dict[str, Any]:
    """Get this asset's position in the cross-asset leaderboard."""
    try:
        from modules.executive_intelligence.cross_asset_engine import build_leaderboard
        board = build_leaderboard()
        for e in board:
            if e.symbol == symbol:
                return {
                    "rank": e.rank,
                    "is_leader": e.is_leader,
                    "is_laggard": e.is_laggard,
                    "momentum_score": e.momentum_score,
                }
    except Exception:
        pass
    return {"rank": 0, "is_leader": False, "is_laggard": False, "momentum_score": 0}


# ── Stale data detection ───────────────────────────────────────────────────

def check_data_freshness(symbol: str) -> Dict[str, Any]:
    """Check if data sources are stale for a symbol."""
    stale_sources = []
    now = datetime.now(timezone.utc)

    # Check market_metrics
    try:
        from modules.market_thesis.config import source_path_for_symbol
        path = source_path_for_symbol("market_metrics", symbol)
        if path and path.exists():
            age_min = (now - datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)).total_seconds() / 60
            if age_min > 30:
                stale_sources.append(f"market_metrics ({age_min:.0f}min)")
        else:
            stale_sources.append("market_metrics (missing)")
    except Exception:
        stale_sources.append("market_metrics (error)")

    # Check signal_event
    try:
        path = source_path_for_symbol("signal_event", symbol)
        if path and path.exists():
            age_min = (now - datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)).total_seconds() / 60
            if age_min > 30:
                stale_sources.append(f"CDP signals ({age_min:.0f}min)")
        else:
            stale_sources.append("CDP signals (missing)")
    except Exception:
        pass

    return {
        "is_stale": len(stale_sources) > 0,
        "stale_sources": stale_sources,
        "warning": f"Données anciennes: {', '.join(stale_sources[:3])}" if stale_sources else None,
    }


# ── Aggregate all live data ────────────────────────────────────────────────

def bind_live_data(symbol: str, thesis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Enrich setup card data with live sources.

    Returns a dict with live price, CDP triggers, reliability,
    leaderboard position, and freshness status.
    """
    live = {
        "symbol": symbol,
        "price": None,
        "metrics": {},
        "cdp_triggers": [],
        "reliability": {},
        "leaderboard": {},
        "freshness": {"is_stale": False, "stale_sources": []},
        "has_data": False,
    }

    # Live price and metrics
    live["metrics"] = get_live_metrics(symbol)
    live["price"] = live["metrics"].get("price") or get_live_price(symbol)

    # CDP triggers
    live["cdp_triggers"] = get_active_cdp_triggers(symbol)

    # Reliability
    live["reliability"] = get_reliability_context(symbol)

    # Leaderboard
    live["leaderboard"] = get_leaderboard_position(symbol)

    # Freshness
    live["freshness"] = check_data_freshness(symbol)

    # Has data flag
    live["has_data"] = bool(
        live["price"] is not None
        or thesis is not None
        or live["cdp_triggers"]
    )

    return live
