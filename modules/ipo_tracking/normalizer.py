from __future__ import annotations

from copy import deepcopy
from typing import Any

from .io import utc_now

SOURCE_NORMALIZERS: dict[str, str] = {
    "nasdaq_quote": "market_data",
    "yahoo_chart": "market_data",
    "sec_edgar": "filing",
    "yahoo_news_rss": "news",
    "tradingview_webhook": "technical_alert",
    "bot_vision_adapter": "vision_context",
    "desk_pro_latest": "dashboard",
    "google_sheets_latest": "sheets",
    "telegram_signal": "signal",
}


def _normalize_nasdaq_quote(event: dict[str, Any]) -> dict[str, Any]:
    bars = event.get("bars") or []
    out = {
        "event_type": "market_data",
        "normalized_at": utc_now(),
        "source_event_collected_at": event.get("collected_at"),
        "symbol": event.get("symbol", "SPCX"),
        "price": event.get("regular_market_price"),
        "previous_close": event.get("previous_close"),
        "volume": event.get("volume"),
        "exchange": event.get("exchange"),
        "currency": event.get("currency"),
        "bars_count": len(bars),
        "bars": deepcopy(bars[-390:]),
        "market_phase": event.get("market_phase", "unknown"),
        "price_status": event.get("price_status", "missing"),
        "ipo_cross_state": event.get("ipo_cross_state", "unknown"),
        "halt_status": event.get("halt_status"),
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
        "market_phase": event.get("market_phase", _default_market_phase()),
        "price_status": _price_status_from_event(event),
        "ipo_cross_state": "unknown",
        "halt_status": None,
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
        "spcx_capture_count": event.get("spcx_capture_count", 0),
        "spcx_capture_map": event.get("spcx_capture_map", {}),
        "comparable_count": event.get("comparable_count", 0),
        "comparable_map": event.get("comparable_map", {}),
        "ok": event.get("ok", False),
    }


def _normalize_desk_pro(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_type": "dashboard",
        "normalized_at": utc_now(),
        "source_event_collected_at": event.get("collected_at"),
        "symbol": event.get("symbol", "SPCX"),
        "signals_count": event.get("signals_count", 0),
        "signals": event.get("signals", []),
        "freshness_seconds": event.get("freshness_seconds"),
        "ok": event.get("ok", False),
    }


def _normalize_google_sheets(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_type": "sheets",
        "normalized_at": utc_now(),
        "source_event_collected_at": event.get("collected_at"),
        "symbol": event.get("symbol", "SPCX"),
        "rows_count": event.get("rows_count", 0),
        "sheets_push": event.get("sheets_push", {}),
        "freshness_seconds": event.get("freshness_seconds"),
        "ok": event.get("ok", False),
    }


def _normalize_telegram_signal(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_type": "signal",
        "normalized_at": utc_now(),
        "source_event_collected_at": event.get("collected_at"),
        "symbol": event.get("symbol", "SPCX"),
        "signals_count": event.get("signals_count", 0),
        "signals": event.get("signals", []),
        "alert_sent": event.get("alert_sent", False),
        "freshness_seconds": event.get("freshness_seconds"),
        "ok": event.get("ok", False),
    }


def _price_status_from_event(event: dict[str, Any]) -> str:
    price = event.get("regular_market_price")
    if price is not None:
        return "live"
    bars = event.get("bars") or []
    if bars and any(b.get("close") is not None for b in bars):
        return "live"
    if event.get("ok"):
        return "WAITING_FIRST_PRINT"
    return "missing"


def _default_market_phase() -> str:
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


_NORMALIZE_FN = {
    "nasdaq_quote": _normalize_nasdaq_quote,
    "yahoo_chart": _normalize_yahoo_chart,
    "sec_edgar": _normalize_sec_edgar,
    "yahoo_news_rss": _normalize_yahoo_rss,
    "tradingview_webhook": _normalize_tradingview,
    "bot_vision_adapter": _normalize_bot_vision,
    "desk_pro_latest": _normalize_desk_pro,
    "google_sheets_latest": _normalize_google_sheets,
    "telegram_signal": _normalize_telegram_signal,
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

    market_phase = "unknown"
    price_status = "missing"
    for me in market_evts:
        mp = me.get("market_phase", "unknown")
        if mp != "unknown":
            market_phase = mp
        ps = me.get("price_status", "missing")
        if ps == "live" or (ps != "missing" and price_status == "missing"):
            price_status = ps

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
        "market_phase": market_phase,
        "price_status": price_status,
    }
