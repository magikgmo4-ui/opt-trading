from __future__ import annotations
from statistics import mean

def score_snapshot(events: list[dict], cfg: dict) -> dict:
    quote = _latest(events, "yahoo_chart") or {}
    sec = _latest(events, "sec_edgar") or {}
    news = _latest(events, "yahoo_news_rss") or {}
    tv = _latest(events, "tradingview_webhook") or {}
    bars = quote.get("bars") or []
    closes = [b.get("close") for b in bars if isinstance(b.get("close"), (int, float))]
    vols = [b.get("volume") for b in bars if isinstance(b.get("volume"), (int, float))]
    price = quote.get("regular_market_price") or (closes[-1] if closes else tv.get("price"))
    prev = quote.get("previous_close")
    ipo = ((cfg.get("asset") or {}).get("ipo_price_usd") or 135)
    gap_ipo = _pct(price, ipo)
    gap_prev = _pct(price, prev) if prev else None
    rel_vol = None
    if len(vols) > 20 and vols[-1] is not None:
        rel_vol = vols[-1] / max(1, mean(vols[-20:]))
    momentum = _clamp((gap_ipo or 0) / 25 + (rel_vol or 0) / 5, 0, 1)
    news_velocity = _clamp(len(news.get("articles") or []) / 20, 0, 1)
    sec_activity = _clamp(len(sec.get("filings") or []) / 20, 0, 1)
    flags = tv.get("flags") or {}
    smart_money = sum(0.25 for k in ["fvg", "bos", "vwap_reclaim", "orb_break"] if flags.get(k))
    risk = _clamp((gap_ipo or 0) / 60 + (news_velocity * 0.2), 0, 1)
    trade_ready = _clamp(momentum * 0.35 + news_velocity * 0.15 + smart_money * 0.35 + (1 - risk) * 0.15, 0, 1)
    accumulation = _clamp((1 - risk) * 0.4 + sec_activity * 0.1 + (0.5 if gap_ipo is not None and gap_ipo < 15 else 0.1), 0, 1)
    return {"input_class": "spacex_super_desk.v1", "symbol": (cfg.get("asset") or {}).get("primary_symbol", "SPCX"), "price": price, "ipo_price": ipo, "gap_vs_ipo_pct": gap_ipo, "gap_vs_previous_close_pct": gap_prev, "relative_volume_estimate": rel_vol, "scores": {"momentum": round(momentum, 3), "news_velocity": round(news_velocity, 3), "sec_activity": round(sec_activity, 3), "smart_money": round(smart_money, 3), "risk": round(risk, 3), "trade_ready": round(trade_ready, 3), "accumulation": round(accumulation, 3)}, "signals": _signals(gap_ipo, trade_ready, accumulation, risk, flags), "latest_events": {e.get("source", "unknown"): e for e in events[-10:]}}

def _signals(gap_ipo, trade_ready, accumulation, risk, flags):
    out = []
    if gap_ipo is not None and gap_ipo > 20:
        out.append("SPCX_MOMENTUM_EXTENDED")
    if trade_ready >= 0.7:
        out.append("SPCX_TRADE_READY_WATCH")
    if accumulation >= 0.65:
        out.append("SPCX_ACCUMULATION_ZONE_WATCH")
    if risk >= 0.7:
        out.append("SPCX_RISK_HIGH")
    for k, v in (flags or {}).items():
        if v:
            out.append("SPCX_" + k.upper())
    return out

def _latest(events, source):
    for e in reversed(events):
        if e.get("source") == source:
            return e
    return None

def _pct(a, b):
    try:
        if a is None or b in (None, 0):
            return None
        return (float(a) - float(b)) / float(b) * 100
    except Exception:
        return None

def _clamp(x, lo, hi):
    try:
        return max(lo, min(hi, float(x)))
    except Exception:
        return lo
