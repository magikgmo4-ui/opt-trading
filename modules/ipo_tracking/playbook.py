from __future__ import annotations
from typing import Any

from .io import utc_now
from .setups import SETUPS, CATEGORIES, get_setup, Setup
from .accumulation import classify_zone, accumulation_summary


def generate_playbook(
    snapshot: dict[str, Any],
    backtest_results: list[Any] | None = None,
) -> dict[str, Any]:
    price = snapshot.get("price")
    scores = snapshot.get("scores", {})
    signals = snapshot.get("signals", [])
    acc = accumulation_summary(snapshot)
    zone = classify_zone(price)

    active_setups = _select_active_setups(snapshot, backtest_results)
    market_context = _market_context(snapshot)

    return {
        "generated_at": utc_now(),
        "symbol": snapshot.get("symbol", "SPCX"),
        "price": price,
        "ipo_price": snapshot.get("ipo_price", 135),
        "mode": "MONITOR_ONLY",

        "status": {
            "zone": {"id": zone.zone_id, "label": zone.label, "action": zone.action},
            "accumulation_score": acc.get("accumulation_score"),
            "decision": acc.get("decision"),
            "active_signals": signals,
        },

        "market_context": market_context,

        "active_setups": active_setups,

        "position_plan": {
            "zone_action": zone.action,
            "max_sizing_pct": zone.sizing_pct,
            "no_live_orders": True,
            "note": "All sizing is decision-support only. No automated execution.",
        },

        "watchlist": _build_watchlist(snapshot),
    }


def _select_active_setups(snapshot, backtest_results):
    scores = snapshot.get("scores", {})
    signals = snapshot.get("signals", [])
    price = snapshot.get("price")
    active = []

    momentum = scores.get("momentum", 0)
    trade_ready = scores.get("trade_ready", 0)
    accumulation = scores.get("accumulation", 0)

    if momentum > 0.3 and trade_ready > 0.5:
        s = get_setup("IPO_ORB_5M")
        if s:
            active.append({"setup_id": s.setup_id, "name": s.name, "category": s.category, "timeframe": s.timeframe, "active": True, "reason": "momentum + trade_ready elevated"})

    if momentum > 0.2:
        s = get_setup("GAP_AND_GO")
        if s:
            active.append({"setup_id": s.setup_id, "name": s.name, "category": s.category, "timeframe": s.timeframe, "active": True, "reason": "momentum present"})

    if accumulation > 0.5 and momentum < 0.3:
        s = get_setup("VWAP_RECLAIM")
        if s:
            active.append({"setup_id": s.setup_id, "name": s.name, "category": s.category, "timeframe": s.timeframe, "active": True, "reason": "accumulation zone, possible mean reversion"})

        s = get_setup("FVG_RECLAIM")
        if s:
            active.append({"setup_id": s.setup_id, "name": s.name, "category": s.category, "timeframe": s.timeframe, "active": True, "reason": "accumulation zone FVG opportunity"})

    for sig in signals:
        if "MOMENTUM" in sig:
            s = get_setup("HIGH_VOLUME_CONTINUATION")
            if s and s.setup_id not in [a["setup_id"] for a in active]:
                active.append({"setup_id": s.setup_id, "name": s.name, "category": s.category, "timeframe": s.timeframe, "active": True, "reason": f"signal: {sig}"})

    s = get_setup("WEEKLY_MOMENTUM")
    if s:
        active.append({"setup_id": s.setup_id, "name": s.name, "category": s.category, "timeframe": s.timeframe, "active": True, "reason": "always monitor on weekly"})

    if backtest_results:
        best_setups = [r.setup_id for r in backtest_results if hasattr(r, 'expectancy_r') and r.expectancy_r > 0.3][:3]
        for sid in best_setups:
            if sid not in [a["setup_id"] for a in active]:
                s = get_setup(sid)
                if s:
                    active.append({"setup_id": s.setup_id, "name": s.name, "category": s.category, "timeframe": s.timeframe, "active": True, "reason": "backtest-positive"})

    return active


def _market_context(snapshot):
    latest = snapshot.get("latest_events", {})
    market = latest.get("yahoo_chart", {})
    sec = latest.get("sec_edgar", {})
    news = latest.get("yahoo_news_rss", {})

    return {
        "price": snapshot.get("price"),
        "relative_volume": snapshot.get("relative_volume_estimate"),
        "gap_vs_ipo_pct": snapshot.get("gap_vs_ipo_pct"),
        "bars_count": len(market.get("bars", [])),
        "filings_count": len(sec.get("filings", [])),
        "news_articles_count": len(news.get("articles", [])),
    }


def _build_watchlist(snapshot):
    return {
        "primary": ["SPCX"],
        "correlated": ["RKLB", "ASTS", "RDW", "LUNR"],
        "etfs": ["ARKX", "UFO", "ITA"],
        "indexes": ["QQQ", "SPY", "IWM"],
        "macro": ["DXY", "TNX", "VIX"],
    }
