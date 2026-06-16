"""
Action builder — PR5.

Builds the ActionPlan from MarketContextInput and all section builders.
Readiness is always monitor_only — no auto execution.
"""

from __future__ import annotations

from ..context_aggregator import MarketContextInput
from ..models import ActionPlan
from ..narrative import action_narrative, voice_one_liner


def build_action(
    ctx: MarketContextInput,
    htf_bias: str = "neutral",
    ltf_bias: str = "neutral",
    alignment: str = "neutral",
    probability_bull: int = 33,
    probability_bear: int = 33,
    has_setups: bool = False,
    has_high_risk: bool = False,
) -> ActionPlan:
    """Build an ActionPlan from context and derived signals."""

    # ── Direction ──────────────────────────────────────────────────────
    direction = _determine_direction(
        htf_bias=htf_bias,
        ltf_bias=ltf_bias,
        alignment=alignment,
        prob_bull=probability_bull,
        prob_bear=probability_bear,
    )

    # ── Key levels to watch ────────────────────────────────────────────
    key_levels = _build_key_levels(ctx)

    # ── Narratives ─────────────────────────────────────────────────────
    narrative = action_narrative(direction=direction, has_setups=has_setups, has_high_risk=has_high_risk)
    one_liner = voice_one_liner(
        symbol=ctx.symbol,
        direction=direction,
        htf_bias=htf_bias,
        ltf_bias=ltf_bias,
        prob_bull=probability_bull,
        prob_bear=probability_bear,
    )

    return ActionPlan(
        direction=direction,  # type: ignore[arg-type]
        readiness="monitor_only",
        key_levels=key_levels,
        narrative=narrative,
        voice_one_liner=one_liner,
    )


def _determine_direction(
    htf_bias: str,
    ltf_bias: str,
    alignment: str,
    prob_bull: int,
    prob_bear: int,
) -> str:
    """Determine directional bias from all signals."""
    bullish_signals = 0
    bearish_signals = 0

    if htf_bias == "bullish":
        bullish_signals += 2
    elif htf_bias == "bearish":
        bearish_signals += 2

    if ltf_bias == "bullish":
        bullish_signals += 1
    elif ltf_bias == "bearish":
        bearish_signals += 1

    if alignment == "aligned_bullish":
        bullish_signals += 2
    elif alignment == "aligned_bearish":
        bearish_signals += 2
    elif alignment == "divergent":
        # Reduce conviction for divergence
        pass

    # Probability contribution
    if prob_bull >= 60:
        bullish_signals += 2
    elif prob_bull >= 45:
        bullish_signals += 1
    if prob_bear >= 60:
        bearish_signals += 2
    elif prob_bear >= 45:
        bearish_signals += 1

    diff = bullish_signals - bearish_signals

    if diff >= 3:
        return "bullish"
    elif diff <= -3:
        return "bearish"
    elif abs(diff) <= 1:
        return "wait"
    else:
        return "neutral"


def _build_key_levels(ctx: MarketContextInput) -> list[str]:
    """Extract key levels to watch from all sources."""
    levels: list[str] = []

    # From setups
    for s in ctx.priority_inputs[:3]:
        if s.setup_id and s.grade not in ("REJECT",):
            entry = f"{s.setup_id}: entry "
            if s.entry_zone:
                entry += f"{s.entry_zone[0]:.0f}-{s.entry_zone[-1]:.0f}" if len(s.entry_zone) > 1 else f"{s.entry_zone[0]:.0f}"
            else:
                entry += "N/A"
            levels.append(entry)

            if s.invalidation is not None:
                levels.append(f"Invalidation: {s.invalidation:.0f}")

            if s.targets:
                for i, t in enumerate(s.targets[:2], 1):
                    levels.append(f"TP{i}: {t:.0f}")

    # From vision levels
    for v in ctx.vision_inputs:
        for s in v.support_levels[:1]:
            levels.append(f"Support: {s:.0f}")
        for r in v.resistance_levels[:1]:
            levels.append(f"Resistance: {r:.0f}")

    # From multi-TF
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        lvls = mtf.get("levels", {})
        if isinstance(lvls, dict):
            vwap = lvls.get("vwap")
            if isinstance(vwap, (int, float)):
                levels.append(f"VWAP: {vwap:.0f}")

    return levels


def build_action_narrative_wrapper(
    symbol: str,
    direction: str,
    htf_bias: str = "neutral",
    ltf_bias: str = "neutral",
    prob_bull: int = 33,
    prob_bear: int = 33,
) -> str:
    """Generate concise French action narrative and voice one-liner."""
    return voice_one_liner(
        symbol=symbol,
        direction=direction,
        htf_bias=htf_bias,
        ltf_bias=ltf_bias,
        prob_bull=prob_bull,
        prob_bear=prob_bear,
    )
