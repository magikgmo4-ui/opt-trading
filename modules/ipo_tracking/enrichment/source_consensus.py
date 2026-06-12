from __future__ import annotations
from statistics import mean
from typing import Any


SOURCE_WEIGHTS = {
    "yahoo_chart": 0.25,
    "tradingview_webhook": 0.25,
    "bot_vision_adapter": 0.15,
    "sec_edgar": 0.10,
    "yahoo_news_rss": 0.10,
    "desk_pro_latest": 0.05,
    "google_sheets_latest": 0.05,
    "telegram_signal": 0.05,
}

STALE_SECONDS = {
    "yahoo_chart": 300,
    "tradingview_webhook": 600,
    "bot_vision_adapter": 1200,
    "sec_edgar": 86400,
    "yahoo_news_rss": 3600,
    "desk_pro_latest": 600,
    "google_sheets_latest": 3600,
    "telegram_signal": 1800,
}


def compute_consensus(
    events: list[dict[str, Any]],
    snapshot: dict[str, Any],
    *,
    now: str | None = None,
) -> dict[str, Any]:
    from datetime import datetime, timezone, timedelta
    if now is None:
        now = datetime.now(timezone.utc).isoformat()

    prices: dict[str, float] = {}
    volumes: dict[str, float] = {}
    staleness: dict[str, bool] = {}
    missing: list[str] = []

    now_dt = datetime.fromisoformat(now.replace("Z", "+00:00"))

    for e in events:
        source = e.get("source", "unknown")
        collected = e.get("collected_at")
        is_stale = True

        if collected and source in STALE_SECONDS:
            try:
                col_dt = datetime.fromisoformat(collected.replace("Z", "+00:00"))
                is_stale = (now_dt - col_dt).total_seconds() > STALE_SECONDS.get(source, 600)
            except (ValueError, TypeError):
                pass

        if source == "yahoo_chart":
            p = e.get("regular_market_price")
            if p is not None:
                prices[source] = float(p)
            v = e.get("volume")
            if v is not None:
                volumes[source] = float(v)
        elif source == "tradingview_webhook":
            p = e.get("price")
            if p is not None:
                prices[source] = float(p)
            v = e.get("volume")
            if v is not None:
                volumes[source] = float(v)
        elif source == "bot_vision_adapter":
            for item in e.get("items", []):
                preview = item.get("json_preview")
                if preview and isinstance(preview, dict):
                    mp = preview.get("regular_market_price")
                    if mp is not None:
                        prices[source] = float(mp)
                        break

        staleness[source] = is_stale

    for src in SOURCE_WEIGHTS:
        if src not in prices and src not in ["sec_edgar", "yahoo_news_rss", "desk_pro_latest", "google_sheets_latest", "telegram_signal"]:
            missing.append(src)

    consensus_price = mean(prices.values()) if prices else snapshot.get("price")
    consensus_volume = mean(volumes.values()) if volumes else None

    price_deviations = {}
    if len(prices) > 1:
        avg_p = mean(prices.values())
        for src, p in prices.items():
            price_deviations[src] = round(abs(p - avg_p) / avg_p * 100, 3) if avg_p > 0 else 0.0

    disagreement = 0.0
    if len(prices) >= 2:
        pvals = list(prices.values())
        avg_p = mean(pvals)
        disagreement = round(sum(abs(p - avg_p) / avg_p * 100 for p in pvals) / len(pvals), 2) if avg_p > 0 else 0.0

    trusted_sources = [s for s in prices if not staleness.get(s, True)]
    stale_sources = [s for s, v in staleness.items() if v and s in prices]
    missing_sources = [s for s in SOURCE_WEIGHTS if s not in prices and s not in missing]

    weighted_trust = sum(SOURCE_WEIGHTS.get(s, 0) for s in trusted_sources)

    return {
        "consensus_price": round(consensus_price, 2) if consensus_price else None,
        "consensus_volume": round(consensus_volume, 2) if consensus_volume else None,
        "source_count": len(prices),
        "trusted_source_count": len(trusted_sources),
        "source_disagreement_score": disagreement,
        "price_deviations": price_deviations,
        "stale_source_flags": stale_sources,
        "missing_source_flags": missing_sources + missing,
        "trusted_sources": trusted_sources,
        "weighted_trust_score": round(weighted_trust, 3),
        "source_prices": {s: round(p, 2) for s, p in prices.items()},
    }
