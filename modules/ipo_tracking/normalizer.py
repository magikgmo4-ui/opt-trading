from __future__ import annotations

from copy import deepcopy
from typing import Any

from .io import utc_now

SOURCE_NORMALIZERS: dict[str, str] = {
    "yahoo_chart": "market_data",
    "sec_edgar": "filing",
    "yahoo_news_rss": "news",
    "tradingview_webhook": "technical_alert",
    "bot_vision_adapter": "vision_context",
}


def _normalize_yahoo_chart(event: dict[str, Any]) -> dict[str, Any]:
    bars = event.get("bars") or []
    out = {
        "event_type": "market_data",
        "normalized_at": utc_now(),
        "source_event_collected_at": event.get("collected_at"),
        "symbol": event.get("symbol", "SPCX"),
        "price": event.get("regular_market_price"),
        "previous_close": event.get("previous_close"),
        "exchange": event.get("exchange"),
        "currency": event.get("currency"),
        "bars_count": len(bars),
        "bars": deepcopy(bars[-390:]),
    }
    if bars:
        closes = [b.get("close") for b in bars if isinstance(b.get("close"), (int, float))]
        vols = [b.get("volume") for b in bars if isinstance(b.get("volume"), (int, float))]
        highs = [b.get("high") for b in bars if isinstance(b.get("high"), (int, float))]
        lows = [b.get("low") for b in bars if isinstance(b.get("low"), (int, float))]
        out.update({
            "day_high": max(highs) if highs else None,
            "day_low": min(lows) if lows else None,
            "last_close": closes[-1] if closes else None,
            "volume_total": sum(vols) if vols else None,
        })
    out["ok"] = event.get("ok", False)
    return out


def _normalize_sec_edgar(event: dict[str, Any]) -> dict[str, Any]:
    filings = event.get("filings") or []
    recent = deepcopy(filings[:40])
    return {
        "event_type": "filing",
        "normalized_at": utc_now(),
        "source_event_collected_at": event.get("collected_at"),
        "company_name": event.get("company_name"),
        "tickers": event.get("tickers", []),
        "filings_count": len(filings),
        "filings": recent,
        "ok": event.get("ok", False),
    }


def _normalize_yahoo_rss(event: dict[str, Any]) -> dict[str, Any]:
    articles = event.get("articles") or []
    return {
        "event_type": "news",
        "normalized_at": utc_now(),
        "source_event_collected_at": event.get("collected_at"),
        "query": event.get("query"),
        "articles_count": len(articles),
        "articles": deepcopy(articles[:40]),
        "ok": event.get("ok", False),
    }


def _normalize_tradingview(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_type": "technical_alert",
        "normalized_at": utc_now(),
        "source_event_collected_at": event.get("collected_at"),
        "symbol": event.get("symbol", "SPCX"),
        "timeframe": event.get("timeframe"),
        "event": event.get("event"),
        "price": event.get("price"),
        "volume": event.get("volume"),
        "vwap": event.get("vwap"),
        "flags": event.get("flags", {}),
        "ok": event.get("ok", False),
    }


def _normalize_bot_vision(event: dict[str, Any]) -> dict[str, Any]:
    items = event.get("items") or []
    return {
        "event_type": "vision_context",
        "normalized_at": utc_now(),
        "source_event_collected_at": event.get("collected_at"),
        "items_count": len(items),
        "ok": event.get("ok", False),
    }


_NORMALIZE_FN = {
    "yahoo_chart": _normalize_yahoo_chart,
    "sec_edgar": _normalize_sec_edgar,
    "yahoo_news_rss": _normalize_yahoo_rss,
    "tradingview_webhook": _normalize_tradingview,
    "bot_vision_adapter": _normalize_bot_vision,
}


def normalize_event(event: dict[str, Any]) -> dict[str, Any]:
    source = event.get("source", "unknown")
    fn = _NORMALIZE_FN.get(source)
    if fn is None:
        return {
            "event_type": "unknown",
            "normalized_at": utc_now(),
            "source": source,
            "source_event_collected_at": event.get("collected_at"),
            "ok": False,
            "error": f"no normalizer for source={source}",
            "raw": deepcopy(event),
        }
    return fn(event)


def normalize_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [normalize_event(e) for e in events]


def normalized_summary(normalized: list[dict[str, Any]]) -> dict[str, Any]:
    by_type: dict[str, int] = {}
    ok_count = 0
    for e in normalized:
        t = e.get("event_type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1
        if e.get("ok"):
            ok_count += 1

    market_evts = [e for e in normalized if e.get("event_type") == "market_data"]
    filing_evts = [e for e in normalized if e.get("event_type") == "filing"]
    news_evts = [e for e in normalized if e.get("event_type") == "news"]

    return {
        "total_events": len(normalized),
        "ok_events": ok_count,
        "by_type": by_type,
        "market_data_available": len(market_evts) > 0,
        "filings_available": len(filing_evts) > 0,
        "news_available": len(news_evts) > 0,
        "bars_total": sum(e.get("bars_count", 0) for e in market_evts),
        "filings_total": sum(e.get("filings_count", 0) for e in filing_evts),
        "articles_total": sum(e.get("articles_count", 0) for e in news_evts),
    }
