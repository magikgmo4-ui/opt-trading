"""
Context builder — PR3.

Builds the MarketContext section from MarketContextInput.
Determines macro regime, DXY/VIX/SPY trends, market phase.
Never crashes — uses defaults for missing data.
"""

from __future__ import annotations

from typing import Optional

from .context_aggregator import MarketContextInput
from .models import MarketContext
from .narrative import context_narrative


def build_context(ctx: MarketContextInput) -> MarketContext:
    """Build a MarketContext from aggregated data.

    Extracts macro regime from multi-TF analysis raw data,
    DXY/VIX/SPY from macro context, and market phase from technical bias.
    """
    macro_regime = "unknown"
    dxy_trend = "unknown"
    vix_state = "unknown"
    spy_trend = "unknown"
    market_phase = "unknown"
    fear_greed = None

    # ── Extract from multi-TF raw data ──────────────────────────────────
    mtf = ctx.multitf_raw or {}
    macro_ctx = mtf.get("macro_context", {}) if isinstance(mtf, dict) else {}

    if isinstance(macro_ctx, dict):
        if macro_ctx.get("risk_regime"):
            mr = str(macro_ctx["risk_regime"]).lower()
            if mr in ("risk_on", "risk_off", "neutral"):
                macro_regime = mr
        if macro_ctx.get("dxy_trend"):
            dt = str(macro_ctx["dxy_trend"]).lower()
            if dt in ("bullish", "bearish", "neutral"):
                dxy_trend = dt
        if macro_ctx.get("vix_state"):
            vs = str(macro_ctx["vix_state"]).lower()
            if vs in ("low", "normal", "elevated", "high"):
                vix_state = vs
        if macro_ctx.get("spy_trend"):
            st = str(macro_ctx["spy_trend"]).lower()
            if st in ("bullish", "bearish", "neutral"):
                spy_trend = st

    # ── Derive from technique when macro is missing ─────────────────────
    if macro_regime == "unknown":
        # Use HTF bias as proxy for risk environment
        htf_bias = _extract_htf_bias(ctx)
        if htf_bias == "bullish":
            macro_regime = "risk_on"
        elif htf_bias == "bearish":
            macro_regime = "risk_off"

    if market_phase == "unknown":
        htf_bias = _extract_htf_bias(ctx)
        ltf_bias = _extract_ltf_bias(ctx)
        if htf_bias == "bullish" and ltf_bias == "bullish":
            market_phase = "markup"
        elif htf_bias == "bearish" and ltf_bias == "bearish":
            market_phase = "markdown"
        elif htf_bias == "bearish" and ltf_bias == "bullish":
            market_phase = "accumulation"
        elif htf_bias == "bullish" and ltf_bias == "bearish":
            market_phase = "distribution"

    # ── Extract from flow metrics ───────────────────────────────────────
    flow = ctx.flow_inputs
    if flow is not None:
        # Price change can inform DXY trend (not applicable here, just skip)

        # Funding rate polarity
        if flow.funding_rate is not None:
            if flow.funding_rate > 0.01:
                if macro_regime == "risk_on":
                    market_phase = "markup"  # confirmed by funding
            elif flow.funding_rate < -0.01:
                if macro_regime == "risk_off":
                    market_phase = "markdown"

    # ── Narrative ───────────────────────────────────────────────────────
    narrative = context_narrative(
        macro_regime=macro_regime,
        dxy_trend=dxy_trend,
        vix_state=vix_state,
        spy_trend=spy_trend,
        market_phase=market_phase,
        fear_greed=fear_greed,
    )

    return MarketContext(
        macro_regime=macro_regime,  # type: ignore[arg-type]
        dxy_trend=dxy_trend,  # type: ignore[arg-type]
        vix_state=vix_state,  # type: ignore[arg-type]
        spy_trend=spy_trend,  # type: ignore[arg-type]
        market_phase=market_phase,  # type: ignore[arg-type]
        narrative=narrative,
    )


# ── Helpers ────────────────────────────────────────────────────────────────

def _extract_htf_bias(ctx: MarketContextInput) -> str:
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        bias = mtf.get("bias", {})
        if isinstance(bias, dict):
            htf = bias.get("htf", "")
            if htf in ("bullish", "bearish", "neutral"):
                return htf
        # Try timeframes
        tfs = mtf.get("timeframes", {})
        if isinstance(tfs, dict):
            for tf in ("D1", "W1", "H4"):
                tf_data = tfs.get(tf, {})
                if isinstance(tf_data, dict):
                    ind = tf_data.get("indicators", {})
                    if isinstance(ind, dict):
                        trend = ind.get("trend", "")
                        if trend in ("bullish", "bearish", "neutral"):
                            return trend
    return "neutral"


def _extract_ltf_bias(ctx: MarketContextInput) -> str:
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        bias = mtf.get("bias", {})
        if isinstance(bias, dict):
            ltf = bias.get("ltf", "")
            if ltf in ("bullish", "bearish", "neutral"):
                return ltf
        tfs = mtf.get("timeframes", {})
        if isinstance(tfs, dict):
            for tf in ("M15", "H1", "H4"):
                tf_data = tfs.get(tf, {})
                if isinstance(tf_data, dict):
                    ind = tf_data.get("indicators", {})
                    if isinstance(ind, dict):
                        trend = ind.get("trend", "")
                        if trend in ("bullish", "bearish", "neutral"):
                            return trend
    return "neutral"
