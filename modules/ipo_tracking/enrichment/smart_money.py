from __future__ import annotations
from typing import Any


def detect_fvg(bars: list[dict[str, Any]]) -> dict[str, Any]:
    if len(bars) < 3:
        return {"bullish": False, "bearish": False, "zones": []}

    zones = []
    for i in range(2, len(bars)):
        a, b, c = bars[i - 2], bars[i - 1], bars[i]
        a_h, a_l = _f(a.get("high")), _f(a.get("low"))
        b_h, b_l = _f(b.get("high")), _f(b.get("low"))
        c_h, c_l = _f(c.get("high")), _f(c.get("low"))

        if None in (a_h, a_l, c_h, c_l):
            continue

        if c_l > a_h:
            gap_pct = (c_l - a_h) / a_h * 100
            zones.append({"type": "bullish", "top": c_l, "bottom": a_h, "gap_pct": round(gap_pct, 2), "index": i, "filled": False})

        if c_h < a_l:
            gap_pct = (a_l - c_h) / a_l * 100
            zones.append({"type": "bearish", "top": a_l, "bottom": c_h, "gap_pct": round(gap_pct, 2), "index": i, "filled": False})

    last_close = _f(bars[-1].get("close")) if bars else None
    for z in zones:
        if last_close and z["type"] == "bullish" and last_close <= z["top"] and last_close >= z["bottom"]:
            z["filled"] = True
        if last_close and z["type"] == "bearish" and last_close >= z["bottom"] and last_close <= z["top"]:
            z["filled"] = True

    bullish = any(z["type"] == "bullish" for z in zones[-3:])
    bearish = any(z["type"] == "bearish" for z in zones[-3:])

    return {"bullish": bullish, "bearish": bearish, "zones": zones[-5:], "active_count": len(zones)}


def detect_order_blocks(bars: list[dict[str, Any]]) -> dict[str, Any]:
    if len(bars) < 3:
        return {"bullish_ob": None, "bearish_ob": None}

    ob_bullish = None
    ob_bearish = None
    for i in range(1, len(bars) - 1):
        b = bars[i]
        prev = bars[i - 1]
        nxt = bars[i + 1]
        b_o, b_c, b_h, b_l = _f(b.get("open")), _f(b.get("close")), _f(b.get("high")), _f(b.get("low"))
        n_c = _f(nxt.get("close"))

        if None in (b_o, b_c, n_c):
            continue

        if b_c > b_o and n_c < b_c:
            ob_bearish = {"price": b_c, "index": i, "type": "bearish"}
        if b_c < b_o and n_c > b_c:
            ob_bullish = {"price": b_c, "index": i, "type": "bullish"}

    last_close = _f(bars[-1].get("close")) if bars else None
    ob_bullish_active = ob_bullish and last_close and last_close > ob_bullish["price"] * 0.995
    ob_bearish_active = ob_bearish and last_close and last_close < ob_bearish["price"] * 1.005

    return {
        "bullish_ob": {"price": round(ob_bullish["price"], 2), "index": ob_bullish["index"], "active": ob_bullish_active} if ob_bullish else None,
        "bearish_ob": {"price": round(ob_bearish["price"], 2), "index": ob_bearish["index"], "active": ob_bearish_active} if ob_bearish else None,
    }


def detect_liquidity_sweeps(bars: list[dict[str, Any]]) -> dict[str, Any]:
    if len(bars) < 10:
        return {"high_sweep": False, "low_sweep": False}

    lookback = min(20, len(bars) // 2)
    recent = bars[-lookback:]
    highs = [_f(r.get("high")) for r in recent if _f(r.get("high")) is not None]
    lows = [_f(r.get("low")) for r in recent if _f(r.get("low")) is not None]

    if not highs or not lows:
        return {"high_sweep": False, "low_sweep": False}

    max_high = max(highs)
    min_low = min(lows)

    recent_highs = [_f(r.get("high")) for r in bars[-3:] if _f(r.get("high")) is not None]
    recent_lows = [_f(r.get("low")) for r in bars[-3:] if _f(r.get("low")) is not None]

    high_sweep = any(h > max_high * 0.995 for h in recent_highs) if recent_highs else False
    low_sweep = any(l < min_low * 1.005 for l in recent_lows) if recent_lows else False

    return {"high_sweep": high_sweep, "low_sweep": low_sweep, "lookback": lookback}


def detect_bos_choch(bars: list[dict[str, Any]]) -> dict[str, Any]:
    if len(bars) < 5:
        return {"bos": False, "choch": False}

    swing_highs = []
    swing_lows = []
    for i in range(2, len(bars) - 2):
        h = _f(bars[i].get("high"))
        l = _f(bars[i].get("low"))
        if h is None or l is None:
            continue
        if all(h >= _f(bars[j].get("high")) for j in range(i - 2, i + 3) if _f(bars[j].get("high")) is not None):
            swing_highs.append((i, h))
        if all(l <= _f(bars[j].get("low")) for j in range(i - 2, i + 3) if _f(bars[j].get("low")) is not None):
            swing_lows.append((i, l))

    last_close = _f(bars[-1].get("close")) if bars else None
    bos = False
    choch = False

    if len(swing_highs) >= 2:
        prev_h = swing_highs[-2][1]
        latest_h = swing_highs[-1][1]
        if last_close and last_close > prev_h:
            bos = True
        if latest_h < prev_h:
            choch = True

    if len(swing_lows) >= 2:
        prev_l = swing_lows[-2][1]
        latest_l = swing_lows[-1][1]
        if last_close and last_close < prev_l:
            bos = True
        if latest_l > prev_l:
            choch = True

    return {"bos": bos, "choch": choch, "swing_highs": len(swing_highs), "swing_lows": len(swing_lows)}


def detect_equal_highs_lows(bars: list[dict[str, Any]], tolerance_pct: float = 0.05) -> dict[str, Any]:
    if len(bars) < 5:
        return {"equal_highs": False, "equal_lows": False}

    highs = [_f(r.get("high")) for r in bars if _f(r.get("high")) is not None]
    lows = [_f(r.get("low")) for r in bars if _f(r.get("low")) is not None]

    eq_highs = False
    eq_lows = False

    for i in range(len(highs)):
        for j in range(i + 1, len(highs)):
            if abs(highs[i] - highs[j]) / max(highs[i], 1) * 100 <= tolerance_pct:
                eq_highs = True
                break

    for i in range(len(lows)):
        for j in range(i + 1, len(lows)):
            if abs(lows[i] - lows[j]) / max(lows[i], 1) * 100 <= tolerance_pct:
                eq_lows = True
                break

    return {"equal_highs": eq_highs, "equal_lows": eq_lows, "tolerance_pct": tolerance_pct}


def detect_premium_discount(bars: list[dict[str, Any]]) -> dict[str, Any]:
    if len(bars) < 20:
        return {"regime": "mid_range", "position_pct": 50.0}

    highs = [_f(r.get("high")) for r in bars[-20:] if _f(r.get("high")) is not None]
    lows = [_f(r.get("low")) for r in bars[-20:] if _f(r.get("low")) is not None]
    last_close = _f(bars[-1].get("close")) if bars else None

    if not highs or not lows or last_close is None:
        return {"regime": "mid_range", "position_pct": 50.0}

    max_h = max(highs)
    min_l = min(lows)
    total_range = max_h - min_l
    if total_range <= 0:
        return {"regime": "mid_range", "position_pct": 50.0}

    position_pct = (last_close - min_l) / total_range * 100

    if position_pct >= 70:
        regime = "premium"
    elif position_pct <= 30:
        regime = "discount"
    else:
        regime = "mid_range"

    return {"regime": regime, "position_pct": round(position_pct, 1), "max_high": max_h, "min_low": min_l}


def compute_smart_money(bars: list[dict[str, Any]]) -> dict[str, Any]:
    fvg = detect_fvg(bars)
    ob = detect_order_blocks(bars)
    liq = detect_liquidity_sweeps(bars)
    bc = detect_bos_choch(bars)
    eq = detect_equal_highs_lows(bars)
    pd = detect_premium_discount(bars)

    smc_score = 0.0
    if fvg["bullish"]:
        smc_score += 0.2
    if fvg["bearish"]:
        smc_score -= 0.15
    if ob.get("bullish_ob") and ob["bullish_ob"].get("active"):
        smc_score += 0.15
    if ob.get("bearish_ob") and ob["bearish_ob"].get("active"):
        smc_score -= 0.1
    if liq["high_sweep"]:
        smc_score += 0.1
    if liq["low_sweep"]:
        smc_score -= 0.1
    if bc["bos"]:
        smc_score += 0.2
    if bc["choch"]:
        smc_score += 0.15
    if pd["regime"] == "premium":
        smc_score -= 0.1
    if pd["regime"] == "discount":
        smc_score += 0.15

    return {
        "fvg": fvg,
        "order_blocks": ob,
        "liquidity_sweeps": liq,
        "bos_choch": bc,
        "equal_highs_lows": eq,
        "premium_discount": pd,
        "smc_score": round(max(-1.0, min(1.0, smc_score)), 3),
        "smc_bias": "bullish" if smc_score > 0.15 else ("bearish" if smc_score < -0.15 else "neutral"),
    }


def _f(v: Any) -> float | None:
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None
