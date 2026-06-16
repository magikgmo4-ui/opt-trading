"""
Probabilities builder — PR4.

Builds the ProbabilitySet from MarketContextInput.
Aggregates scores from multi-TF setups, priority engine, and flow metrics.
Produces bull/range/bear percentages (must total 100).

Never crashes — returns balanced 33/34/33 if no data.
"""

from __future__ import annotations

from ..context_aggregator import MarketContextInput
from ..models import ProbabilitySet
from ..narrative import probabilities_narrative


def build_probabilities(ctx: MarketContextInput) -> ProbabilitySet:
    """Build a ProbabilitySet from aggregated data.

    Sources (weighted):
    - Multi-TF setup scores (weight 0.40)
    - Flow/positioning signal (weight 0.30)
    - CDP/Telegram signal bias (weight 0.20)
    - HTF/LTF alignment (weight 0.10)
    """

    bull_score = 0.0
    bear_score = 0.0
    total_weight = 0.0

    flow = ctx.flow_inputs

    # ── Multi-TF setups (weight 0.40) ──────────────────────────────────
    setups = ctx.priority_inputs
    if setups:
        weight = 0.40
        for s in setups:
            if s.direction == "long":
                bull_score += (s.probability_pct / 100.0) * weight
            elif s.direction == "short":
                bear_score += (s.probability_pct / 100.0) * weight
            # monitor_only: neutral contribution
        total_weight += weight

    # ── Flow / positioning (weight 0.30) ───────────────────────────────
    if flow is not None:
        weight = 0.30
        # Funding rate polarity
        if flow.funding_rate is not None:
            if flow.funding_rate > 0.01:
                bear_score += 0.15  # positive funding = bearish signal (crowded longs)
            elif flow.funding_rate < -0.01:
                bull_score += 0.15  # negative funding = bullish signal (crowded shorts)

        # Long/short ratio
        if flow.long_short_ratio is not None:
            if flow.long_short_ratio > 2.0:
                bear_score += 0.15  # overly bullish positioning
            elif flow.long_short_ratio < 0.5:
                bull_score += 0.15  # overly bearish positioning
            else:
                bull_score += 0.05
                bear_score += 0.05

        total_weight += weight

    # ── CDP / Telegram signals (weight 0.20) ───────────────────────────
    tg = ctx.telegram_inputs
    cdp = [e for e in ctx.news_inputs if e.source == "cdp"]
    if tg or cdp:
        weight = 0.20
        tg_bull = sum(1 for s in tg if s.direction.upper() in ("LONG", "BUY"))
        tg_bear = sum(1 for s in tg if s.direction.upper() in ("SHORT", "SELL"))
        tg_total = tg_bull + tg_bear
        if tg_total > 0:
            bull_score += (tg_bull / tg_total) * weight * 0.5
            bear_score += (tg_bear / tg_total) * weight * 0.5

        cdp_bull = sum(1 for e in cdp if e.event_type in (
            "VWAP_RECLAIM", "ORB_HIGH_BREAK", "BOS_BULL", "CHOCH_BULL"))
        cdp_bear = sum(1 for e in cdp if e.event_type in (
            "VWAP_LOSS", "ORB_LOW_BREAK", "BOS_BEAR", "CHOCH_BEAR"))
        cdp_total = cdp_bull + cdp_bear
        if cdp_total > 0:
            bull_score += (cdp_bull / cdp_total) * weight * 0.5
            bear_score += (cdp_bear / cdp_total) * weight * 0.5

        total_weight += weight

    # ── HTF/LTF alignment (weight 0.10) ────────────────────────────────
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        bias = mtf.get("bias", {})
        if isinstance(bias, dict):
            htf = bias.get("htf", "")
            ltf = bias.get("ltf", "")
            if htf or ltf:
                weight = 0.10
                if htf == "bullish" and ltf == "bullish":
                    bull_score += 0.10
                elif htf == "bearish" and ltf == "bearish":
                    bear_score += 0.10
                elif htf == "bullish":
                    bull_score += 0.05
                elif htf == "bearish":
                    bear_score += 0.05
                total_weight += weight

    # ── Normalize to 100% ──────────────────────────────────────────────
    if total_weight > 0:
        # Scale scores to the weight actually applied
        raw_bull = bull_score
        raw_bear = bear_score
        raw_range = max(0.0, 1.0 - raw_bull - raw_bear)

        bull = int(round(raw_bull * 100))
        bear = int(round(raw_bear * 100))
        range_val = int(round(raw_range * 100))
    else:
        # No data: balanced default
        bull, range_val, bear = 33, 34, 33

    # ── Ensure total == 100 (adjust range) ─────────────────────────────
    total = bull + range_val + bear
    if total != 100:
        diff = 100 - total
        range_val += diff

    # ── Clamp all values ───────────────────────────────────────────────
    if bull < 0:
        extra = -bull
        bull = 0
        range_val -= extra
    if bear < 0:
        extra = -bear
        bear = 0
        range_val -= extra
    if range_val < 0:
        range_val = 0

    # Final adjustment
    total = bull + range_val + bear
    if total != 100:
        range_val += (100 - total)
    range_val = max(0, min(100, range_val))

    # ── Narrative ───────────────────────────────────────────────────────
    narrative = probabilities_narrative(bull=bull, range_val=range_val, bear=bear)

    return ProbabilitySet(bull=bull, range=range_val, bear=bear)
