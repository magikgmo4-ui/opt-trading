from __future__ import annotations

from statistics import mean
from typing import Any

IPO_PRICE = 135.0


def _num(v: Any) -> float | None:
    try:
        if v is None:
            return None
        return float(v)
    except (TypeError, ValueError):
        return None


def _latest_bar(market: dict[str, Any]) -> dict[str, Any]:
    bars = market.get("bars") or []
    return bars[-1] if bars else {}


def derive_technical(market: dict[str, Any]) -> dict[str, Any]:
    bars = [b for b in (market.get("bars") or []) if _num(b.get("close")) is not None]
    latest = bars[-1] if bars else {}
    close = _num(latest.get("close")) or _num(market.get("regular_market_price"))
    prev = _num(market.get("previous_close"))
    highs = [_num(b.get("high")) for b in bars if _num(b.get("high")) is not None]
    lows = [_num(b.get("low")) for b in bars if _num(b.get("low")) is not None]
    vols = [_num(b.get("volume")) for b in bars if _num(b.get("volume")) is not None]
    day_high = max(highs) if highs else None
    day_low = min(lows) if lows else None
    avg_vol = mean(vols[-30:]) if len(vols) >= 2 else None
    last_vol = vols[-1] if vols else None
    rel_vol = (last_vol / avg_vol) if avg_vol and last_vol is not None else None
    ipo_gap_pct = ((close - IPO_PRICE) / IPO_PRICE * 100.0) if close else None
    prev_gap_pct = ((close - prev) / prev * 100.0) if close and prev else None
    return {
        "price": close,
        "previous_close": prev,
        "day_high": day_high,
        "day_low": day_low,
        "relative_volume": rel_vol,
        "ipo_gap_pct": ipo_gap_pct,
        "prev_gap_pct": prev_gap_pct,
        "bars_count": len(bars),
    }


def detect_smart_money(market: dict[str, Any]) -> dict[str, Any]:
    bars = market.get("bars") or []
    fvg_bullish = False
    fvg_bearish = False
    if len(bars) >= 3:
        a, _, c = bars[-3], bars[-2], bars[-1]
        a_high = _num(a.get("high")); a_low = _num(a.get("low")); c_high = _num(c.get("high")); c_low = _num(c.get("low"))
        if a_high is not None and c_low is not None and c_low > a_high:
            fvg_bullish = True
        if a_low is not None and c_high is not None and c_high < a_low:
            fvg_bearish = True
    tech = derive_technical(market)
    price = tech.get("price")
    day_high = tech.get("day_high")
    day_low = tech.get("day_low")
    return {
        "fvg_bullish": fvg_bullish,
        "fvg_bearish": fvg_bearish,
        "bos_candidate": bool(price and day_high and price >= day_high),
        "liquidity_sweep_candidate": bool(price and day_low and price <= day_low),
        "note": "Derived from provider OHLCV. TradingView alert data should override when available.",
    }


def score_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    market = snapshot.get("market", {}) or {}
    tech = snapshot.setdefault("technical", derive_technical(market))
    smc = snapshot.setdefault("smart_money", detect_smart_money(market))
    news = snapshot.get("news", {}) or {}
    sec = snapshot.get("sec", {}) or {}

    price = tech.get("price")
    ipo_gap = tech.get("ipo_gap_pct")
    rel_vol = tech.get("relative_volume")
    news_count = int(news.get("count") or len(news.get("articles") or []))
    filing_count = len(sec.get("recent_filings") or [])

    momentum = 0
    if price and price > IPO_PRICE:
        momentum += 25
    if ipo_gap is not None:
        momentum += max(0, min(25, ipo_gap))
    if rel_vol:
        momentum += max(0, min(25, (rel_vol - 1) * 10))
    if smc.get("fvg_bullish") or smc.get("bos_candidate"):
        momentum += 15

    news_score = min(100, news_count * 8 + filing_count * 3)
    risk_score = 35
    if ipo_gap is not None and ipo_gap > 50:
        risk_score += 25
    if rel_vol and rel_vol > 5:
        risk_score += 15
    if smc.get("fvg_bearish"):
        risk_score += 10
    risk_score = min(100, risk_score)

    trade_ready = max(0, min(100, momentum * 0.65 + news_score * 0.20 - risk_score * 0.15 + 20))
    accumulation = max(0, min(100, 75 - (ipo_gap or 0) * 0.8 - risk_score * 0.15 + news_score * 0.1))

    setup = "WATCH"
    if trade_ready >= 85:
        setup = "A_PLUS_MOMENTUM"
    elif trade_ready >= 75:
        setup = "A_MOMENTUM"
    elif accumulation >= 70:
        setup = "ACCUMULATION_CANDIDATE"

    return {
        "momentum_score": round(momentum, 2),
        "news_velocity_score": round(news_score, 2),
        "risk_score": round(risk_score, 2),
        "trade_ready_score": round(trade_ready, 2),
        "accumulation_score": round(accumulation, 2),
        "selected_setup": setup,
        "monitor_only": True,
    }


def derive_alerts(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    alerts = []
    scores = snapshot.get("scores", {})
    tech = snapshot.get("technical", {})
    smc = snapshot.get("smart_money", {})
    if scores.get("trade_ready_score", 0) >= 75:
        alerts.append({"event": "SPCX_TRADE_READY_HIGH", "severity": "high", "score": scores.get("trade_ready_score")})
    if scores.get("accumulation_score", 0) >= 70:
        alerts.append({"event": "SPCX_ACCUMULATION_ZONE", "severity": "medium", "score": scores.get("accumulation_score")})
    if smc.get("fvg_bullish"):
        alerts.append({"event": "SPCX_FVG_BULLISH", "severity": "medium"})
    if smc.get("fvg_bearish"):
        alerts.append({"event": "SPCX_FVG_BEARISH", "severity": "medium"})
    if tech.get("ipo_gap_pct") is not None and tech.get("ipo_gap_pct") > 20:
        alerts.append({"event": "SPCX_IPO_GAP_STRONG", "severity": "high", "ipo_gap_pct": tech.get("ipo_gap_pct")})
    return alerts
