from __future__ import annotations
from statistics import mean
from typing import Any


SOURCE_WEIGHTS = {
    "nasdaq_quote": 0.30,
    "yahoo_chart": 0.25,
    "tradingview_webhook": 0.25,
    "bot_vision_adapter": 0.15,
    "sec_edgar": 0.10,
    "yahoo_news_rss": 0.10,
    "desk_pro_latest": 0.05,
    "google_sheets_latest": 0.05,
    "telegram_signal": 0.05,
}

PRICE_WEIGHTS = {
    "nasdaq_quote": 0.32,
    "yahoo_chart": 0.26,
    "tradingview_webhook": 0.26,
    "bot_vision_adapter": 0.16,
}

INFO_WEIGHTS = {
    "sec_edgar": 0.29,
    "yahoo_news_rss": 0.29,
    "desk_pro_latest": 0.14,
    "google_sheets_latest": 0.14,
    "telegram_signal": 0.14,
}

STALE_SECONDS = {
    "nasdaq_quote": 120,
    "yahoo_chart": 300,
    "tradingview_webhook": 600,
    "bot_vision_adapter": 1200,
    "sec_edgar": 86400,
    "yahoo_news_rss": 3600,
    "desk_pro_latest": 600,
    "google_sheets_latest": 3600,
    "telegram_signal": 1800,
}

PRICE_SOURCE_ORDER = [
    "nasdaq_quote",
    "yahoo_chart",
    "tradingview_webhook",
    "bot_vision_adapter",
]

PRICE_PRODUCING_SOURCES = set(PRICE_SOURCE_ORDER)
INFO_SOURCES = {"sec_edgar", "yahoo_news_rss", "desk_pro_latest", "google_sheets_latest", "telegram_signal"}


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
    price_statuses: dict[str, str] = {}
    info_presence: dict[str, bool] = {}

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

        if source == "nasdaq_quote":
            p = e.get("regular_market_price")
            if p is not None:
                prices[source] = float(p)
            v = e.get("volume")
            if v is not None:
                volumes[source] = float(v)
            price_statuses[source] = e.get("price_status", "missing")

        elif source == "yahoo_chart":
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

        elif source in INFO_SOURCES:
            info_presence[source] = e.get("ok", False) and not is_stale

        staleness[source] = is_stale

    nasdaq_has_price = "nasdaq_quote" in prices and prices["nasdaq_quote"] is not None
    nasdaq_price_status = price_statuses.get("nasdaq_quote", "")
    nasdaq_no_price = nasdaq_price_status in ("NO_PRICE_AVAILABLE_YET", "PRICE_NOT_AVAILABLE_YET", "WAITING_FIRST_PRINT", "missing")

    any_source_has_bars = False
    for e in events:
        src = e.get("source", "")
        if src in ("yahoo_chart", "tradingview_webhook", "bot_vision_adapter"):
            bars = e.get("bars", [])
            if bars and len(bars) > 0:
                for b in bars:
                    if isinstance(b, dict) and b.get("volume", 0) and b.get("volume", 0) > 0:
                        any_source_has_bars = True
                        break
            if any_source_has_bars:
                break

    if not nasdaq_has_price and nasdaq_no_price and not any_source_has_bars:
        for src in list(prices.keys()):
            if src != "nasdaq_quote":
                del prices[src]
        for src in list(staleness.keys()):
            if src != "nasdaq_quote":
                staleness[src] = True

    missing = []
    for src in SOURCE_WEIGHTS:
        if src not in prices and src not in INFO_SOURCES:
            missing.append(src)

    consensus_price = _priority_weighted_price(prices) or snapshot.get("price")
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

    if nasdaq_no_price and not any_source_has_bars:
        trusted_sources = []
    else:
        trusted_sources = [s for s in prices if not staleness.get(s, True)]
    stale_sources = [s for s, v in staleness.items() if v and s in prices]

    all_missing = [s for s in SOURCE_WEIGHTS if s not in prices and s not in INFO_SOURCES]
    all_missing.extend(missing)

    price_trust = sum(PRICE_WEIGHTS.get(s, 0) for s in trusted_sources)
    info_trust = sum(INFO_WEIGHTS.get(s, 0) for s, ok in info_presence.items() if ok)

    market_phase = _determine_market_phase(events)
    best_price_status = _best_price_status(price_statuses, prices)

    return {
        "consensus_price": round(consensus_price, 2) if consensus_price else None,
        "consensus_volume": round(consensus_volume, 2) if consensus_volume else None,
        "source_count": len(prices),
        "trusted_source_count": len(trusted_sources),
        "source_disagreement_score": disagreement,
        "price_deviations": price_deviations,
        "stale_source_flags": stale_sources,
        "missing_source_flags": list(set(all_missing)),
        "trusted_sources": trusted_sources,
        "weighted_trust_score": round(min(1.0, price_trust), 3),
        "price_trust": round(price_trust, 3),
        "info_trust": round(info_trust, 3),
        "source_prices": {s: round(p, 2) for s, p in prices.items()},
        "market_phase": market_phase,
        "price_status": best_price_status,
    }


def _priority_weighted_price(prices: dict[str, float]) -> float | None:
    if not prices:
        return None
    for src in PRICE_SOURCE_ORDER:
        if src in prices and prices[src] is not None:
            w = PRICE_WEIGHTS.get(src, 0)
            weighted_sum = prices[src] * w
            total_weight = w
            for other_src, p in prices.items():
                if other_src != src:
                    ow = PRICE_WEIGHTS.get(other_src, 0) * 0.5
                    weighted_sum += p * ow
                    total_weight += ow
            return weighted_sum / total_weight if total_weight > 0 else prices[src]
    return mean(prices.values())


def _determine_market_phase(events: list[dict[str, Any]]) -> str:
    for e in events:
        if e.get("source") == "nasdaq_quote":
            return e.get("market_phase", "unknown")
    for e in events:
        if e.get("source") == "yahoo_chart":
            session = e.get("market_phase", "unknown")
            if session != "unknown":
                return session
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    h = now.hour + now.minute / 60.0
    wd = now.weekday()
    if wd >= 5:
        return "closed"
    if h < 13.416:
        return "preopen"
    if h < 14.5:
        return "regular"
    if h < 20.0:
        return "after_hours"
    return "closed"


def _best_price_status(price_statuses: dict[str, str], prices: dict[str, float]) -> str:
    if not prices:
        return "missing"
    if prices:
        return "live"
    return "missing"
