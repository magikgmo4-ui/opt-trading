"""
Technique builder — PR3.

Builds the TechnicalSection from MarketContextInput.
Extracts HTF/LTF bias, alignment, key levels, active setups.
Never crashes — uses defaults for missing data.
"""

from __future__ import annotations

from typing import List, Optional

from ..context_aggregator import MarketContextInput
from ..models import TechnicalSection
from ..narrative import technique_narrative


def build_technique(ctx: MarketContextInput) -> TechnicalSection:
    """Build a TechnicalSection from aggregated data."""

    # ── Bias extraction ─────────────────────────────────────────────────
    htf_bias = _extract_htf_bias(ctx)
    ltf_bias = _extract_ltf_bias(ctx)
    alignment = _compute_alignment(htf_bias, ltf_bias)

    # ── Key levels ──────────────────────────────────────────────────────
    supports, resistances, vwap = _extract_levels(ctx)

    # ── Price (for VWAP comparison) ─────────────────────────────────────
    price = _extract_price(ctx)

    # ── Active setups ───────────────────────────────────────────────────
    setups = ctx.priority_inputs
    active_names: List[str] = []
    for s in setups:
        if s.grade not in ("REJECT",) and s.grade in ("A+", "A", "A-", "B+", "B", "B-", "C"):
            active_names.append(s.setup_id)

    # ── Narrative ───────────────────────────────────────────────────────
    narrative = technique_narrative(
        htf_bias=htf_bias,
        ltf_bias=ltf_bias,
        alignment=alignment,
        supports=supports if supports else None,
        resistances=resistances if resistances else None,
        vwap=vwap,
        price=price,
        active_setups=active_names if active_names else None,
    )

    return TechnicalSection(
        htf_bias=htf_bias,  # type: ignore[arg-type]
        ltf_bias=ltf_bias,  # type: ignore[arg-type]
        alignment=alignment,  # type: ignore[arg-type]
        key_support=supports,
        key_resistance=resistances,
        vwap=vwap,
        active_setups=active_names,
        narrative=narrative,
    )


# ── Helpers ────────────────────────────────────────────────────────────────

def _extract_htf_bias(ctx: MarketContextInput) -> str:
    """Extract higher timeframe bias from multi-TF or vision data."""
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        bias = mtf.get("bias", {})
        if isinstance(bias, dict):
            htf = bias.get("htf", "")
            if htf in ("bullish", "bearish", "neutral"):
                return htf
        tfs = mtf.get("timeframes", {})
        if isinstance(tfs, dict):
            for tf_key in ("D1", "W1", "H4"):
                tf_data = tfs.get(tf_key, {})
                if isinstance(tf_data, dict):
                    ind = tf_data.get("indicators", {})
                    if isinstance(ind, dict):
                        trend = ind.get("trend", "")
                        if trend in ("bullish", "bearish", "neutral"):
                            return trend

    # Fallback: derive from vision analysis summary
    for v in ctx.vision_inputs:
        if v.analysis_summary:
            summary_lower = v.analysis_summary.lower()
            if "bearish" in summary_lower and "bullish" not in summary_lower:
                return "bearish"
            if "bullish" in summary_lower and "bearish" not in summary_lower:
                return "bullish"

    # Fallback: from active setups
    if ctx.priority_inputs:
        grades = [s.grade for s in ctx.priority_inputs if s.grade not in ("REJECT",)]
        if grades:
            best = grades[0]
            if "A" in best:
                return "bullish" if ctx.priority_inputs[0].direction == "long" else "bearish"

    return "neutral"


def _extract_ltf_bias(ctx: MarketContextInput) -> str:
    """Extract lower timeframe bias from multi-TF data."""
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        bias = mtf.get("bias", {})
        if isinstance(bias, dict):
            ltf = bias.get("ltf", "")
            if ltf in ("bullish", "bearish", "neutral"):
                return ltf
        tfs = mtf.get("timeframes", {})
        if isinstance(tfs, dict):
            for tf_key in ("M15", "H1", "H4"):
                tf_data = tfs.get(tf_key, {})
                if isinstance(tf_data, dict):
                    ind = tf_data.get("indicators", {})
                    if isinstance(ind, dict):
                        trend = ind.get("trend", "")
                        if trend in ("bullish", "bearish", "neutral"):
                            return trend

    # Fallback: from signal events
    recent_signals = [e for e in ctx.raw_events if e.source == "cdp"]
    if recent_signals:
        buy_count = sum(1 for e in recent_signals if "LONG" in e.direction.upper() or "BUY" in e.direction.upper())
        sell_count = sum(1 for e in recent_signals if "SHORT" in e.direction.upper() or "SELL" in e.direction.upper())
        if buy_count > sell_count:
            return "bullish"
        if sell_count > buy_count:
            return "bearish"

    return "neutral"


def _compute_alignment(htf: str, ltf: str) -> str:
    if htf == "bullish" and ltf == "bullish":
        return "aligned_bullish"
    if htf == "bearish" and ltf == "bearish":
        return "aligned_bearish"
    if htf in ("bullish", "bearish") and ltf in ("bullish", "bearish") and htf != ltf:
        return "divergent"
    return "neutral"


def _extract_levels(ctx: MarketContextInput) -> tuple[List[float], List[float], Optional[float]]:
    """Extract support/resistance levels and VWAP from all sources."""
    supports: List[float] = []
    resistances: List[float] = []
    vwap: Optional[float] = None

    # From vision analysis
    for v in ctx.vision_inputs:
        for s in v.support_levels:
            if s not in supports:
                supports.append(s)
        for r in v.resistance_levels:
            if r not in resistances:
                resistances.append(r)

    # From multi-TF analysis
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        levels = mtf.get("levels", {})
        if isinstance(levels, dict):
            for s in levels.get("support_levels", []):
                if isinstance(s, (int, float)) and s not in supports:
                    supports.append(s)
            for r in levels.get("resistance_levels", []):
                if isinstance(r, (int, float)) and r not in resistances:
                    resistances.append(r)
            v = levels.get("vwap")
            if isinstance(v, (int, float)):
                vwap = float(v)

    # From setups (entry zones act as support/resistance)
    for s in ctx.priority_inputs:
        if s.invalidation is not None:
            if s.direction == "long" and s.invalidation not in supports:
                supports.append(s.invalidation)
            elif s.direction == "short" and s.invalidation not in resistances:
                resistances.append(s.invalidation)

    return sorted(supports), sorted(resistances), vwap


def _extract_price(ctx: MarketContextInput) -> Optional[float]:
    """Extract current price from available sources."""
    # From market metrics
    flow = ctx.flow_inputs
    if flow is not None and flow.price is not None:
        return flow.price

    # From multi-TF
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        price = mtf.get("price")
        if isinstance(price, (int, float)):
            return float(price)

    # From last event
    for e in reversed(ctx.raw_events):
        if e.price is not None:
            return e.price

    return None
