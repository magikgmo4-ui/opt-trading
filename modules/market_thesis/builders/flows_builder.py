"""
Flows builder — PR3.

Builds the FlowSection from MarketContextInput.
Extracts derivatives metrics (OI, funding, L/S, liquidations)
and positioning signals (ETF flows, smart money).
Never crashes — uses defaults for missing data.
"""

from __future__ import annotations

from typing import Optional

from ..context_aggregator import MarketContextInput
from ..models import FlowSection
from ..narrative import flows_narrative


def build_flows(ctx: MarketContextInput) -> FlowSection:
    """Build a FlowSection from aggregated data."""

    oi: Optional[float] = None
    oi_change: Optional[float] = None
    funding: Optional[float] = None
    ls_ratio: Optional[float] = None
    liq_long: Optional[float] = None
    liq_short: Optional[float] = None
    etf: Optional[str] = None

    # ── Market metrics (primary source) ─────────────────────────────────
    flow = ctx.flow_inputs
    if flow is not None:
        oi = flow.open_interest
        funding = flow.funding_rate
        ls_ratio = flow.long_short_ratio
        liq_long = flow.liquidations_long
        liq_short = flow.liquidations_short
        if flow.price_change_24h_pct is not None:
            oi_change = flow.price_change_24h_pct  # proxy for OI change via price

    # ── Coinglass vision (supplement) ───────────────────────────────────
    for v in ctx.vision_inputs:
        for det in v.coinglass_detections:
            mtype = det.get("detected_metric_type", "")
            val = det.get("extracted_value")
            if not isinstance(val, (int, float)):
                continue
            if mtype == "open_interest" and oi is None:
                oi = float(val)
            elif mtype == "long_short_ratio" and ls_ratio is None:
                ls_ratio = float(val)
            elif mtype == "liquidations_long" and liq_long is None:
                liq_long = float(val)
            elif mtype == "liquidations_short" and liq_short is None:
                liq_short = float(val)
            elif mtype == "funding_rate" and funding is None:
                funding = float(val)

    # ── ETF flow from telegram or context ───────────────────────────────
    # (Stub: real ETF flow data comes in Phase D with external data)
    etf = _derive_etf_flow(ctx)

    # ── OI change from multi-TF ─────────────────────────────────────────
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        orderflow = mtf.get("orderflow", {})
        if isinstance(orderflow, dict):
            oi_change_raw = orderflow.get("open_interest_change_pct")
            if isinstance(oi_change_raw, (int, float)):
                oi_change = float(oi_change_raw)

    # ── Narrative ───────────────────────────────────────────────────────
    narrative = flows_narrative(
        open_interest=oi,
        oi_change_pct=oi_change,
        funding_rate=funding,
        long_short_ratio=ls_ratio,
        liquidations_long=liq_long,
        liquidations_short=liq_short,
        etf_flow=etf,
    )

    return FlowSection(
        open_interest=oi,
        oi_change_24h_pct=oi_change,
        funding_rate=funding,
        long_short_ratio=ls_ratio,
        liquidations_long=liq_long,
        liquidations_short=liq_short,
        etf_flow=etf,
        narrative=narrative,
    )


# ── Helpers ────────────────────────────────────────────────────────────────

def _derive_etf_flow(ctx: MarketContextInput) -> Optional[str]:
    """Derive ETF flow direction from context, if available."""
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        macro = mtf.get("macro_context", {})
        if isinstance(macro, dict):
            etf_val = macro.get("etf_flow_bias")
            if isinstance(etf_val, str) and etf_val in ("inflow", "outflow", "flat"):
                return etf_val

    # Fallback: derive from price trend + OI trend
    flow = ctx.flow_inputs
    if flow is not None:
        if flow.price_change_24h_pct is not None:
            if flow.price_change_24h_pct > 2.0:
                return "inflow"
            elif flow.price_change_24h_pct < -2.0:
                return "outflow"

    return None
