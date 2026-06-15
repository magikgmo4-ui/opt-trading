"""
SPCX VWAP Analyzer — Multi-Symbol Institutional Flow Engine
GO_SPACEX_OPS_READINESS_LIVE_01

Analyzes price vs VWAP relationship for any symbol.
Produces structured output: VWAP_STATE, VWAP_SCORE, BIAS, SETUP, entry/invalidation/targets.

Rules:
  1. VWAP_STATE: BULLISH (>VWAP), BEARISH (<VWAP), NEUTRAL (within 0.25%)
  2. Quality: Reclaim, Reject, Holding Above/Below, Extended
  3. Score 0-100: relative_volume, distance%, trend, structure, ORB breakout
  4. Output: symbol, state, score, bias, setup, zones, confidence, risks, summary
"""
from __future__ import annotations
from typing import Any


def analyze_vwap(
    symbol: str,
    price: float,
    vwap: float | None = None,
    day_high: float | None = None,
    day_low: float | None = None,
    relative_volume: float | None = None,
    opening_range_high: float | None = None,
    opening_range_low: float | None = None,
    bars: list[dict] | None = None,
    smc_structures: list[dict] | None = None,
) -> dict[str, Any]:
    """Analyze price vs VWAP relationship and produce an operational reading.

    Args:
        symbol: Ticker (SPCX, NVDA, RKLB, BTCUSDT, XAUUSD, etc.)
        price: Current price
        vwap: Volume-weighted average price (None = no VWAP data)
        day_high: Session high
        day_low: Session low
        relative_volume: Volume relative to average (1.0 = normal)
        opening_range_high: ORB high
        opening_range_low: ORB low
        bars: Recent OHLCV bars for trend/structure detection
        smc_structures: SMC structure list (FVG, BOS, CHOCH, etc.)
    """
    result: dict[str, Any] = {
        "symbol": symbol,
        "price": round(price, 2),
        "vwap": round(vwap, 2) if vwap else None,
        "vwap_state": "NO_DATA",
        "vwap_score": 0,
        "bias": "NEUTRAL",
        "setup": "Aucun setup VWAP",
        "entry_zone": None,
        "invalidation": None,
        "target_1": None,
        "target_2": None,
        "confidence": 0,
        "risks": [],
        "one_line_summary": "",
    }

    if vwap is None or vwap <= 0 or price <= 0:
        result["one_line_summary"] = f"{symbol}: VWAP indisponible — analyse impossible."
        return result

    # --- 1. VWAP State ---
    distance_pct = (price - vwap) / vwap * 100
    result["distance_pct"] = round(distance_pct, 2)

    if abs(distance_pct) < 0.25:
        result["vwap_state"] = "NEUTRAL"
        result["bias"] = "Compression VWAP"
    elif price > vwap:
        result["vwap_state"] = "BULLISH"
        result["bias"] = "Achat intraday"
    else:
        result["vwap_state"] = "BEARISH"
        result["bias"] = "Distribution intraday"

    # --- 2. Quality ---
    quality = _determine_quality(distance_pct, bars or [], vwap)
    result["quality"] = quality

    # --- 3. Score ---
    score = _compute_vwap_score(
        distance_pct=distance_pct,
        relative_volume=relative_volume,
        bars=bars or [],
        vwap=vwap,
        opening_range_high=opening_range_high,
        opening_range_low=opening_range_low,
        price=price,
        smc_structures=smc_structures or [],
    )
    result["vwap_score"] = score

    # --- 4. Setup + zones ---
    _build_setup(result, score, distance_pct, price, vwap, day_high, day_low)

    # --- 5. Confidence ---
    confidence = 30.0
    if score >= 70:
        confidence = 80.0
    elif score >= 55:
        confidence = 60.0
    elif score >= 40:
        confidence = 50.0
    elif score >= 25:
        confidence = 40.0
    result["confidence"] = confidence

    # --- 6. Risks ---
    risks = []
    if distance_pct > 3:
        risks.append("Extension VWAP — risque de mean reversion")
    if distance_pct < -3:
        risks.append("Extension VWAP — risque de short squeeze")
    if relative_volume and relative_volume > 3:
        risks.append("Volume anormal — possible climax")
    if relative_volume and relative_volume < 0.5:
        risks.append("Volume faible — manque de conviction")
    if not risks:
        risks.append("Aucun risque immediat detecte")
    result["risks"] = risks

    # --- 7. One-line summary ---
    _build_summary(result, quality)

    return result


def _determine_quality(distance_pct: float, bars: list[dict], vwap: float) -> str:
    if not bars or len(bars) < 3:
        if abs(distance_pct) < 0.5:
            return "VWAP Equilibrium"
        return "Holding " + ("Above VWAP" if distance_pct > 0 else "Below VWAP")

    closes = [b.get("close") for b in bars[-10:] if b.get("close")]
    if len(closes) < 3:
        return "Holding " + ("Above VWAP" if distance_pct > 0 else "Below VWAP")

    # Detect reclaim: was below, now above
    crosses = 0
    for i in range(1, len(closes)):
        prev_above = closes[i - 1] > vwap
        curr_above = closes[i] > vwap
        if prev_above != curr_above:
            crosses += 1

    currently_above = closes[-1] > vwap
    was_below_before = any(c < vwap for c in closes[:-3])

    if crosses >= 2 and currently_above:
        return "Reclaim VWAP"
    elif crosses >= 2 and not currently_above:
        return "Reject VWAP"
    elif abs(distance_pct) > 3:
        return "Extended From VWAP"
    elif currently_above:
        return "Holding Above VWAP"
    else:
        return "Holding Below VWAP"


def _compute_vwap_score(
    distance_pct: float,
    relative_volume: float | None,
    bars: list[dict],
    vwap: float,
    opening_range_high: float | None,
    opening_range_low: float | None,
    price: float,
    smc_structures: list[dict],
) -> int:
    score = 50

    # --- Relative Volume (0-20 pts) ---
    if relative_volume is not None:
        if relative_volume > 2:
            score += 15
        elif relative_volume > 1.2:
            score += 10
        elif relative_volume > 0.8:
            score += 5
        else:
            score -= 5

    # --- VWAP Distance (0-15 pts) ---
    abs_dist = abs(distance_pct)
    if abs_dist < 0.5:
        score += 10  # tight to VWAP = equilibrium, potential breakout
    elif abs_dist < 2:
        score += 5
    elif abs_dist > 5:
        score -= 10  # overextended

    # --- Trend Alignment (0-20 pts) ---
    if bars and len(bars) >= 5:
        closes = [b.get("close") for b in bars[-5:] if b.get("close")]
        if len(closes) >= 5:
            # Simple trend: are last 3 closes moving in same direction?
            rising = all(closes[i] > closes[i - 1] for i in range(-3, 0))
            falling = all(closes[i] < closes[i - 1] for i in range(-3, 0))
            if rising and distance_pct > 0:
                score += 15  # trend aligned with VWAP position
            elif falling and distance_pct < 0:
                score += 15
            elif rising or falling:
                score += 5  # trend exists but not aligned
            else:
                score -= 5  # choppy

    # --- Market Structure / SMC (0-20 pts) ---
    has_bos = any("BOS" in s.get("type", "") for s in smc_structures)
    has_choch = any("CHOCH" in s.get("type", "") for s in smc_structures)
    has_fvg = any("FVG" in s.get("type", "") for s in smc_structures)
    if has_bos and has_choch:
        score += 15
    elif has_bos or has_choch:
        score += 10
    if has_fvg:
        score += 5

    # --- ORB Breakout (0-15 pts) ---
    if opening_range_high and opening_range_low:
        if price > opening_range_high and distance_pct > 0:
            score += 15  # breakout above ORB, above VWAP = strong
        elif price < opening_range_low and distance_pct < 0:
            score += 15
        elif price > opening_range_high or price < opening_range_low:
            score += 5  # ORB breakout but VWAP not aligned
        else:
            score += 2  # inside ORB

    # --- Strength Index (distance + volume combo) ---
    if relative_volume and relative_volume > 1.5 and abs_dist > 1:
        score += 10  # high conviction move
    elif relative_volume and relative_volume < 0.5 and abs_dist < 0.5:
        score -= 10  # low volume compression = indecision

    return max(0, min(100, score))


def _build_setup(
    result: dict,
    score: int,
    distance_pct: float,
    price: float,
    vwap: float,
    day_high: float | None,
    day_low: float | None,
) -> None:
    vwap_state = result["vwap_state"]
    symbol = result["symbol"]

    if vwap_state == "BULLISH":
        if score >= 55:
            result["setup"] = "Long bias — pullback vers VWAP"
            result["entry_zone"] = f"{vwap:.1f} - {vwap * 1.005:.1f}"
            result["invalidation"] = "Close 15m < VWAP"
            result["target_1"] = round(price * 1.01, 1)
            result["target_2"] = round(price * 1.03, 1) if day_high and price * 1.03 < day_high else round(day_high, 1) if day_high else round(price * 1.03, 1)
        else:
            result["setup"] = "Observation haussiere — attendre pullback"
            result["entry_zone"] = f"{vwap:.1f} - {vwap * 1.005:.1f}"
            result["invalidation"] = "Close 15m < VWAP"
            result["target_1"] = round(price * 1.01, 1)
            result["target_2"] = None

    elif vwap_state == "BEARISH":
        if score >= 55:
            result["setup"] = "Short bias — rally vers VWAP"
            result["entry_zone"] = f"{vwap * 0.995:.1f} - {vwap:.1f}"
            result["invalidation"] = "Close 15m > VWAP"
            result["target_1"] = round(price * 0.99, 1)
            result["target_2"] = round(price * 0.97, 1) if day_low and price * 0.97 > day_low else round(day_low, 1) if day_low else round(price * 0.97, 1)
        else:
            result["setup"] = "Observation baissiere — attendre rally"
            result["entry_zone"] = f"{vwap * 0.995:.1f} - {vwap:.1f}"
            result["invalidation"] = "Close 15m > VWAP"
            result["target_1"] = round(price * 0.99, 1)
            result["target_2"] = None

    else:  # NEUTRAL
        result["setup"] = "Compression VWAP — attendre breakout directionnel"
        result["entry_zone"] = f"{vwap * 0.995:.1f} - {vwap * 1.005:.1f}"
        result["invalidation"] = "Retour dans le range VWAP"
        result["target_1"] = round(price * 1.015, 1)
        result["target_2"] = round(price * 0.985, 1)


def _build_summary(result: dict, quality: str) -> None:
    symbol = result["symbol"]
    state = result["vwap_state"]
    price = result["price"]
    vwap = result["vwap"]
    score = result["vwap_score"]
    target1 = result["target_1"]

    if state == "BULLISH":
        result["one_line_summary"] = (
            f"{symbol} au-dessus du VWAP a {price:.1f} (VWAP {vwap:.1f}). "
            f"{quality}. Score {score}/100. "
            f"Pullback vers VWAP = zone d'achat. Objectif {target1}."
        )
    elif state == "BEARISH":
        result["one_line_summary"] = (
            f"{symbol} sous le VWAP a {price:.1f} (VWAP {vwap:.1f}). "
            f"{quality}. Score {score}/100. "
            f"Rally vers VWAP = zone de vente. Objectif {target1}."
        )
    else:
        result["one_line_summary"] = (
            f"{symbol} en equilibre VWAP a {price:.1f}. "
            f"{quality}. Score {score}/100. "
            f"Attendre breakout directionnel avant engagement."
        )


def analyze_multi_symbol(
    symbols_data: list[dict],
) -> list[dict]:
    """Analyze VWAP for multiple symbols at once."""
    results = []
    for data in symbols_data:
        result = analyze_vwap(
            symbol=data.get("symbol", "???"),
            price=float(data.get("price", 0)),
            vwap=data.get("vwap"),
            day_high=data.get("day_high"),
            day_low=data.get("day_low"),
            relative_volume=data.get("relative_volume"),
            opening_range_high=data.get("orb_high"),
            opening_range_low=data.get("orb_low"),
            bars=data.get("bars"),
            smc_structures=data.get("smc_structures"),
        )
        results.append(result)
    return results
