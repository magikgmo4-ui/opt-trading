from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from modules.ipo_tracking.collectors.news_rss import fetch_yahoo_rss
from modules.ipo_tracking.collectors.sec_edgar import fetch_sec_submissions
from modules.ipo_tracking.collectors.yahoo_public import fetch_chart
from modules.ipo_tracking.config import load_config, resolve_paths
from modules.ipo_tracking.integrations.data_center import write_spacex_view
from modules.ipo_tracking.scoring.spacex_score import derive_alerts, derive_technical, detect_smart_money, score_snapshot
from modules.ipo_tracking.storage.jsonl_store import append_jsonl, atomic_write_json


def _offline_market(symbol: str = "SPCX") -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "ok": False,
        "provider": "offline_stub",
        "symbol": symbol,
        "produced_at": now,
        "regular_market_price": None,
        "previous_close": None,
        "bars": [],
        "note": "No live provider data available. Dry-run preserved.",
    }


def collect_once(*, offline_ok: bool = True, config_path: str | None = None) -> dict[str, Any]:
    config = load_config(config_path)
    paths = resolve_paths(config)
    asset = config.get("asset", {})
    symbol = asset.get("primary_symbol", "SPCX")
    cik = asset.get("sec_cik", "0001181412")
    produced_at = datetime.now(timezone.utc).isoformat()

    market = fetch_chart(symbol=symbol)
    if not market.get("ok") and offline_ok:
        market = _offline_market(symbol)

    # Correlations are best effort and limited to a few public requests.
    correlated = {}
    for sym in (config.get("watchlists", {}).get("correlated_equities", []) or [])[:8]:
        correlated[sym] = fetch_chart(symbol=sym, range_="1d", interval="5m")

    sec = fetch_sec_submissions(cik=str(cik))
    news = fetch_yahoo_rss("SpaceX OR SPCX OR Starlink OR Starship")

    snapshot: dict[str, Any] = {
        "schema": "spacex_super_desk_snapshot.v1",
        "produced_at": produced_at,
        "mode": "monitor_only",
        "asset": {
            "symbol": symbol,
            "company": asset.get("company"),
            "ipo_price_usd": asset.get("ipo_price_usd"),
            "exchange": asset.get("exchange"),
            "sec_cik": cik,
        },
        "market": market,
        "correlated": correlated,
        "sec": sec,
        "news": news,
        "coinglass_context": {"available": False, "mode": "market_risk_proxy", "note": "Use existing Coinglass vision outputs when present."},
        "bot_vision": {"profile_path": config.get("sources", {}).get("bot_vision_headless", {}).get("profile_path")},
        "institutional": {"available": False, "pending": ["etf_holdings", "analyst_targets", "13f", "lockup"]},
    }
    snapshot["technical"] = derive_technical(market)
    snapshot["smart_money"] = detect_smart_money(market)
    snapshot["scores"] = score_snapshot(snapshot)
    snapshot["alerts"] = derive_alerts(snapshot)

    append_jsonl(paths.raw_jsonl, snapshot)
    atomic_write_json(paths.latest_snapshot, snapshot)
    write_spacex_view(paths.data_center_view, snapshot)
    return {
        "ok": True,
        "snapshot": snapshot,
        "paths": {
            "raw_jsonl": str(paths.raw_jsonl),
            "latest_snapshot": str(paths.latest_snapshot),
            "data_center_view": str(paths.data_center_view),
        },
    }
