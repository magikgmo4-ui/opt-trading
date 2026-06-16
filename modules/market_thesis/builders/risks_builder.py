"""
Risks builder — PR4.

Builds the risks list (RiskItem[]) from MarketContextInput.
Identifies concentration risk, technical risk, and event risk.
Never crashes — returns empty list if no data.
"""

from __future__ import annotations

from typing import List

from ..context_aggregator import MarketContextInput
from ..models import RiskItem
from ..narrative import risks_narrative


def build_risks(ctx: MarketContextInput) -> List[RiskItem]:
    """Build a list of RiskItem from aggregated data."""

    risks: List[RiskItem] = []

    flow = ctx.flow_inputs

    # ── Concentration risk (crowding) ──────────────────────────────────
    if flow is not None:
        ls = flow.long_short_ratio
        funding = flow.funding_rate

        if ls is not None:
            if ls > 2.0:
                risks.append(RiskItem(
                    category="concentration",
                    severity="high",
                    description=f"Crowding long très élevé (L/S {ls:.1f}). Risque de cascade de liquidations si support cassé.",
                ))
            elif ls > 1.5:
                risks.append(RiskItem(
                    category="concentration",
                    severity="moderate",
                    description=f"Crowding long élevé (L/S {ls:.1f}). Surveiller les niveaux de support.",
                ))
            elif ls < 0.5:
                risks.append(RiskItem(
                    category="concentration",
                    severity="high",
                    description=f"Crowding short très élevé (L/S {ls:.1f}). Risque de short squeeze.",
                ))
            elif ls < 1.0:
                risks.append(RiskItem(
                    category="concentration",
                    severity="moderate",
                    description=f"Crowding short modéré (L/S {ls:.1f}).",
                ))

        if funding is not None and abs(funding) > 0.05:
            risks.append(RiskItem(
                category="concentration",
                severity="high" if abs(funding) > 0.1 else "moderate",
                description=f"Funding rate extrême ({funding:.4f}%). Risque de squeeze.",
            ))

    # ── Technical risk ─────────────────────────────────────────────────
    setup_count = len([s for s in ctx.priority_inputs if s.grade not in ("REJECT",)])
    if setup_count == 0:
        risks.append(RiskItem(
            category="technical",
            severity="moderate",
            description="Aucun setup technique valide identifié. Absence de configuration claire.",
        ))

    # Check setup grades
    low_grades = [s for s in ctx.priority_inputs if s.grade in ("C", "REJECT")]
    if low_grades:
        risks.append(RiskItem(
            category="technical",
            severity="low",
            description=f"{len(low_grades)} setup(s) de grade faible (C ou REJECT). Attendre confirmation.",
        ))

    # ── Divergence risk ────────────────────────────────────────────────
    mtf = ctx.multitf_raw or {}
    if isinstance(mtf, dict):
        bias = mtf.get("bias", {})
        if isinstance(bias, dict):
            htf = bias.get("htf", "")
            ltf = bias.get("ltf", "")
            if htf == "bullish" and ltf == "bearish":
                risks.append(RiskItem(
                    category="technical",
                    severity="moderate",
                    description="Divergence HTF haussier / LTF baissier. Risque de fausse cassure haussière.",
                ))
            elif htf == "bearish" and ltf == "bullish":
                risks.append(RiskItem(
                    category="technical",
                    severity="moderate",
                    description="Divergence HTF baissier / LTF haussier. Rebond technique possible mais tendance baissière.",
                ))

    # ── Liquidation risk ───────────────────────────────────────────────
    if flow is not None and flow.liquidations_long is not None and flow.liquidations_short is not None:
        if flow.liquidations_long > flow.liquidations_short * 3:
            risks.append(RiskItem(
                category="concentration",
                severity="high",
                description="Liquidations longs 3x supérieures aux shorts. Risque de capitulation long.",
            ))
        elif flow.liquidations_short > flow.liquidations_long * 3:
            risks.append(RiskItem(
                category="concentration",
                severity="high",
                description="Liquidations shorts 3x supérieures aux longs. Risque de short squeeze.",
            ))

    # ── Event risk ─────────────────────────────────────────────────────
    mtf_raw = ctx.multitf_raw or {}
    if isinstance(mtf_raw, dict):
        macro = mtf_raw.get("macro_context", {})
        if isinstance(macro, dict):
            if macro.get("macro_high_impact_soon"):
                risks.append(RiskItem(
                    category="event",
                    severity="high",
                    description="Événement macro à haut impact imminent. Volatilité attendue.",
                ))

    # ── Stale data risk ────────────────────────────────────────────────
    if ctx.stale_sources:
        risks.append(RiskItem(
            category="technical",
            severity="low",
            description=f"Sources stale: {', '.join(ctx.stale_sources[:3])}. Données potentiellement obsolètes.",
        ))

    # ── Narrative ───────────────────────────────────────────────────────
    narrative = risks_narrative(risks)
    # (narrative is embedded in each RiskItem description and the summary)

    return risks
