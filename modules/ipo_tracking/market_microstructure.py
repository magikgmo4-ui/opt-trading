from __future__ import annotations
from typing import Any
from statistics import mean, stdev

from .io import utc_now


def detect_market_regime(
    bars: list[dict[str, Any]],
    indicators: dict[str, Any],
    smart_money: dict[str, Any],
) -> dict[str, Any]:
    if len(bars) < 10:
        return {"regime": "INSUFFICIENT_DATA", "confidence": 0.0}

    closes = [_safe(b.get("close")) for b in bars if _safe(b.get("close")) is not None]
    vols = [_safe(b.get("volume")) for b in bars if _safe(b.get("volume")) is not None]
    highs = [_safe(b.get("high")) for b in bars if _safe(b.get("high")) is not None]
    lows = [_safe(b.get("low")) for b in bars if _safe(b.get("low")) is not None]

    if len(closes) < 5:
        return {"regime": "INSUFFICIENT_DATA", "confidence": 0.0}

    returns = [((closes[i] - closes[i - 1]) / max(0.01, closes[i - 1])) * 100 for i in range(1, len(closes))]
    avg_return = mean(returns) if returns else 0
    vol_returns = stdev(returns) if len(returns) > 1 else 0

    avg_vol = mean(vols) if vols else 0
    last_vol = vols[-1] if vols else 0
    vol_ratio = last_vol / avg_vol if avg_vol > 0 else 1.0

    range_vals = [highs[i] - lows[i] for i in range(len(highs)) if highs[i] and lows[i]]
    avg_range = mean(range_vals) if range_vals else 0
    last_range = range_vals[-1] if range_vals else 0
    range_expansion = last_range / avg_range if avg_range > 0 else 1.0

    fvg_bull = smart_money.get("fvg_bullish", False)
    fvg_bear = smart_money.get("fvg_bearish", False)
    bos = smart_money.get("bos", False)

    rsi = indicators.get("rsi_14") or 50
    vwap_dist = indicators.get("vwap_distance_pct") or 0

    scores = {
        "trend_day": 0.0,
        "mean_reversion_day": 0.0,
        "balanced_day": 0.0,
        "news_day": 0.0,
        "panic_day": 0.0,
        "melt_up_day": 0.0,
    }

    if abs(avg_return) > 0.05 and vol_ratio > 1.2 and range_expansion > 1.1:
        scores["trend_day"] += 0.3
    if rsi > 55 and vwap_dist > 0.3:
        scores["trend_day"] += 0.2
    if bos:
        scores["trend_day"] += 0.15

    if abs(avg_return) < 0.02 and vol_ratio < 1.1 and range_expansion < 1.05:
        scores["balanced_day"] += 0.35
    if 40 < rsi < 60 and abs(vwap_dist) < 0.3:
        scores["balanced_day"] += 0.2

    if fvg_bull and not bos and abs(avg_return) < 0.03:
        scores["mean_reversion_day"] += 0.3
    if abs(vwap_dist) > 0.5:
        scores["mean_reversion_day"] += 0.2

    if vol_ratio > 1.5:
        scores["news_day"] += 0.25
    if range_expansion > 1.3:
        scores["news_day"] += 0.15
    if abs(avg_return) > 0.03:
        scores["news_day"] += 0.15

    if avg_return < -0.08 and vol_ratio > 2.0:
        scores["panic_day"] += 0.5
    if rsi < 30 and vwap_dist < -1.0:
        scores["panic_day"] += 0.3

    if avg_return > 0.08 and vol_ratio > 2.0:
        scores["melt_up_day"] += 0.5
    if rsi > 70 and vwap_dist > 1.0:
        scores["melt_up_day"] += 0.3

    best_regime = max(scores, key=scores.get)
    best_score = scores[best_regime]

    confidence = "HIGH" if best_score > 0.4 else ("MODERATE" if best_score > 0.2 else "LOW")

    return {
        "regime": best_regime,
        "confidence": confidence,
        "score": round(best_score, 3),
        "all_scores": {k: round(v, 3) for k, v in scores.items()},
        "metrics": {
            "avg_return_pct": round(avg_return, 3),
            "volatility_pct": round(vol_returns, 3),
            "rel_volume": round(vol_ratio, 2),
            "range_expansion": round(range_expansion, 2),
            "rsi": round(rsi, 2) if rsi else None,
            "vwap_distance_pct": round(vwap_dist, 2) if vwap_dist else None,
        },
    }


def analyze_opening_auction(bars: list[dict[str, Any]], ipo_price: float) -> dict[str, Any]:
    if len(bars) < 3:
        return {"ok": False, "error": "insufficient bars"}

    first = bars[0]
    later = bars[-1] if len(bars) > 1 else bars[0]

    open_price = _safe(first.get("open")) or _safe(first.get("close"))
    gap_pct = ((open_price - ipo_price) / ipo_price * 100) if open_price and ipo_price else 0

    vol_first = _safe(first.get("volume")) or 0
    vol_avg = mean([_safe(b.get("volume")) or 0 for b in bars[:5]]) if len(bars) >= 5 else vol_first

    return {
        "ok": True,
        "open_price": open_price,
        "gap_vs_ipo_pct": round(gap_pct, 2),
        "first_candle_volume": vol_first,
        "first_candle_rel_vol": round(vol_first / max(1, vol_avg), 2),
        "auction_strength": "STRONG" if gap_pct > 2 else ("WEAK" if gap_pct < -2 else "NEUTRAL"),
        "first_candle_direction": "BULLISH" if first.get("close", 0) > first.get("open", float("inf")) else "BEARISH",
    }


def compute_volume_curve(bars: list[dict[str, Any]]) -> dict[str, Any]:
    if len(bars) < 5:
        return {"ok": False, "error": "insufficient bars"}

    vols = [_safe(b.get("volume")) or 0 for b in bars]
    avg = mean(vols)
    if avg == 0:
        return {"ok": False, "error": "no volume data"}

    quartile = len(bars) // 4
    q1_vol = mean(vols[:quartile]) if quartile > 0 else 0
    q2_vol = mean(vols[quartile:quartile*2])
    q3_vol = mean(vols[quartile*2:quartile*3])
    q4_vol = mean(vols[quartile*3:])

    shape = ""
    if q4_vol > q1_vol * 1.3:
        shape = "U_SHAPED"
    elif q1_vol > q4_vol * 1.3:
        shape = "OPEN_HEAVY"
    elif max(q1_vol, q2_vol, q3_vol, q4_vol) > avg * 1.5:
        shape = "SPIKE"
    else:
        shape = "FLAT"

    return {
        "ok": True,
        "shape": shape,
        "q1_avg_vol": round(q1_vol, 2),
        "q2_avg_vol": round(q2_vol, 2),
        "q3_avg_vol": round(q3_vol, 2),
        "q4_avg_vol": round(q4_vol, 2),
        "total_avg_vol": round(avg, 2),
        "interpretation": _volume_curve_interpretation(shape),
    }


def _volume_curve_interpretation(shape: str) -> str:
    return {
        "U_SHAPED": "Heavy open and close volume. Institutions active. Good for direction trades.",
        "OPEN_HEAVY": "Volume front-loaded. Momentum fades. Favor early exits on ORB/VWAP setups.",
        "SPIKE": "Single event drove volume. Check news. May resume trend or reverse.",
        "FLAT": "No volume conviction. Range-bound likely. Avoid momentum setups.",
    }.get(shape, "Unknown volume pattern.")


def compute_volatility_curve(bars: list[dict[str, Any]]) -> dict[str, Any]:
    if len(bars) < 5:
        return {"ok": False, "error": "insufficient bars"}

    ranges = []
    for b in bars:
        h = _safe(b.get("high"))
        l = _safe(b.get("low"))
        c = _safe(b.get("close"))
        if h and l and c:
            ranges.append((h - l) / c * 100)

    if not ranges:
        return {"ok": False, "error": "no range data"}

    avg_range = mean(ranges)
    max_range = max(ranges)

    expansion = max_range / avg_range if avg_range > 0 else 1.0

    regime = (
        "HIGH_VOLATILITY" if expansion > 2.0 else
        "ELEVATED" if expansion > 1.5 else
        "NORMAL" if expansion > 0.5 else
        "LOW_VOLATILITY"
    )

    return {
        "ok": True,
        "regime": regime,
        "avg_range_pct": round(avg_range, 2),
        "max_range_pct": round(max_range, 2),
        "range_expansion": round(expansion, 2),
    }


def _safe(v: Any) -> float | None:
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None
