"""
Narrative generator — PR3.

Produces French-language narratives for each section of the thesis.
Deterministic rule-based: no LLM, no randomness.
Always returns a non-empty string (fallback if data insufficient).
"""

from __future__ import annotations

from typing import Any, List, Optional


def context_narrative(
    macro_regime: str = "unknown",
    dxy_trend: str = "unknown",
    vix_state: str = "unknown",
    spy_trend: str = "unknown",
    market_phase: str = "unknown",
    fear_greed: Optional[int] = None,
) -> str:
    """Generate French narrative for macro context."""
    parts: List[str] = []
    regime_map = {
        "risk_on": "risk-on",
        "risk_off": "risk-off",
        "neutral": "neutre",
    }
    dxy_map = {
        "bullish": "DXY haussier",
        "bearish": "DXY baissier",
        "neutral": "DXY stable",
    }
    vix_map = {
        "low": "VIX bas",
        "normal": "VIX normal",
        "elevated": "VIX élevé",
        "high": "VIX très élevé",
    }
    spy_map = {
        "bullish": "SPY haussier",
        "bearish": "SPY baissier",
        "neutral": "SPY neutre",
    }
    phase_map = {
        "accumulation": "accumulation",
        "markup": "hausse (markup)",
        "distribution": "distribution",
        "markdown": "baisse (markdown)",
    }

    regime_fr = regime_map.get(macro_regime, macro_regime)
    if macro_regime != "unknown":
        parts.append(f"Régime {regime_fr}")

    dxy_fr = dxy_map.get(dxy_trend, "")
    if dxy_trend != "unknown" and dxy_fr:
        parts.append(dxy_fr)

    vix_fr = vix_map.get(vix_state, "")
    if vix_state != "unknown" and vix_fr:
        parts.append(vix_fr)

    spy_fr = spy_map.get(spy_trend, "")
    if spy_trend != "unknown" and spy_fr:
        parts.append(spy_fr)

    phase_fr = phase_map.get(market_phase, "")
    if market_phase != "unknown" and phase_fr:
        parts.append(f"Phase de {phase_fr}")

    if fear_greed is not None:
        if fear_greed <= 25:
            parts.append(f"Fear & Greed {fear_greed} (peur extrême)")
        elif fear_greed <= 45:
            parts.append(f"Fear & Greed {fear_greed} (peur)")
        elif fear_greed <= 55:
            parts.append(f"Fear & Greed {fear_greed} (neutre)")
        elif fear_greed <= 75:
            parts.append(f"Fear & Greed {fear_greed} (greed)")
        else:
            parts.append(f"Fear & Greed {fear_greed} (greed extrême)")

    if not parts:
        return "Contexte macro insuffisant pour analyse."

    return "Contexte macro : " + ". ".join(parts) + "."


def technique_narrative(
    htf_bias: str = "neutral",
    ltf_bias: str = "neutral",
    alignment: str = "neutral",
    supports: Optional[List[float]] = None,
    resistances: Optional[List[float]] = None,
    vwap: Optional[float] = None,
    price: Optional[float] = None,
    active_setups: Optional[List[str]] = None,
) -> str:
    """Generate French narrative for technical analysis."""
    parts: List[str] = []

    bias_map = {"bullish": "haussier", "bearish": "baissier", "neutral": "neutre"}
    htf = bias_map.get(htf_bias, htf_bias)
    ltf = bias_map.get(ltf_bias, ltf_bias)

    parts.append(f"Biais HTF {htf}, LTF {ltf}")

    align_map = {
        "aligned_bullish": "alignés haussier",
        "aligned_bearish": "alignés baissier",
        "divergent": "divergents",
        "neutral": "neutre",
    }
    align_fr = align_map.get(alignment, alignment)
    parts.append(f"HTF/LTF {align_fr}")

    if supports:
        s_levels = ", ".join(str(int(s)) if s == int(s) else str(s) for s in sorted(supports)[:3])
        parts.append(f"Supports: {s_levels}")
    if resistances:
        r_levels = ", ".join(str(int(r)) if r == int(r) else str(r) for r in sorted(resistances)[:3])
        parts.append(f"Résistances: {r_levels}")

    if vwap is not None and price is not None:
        if price > vwap:
            parts.append(f"Prix au-dessus du VWAP ({vwap:.0f})")
        elif price < vwap:
            parts.append(f"Prix sous le VWAP ({vwap:.0f})")
        else:
            parts.append(f"Prix au VWAP ({vwap:.0f})")
    elif vwap is not None:
        parts.append(f"VWAP à {vwap:.0f}")

    if active_setups:
        setups_str = ", ".join(active_setups[:3])
        parts.append(f"Setups actifs: {setups_str}")

    return "Analyse technique : " + ". ".join(parts) + "."


def flows_narrative(
    open_interest: Optional[float] = None,
    oi_change_pct: Optional[float] = None,
    funding_rate: Optional[float] = None,
    long_short_ratio: Optional[float] = None,
    liquidations_long: Optional[float] = None,
    liquidations_short: Optional[float] = None,
    etf_flow: Optional[str] = None,
) -> str:
    """Generate French narrative for flow/positioning analysis."""
    parts: List[str] = []

    if open_interest is not None:
        oi_str = f"OI {open_interest / 1e9:.1f}B$"
        if oi_change_pct is not None:
            direction = "hausse" if oi_change_pct > 0 else "baisse"
            oi_str += f" ({direction} {abs(oi_change_pct):.1f}%)"
        parts.append(oi_str)

    if funding_rate is not None:
        if funding_rate > 0.01:
            parts.append(f"Funding élevé ({funding_rate:.4f}%)")
        elif funding_rate > 0:
            parts.append(f"Funding positif ({funding_rate:.4f}%)")
        elif funding_rate < 0:
            parts.append(f"Funding négatif ({funding_rate:.4f}%)")
        else:
            parts.append("Funding neutre")

    if long_short_ratio is not None:
        if long_short_ratio > 2.0:
            parts.append(f"Ratio L/S très élevé ({long_short_ratio:.1f}) — crowding long")
        elif long_short_ratio > 1.5:
            parts.append(f"Ratio L/S élevé ({long_short_ratio:.1f})")
        elif long_short_ratio < 0.5:
            parts.append(f"Ratio L/S très bas ({long_short_ratio:.1f}) — crowding short")
        elif long_short_ratio < 1.0:
            parts.append(f"Ratio L/S bas ({long_short_ratio:.1f})")
        else:
            parts.append(f"Ratio L/S équilibré ({long_short_ratio:.1f})")

    if liquidations_long is not None and liquidations_short is not None:
        if liquidations_long > liquidations_short * 2:
            parts.append("Liquidations longs dominantes")
        elif liquidations_short > liquidations_long * 2:
            parts.append("Liquidations shorts dominantes")
        else:
            total = liquidations_long + liquidations_short
            if total > 0:
                parts.append(f"Liquidations équilibrées (total {total / 1e6:.0f}M$)")

    if etf_flow:
        flow_map = {"inflow": "ETF inflows", "outflow": "ETF outflows", "flat": "ETF flat"}
        parts.append(flow_map.get(etf_flow, etf_flow))

    if not parts:
        return "Données de flux insuffisantes pour analyse."

    return "Flux et positionnement : " + ". ".join(parts) + "."


def news_narrative(
    sentiment: str = "unknown",
    sentiment_score: float = 0.0,
    key_drivers: Optional[List[str]] = None,
    total_signals: int = 0,
    tg_count: int = 0,
    cdp_count: int = 0,
) -> str:
    """Generate French narrative for news/sentiment."""
    parts: List[str] = []

    sent_map = {"positive": "positif", "negative": "négatif", "neutral": "neutre"}
    sent_fr = sent_map.get(sentiment, sentiment)
    parts.append(f"Sentiment {sent_fr} (score {sentiment_score:+.2f})")

    signal_parts = []
    if tg_count:
        signal_parts.append(f"{tg_count} signaux Telegram")
    if cdp_count:
        signal_parts.append(f"{cdp_count} signaux CDP")
    if signal_parts:
        parts.append("Signaux: " + ", ".join(signal_parts))

    if key_drivers:
        drivers_str = "; ".join(key_drivers[:3])
        parts.append(f"Drivers: {drivers_str}")

    return "Analyse news : " + ". ".join(parts) + "."


def risks_narrative(risks: Optional[List[Any]] = None) -> str:
    """Generate French narrative summarizing risks."""
    if not risks:
        return "Aucun risque significatif identifié."

    high = [r for r in risks if getattr(r, "severity", None) == "high"]
    moderate = [r for r in risks if getattr(r, "severity", None) == "moderate"]
    low = [r for r in risks if getattr(r, "severity", None) == "low"]

    parts = []
    if high:
        parts.append(f"{len(high)} risque(s) élevé(s)")
    if moderate:
        parts.append(f"{len(moderate)} risque(s) modéré(s)")
    if low:
        parts.append(f"{len(low)} risque(s) faible(s)")

    if not parts:
        return "Risques non évalués."

    summary = "Risques : " + ", ".join(parts) + "."
    if high:
        first_high = getattr(high[0], "description", "")
        if first_high:
            summary += f" Principal: {first_high[:150]}"
    return summary


def probabilities_narrative(
    bull: int = 33,
    range_val: int = 34,
    bear: int = 33,
) -> str:
    """Generate French narrative for probability decomposition."""
    if bull > bear and bull > range_val:
        bias = "haussier"
        conf = "élevée" if bull >= 60 else "modérée" if bull >= 45 else "faible"
    elif bear > bull and bear > range_val:
        bias = "baissier"
        conf = "élevée" if bear >= 60 else "modérée" if bear >= 45 else "faible"
    else:
        bias = "neutre"
        conf = "élevée" if range_val >= 50 else "modérée"

    return (
        f"Probabilités : biais {bias}, conviction {conf}. "
        f"Haussier {bull}%, Range {range_val}%, Baissier {bear}%."
    )


def action_narrative(
    direction: str = "neutral",
    has_setups: bool = False,
    has_high_risk: bool = False,
) -> str:
    """Generate French narrative for the action recommendation."""
    dir_map = {
        "bullish": "Biais haussier",
        "bearish": "Biais baissier",
        "neutral": "Biais neutre",
        "wait": "En attente de confirmation",
    }
    base = dir_map.get(direction, direction)

    if direction == "wait":
        base += ". Aucun setup confirmé pour le moment"
    elif not has_setups:
        base += ". Aucun setup technique actif"

    if has_high_risk:
        base += ". Attention : risque(s) élevé(s) détecté(s)"

    base += ". Surveillance uniquement — aucun ordre automatique."
    return base


def voice_one_liner(
    symbol: str = "???",
    direction: str = "neutral",
    htf_bias: str = "neutral",
    ltf_bias: str = "neutral",
    prob_bull: int = 33,
    prob_bear: int = 33,
) -> str:
    """Generate a single-line French voice summary (< 200 chars)."""
    dir_map = {
        "bullish": "haussier",
        "bearish": "baissier",
        "neutral": "neutre",
        "wait": "en attente",
    }
    dir_fr = dir_map.get(direction, direction)

    bias_map = {"bullish": "haussière", "bearish": "baissière", "neutral": "neutre"}
    htf_fr = bias_map.get(htf_bias, htf_bias)
    ltf_fr = bias_map.get(ltf_bias, ltf_bias)

    line = f"{symbol} biais {dir_fr}. HTF {htf_fr}, LTF {ltf_fr}. Proba {prob_bull}/{prob_bear}%."

    # Ensure < 200 chars
    if len(line) > 200:
        line = line[:197] + "..."

    return line
