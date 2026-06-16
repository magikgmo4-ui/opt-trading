"""
Executive Briefing Engine — PR5.

Synthesizes cross-asset analysis, regime detection, and change detection
into a human-readable ExecutiveBriefing for DeskPro, Voice, and API.

Read-only. No trade execution.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from .cross_asset_engine import build_leaderboard, compute_influences, detect_leaders, detect_laggards
from .models import ExecutiveBriefing, TopOpportunity, TopRisk
from .narrative_memory import detect_changes, summarize_changes
from .regime_engine import detect_regime


def build_briefing() -> ExecutiveBriefing:
    """Build a complete executive briefing from all engines.

    Returns an ExecutiveBriefing with summary, what_changed, what_to_watch,
    top risks/opportunities, and voice-friendly text.
    """
    now = datetime.now(timezone.utc)
    briefing_id = f"brief_{now.strftime('%Y%m%dT%H%M%SZ')}"

    # ── Gather data ──────────────────────────────────────────────────
    board = build_leaderboard()
    regime = detect_regime()
    influences = compute_influences()
    changes = detect_changes()
    change_summary = summarize_changes(changes)

    leaders = detect_leaders()
    laggards = detect_laggards()

    # ── Leaders & laggards ────────────────────────────────────────────
    leader_names = [e.symbol for e in leaders]
    laggard_names = [e.symbol for e in laggards]

    # ── Summary ───────────────────────────────────────────────────────
    summary = _build_summary(regime.regime, regime.confidence, board, leaders, laggards)

    # ── What changed ──────────────────────────────────────────────────
    what_changed = change_summary

    # ── What to watch ─────────────────────────────────────────────────
    what_to_watch = _build_what_to_watch(board, regime, changes)

    # ── Top risks ─────────────────────────────────────────────────────
    top_risks = _build_top_risks(board, regime, changes)

    # ── Top opportunities ─────────────────────────────────────────────
    top_opportunities = _build_top_opportunities(board, leaders)

    # ── Voice ─────────────────────────────────────────────────────────
    voice_one_liner = _build_voice_one_liner(regime.regime, board, leaders, laggards)
    voice_briefing = _build_voice_briefing(regime, board, leaders, laggards, changes)

    return ExecutiveBriefing(
        briefing_id=briefing_id,
        generated_at=now,
        market_regime=regime.regime,
        regime_confidence=regime.confidence,
        overall_confidence=regime.confidence,
        leaders=leader_names,
        laggards=laggard_names,
        summary=summary,
        what_changed=what_changed,
        what_to_watch=what_to_watch,
        top_risks=[r.description for r in top_risks],
        top_opportunities=[o.reason for o in top_opportunities],
        voice_one_liner=voice_one_liner,
        voice_briefing=voice_briefing,
    )


# ── Summary ────────────────────────────────────────────────────────────────

def _build_summary(regime: str, confidence: int, board, leaders, laggards) -> str:
    regime_names = {
        "risk_on": "Risk-On", "risk_off": "Risk-Off", "expansion": "Expansion",
        "compression": "Compression", "distribution": "Distribution",
        "accumulation": "Accumulation", "panic": "Panique", "recovery": "Reprise",
    }
    name = regime_names.get(regime, regime)

    total = len(board)
    bullish = sum(1 for e in board if e.direction == "bullish")
    bearish = sum(1 for e in board if e.direction == "bearish")

    parts = [f"Le marché reste en régime {name} avec {confidence}% de confiance."]

    if leaders:
        leader_str = ", ".join(l.symbol for l in leaders[:3])
        parts.append(f"Les leaders sont {leader_str}.")

    if laggards:
        laggard_str = ", ".join(l.symbol for l in laggards[:3])
        parts.append(f"Les actifs en retard sont {laggard_str}.")

    parts.append(f"{bullish} actifs sur {total} en biais haussier, {bearish} baissiers.")

    return " ".join(parts)


# ── What to watch ──────────────────────────────────────────────────────────

def _build_what_to_watch(board, regime, changes) -> str:
    parts = []

    # High-risk assets
    high_risk = [e for e in board if e.confidence < 40 and e.direction in ("bearish", "neutral")]
    if high_risk:
        parts.append(f"Surveiller {', '.join(e.symbol for e in high_risk[:3])} : confiance faible.")

    # Regime-specific advice
    advice = {
        "risk_on": "Le momentum haussier est favorable. Surveiller les signes de distribution.",
        "risk_off": "Prudence recommandée. Attendre les signes de reprise avant exposition.",
        "expansion": "La tendance haussière s'accélère. Risque de surchauffe à surveiller.",
        "compression": "Le marché est en phase de décision. Une cassure directionnelle est probable.",
        "panic": "Éviter toute exposition. Attendre la stabilisation complète.",
        "recovery": "Opportunités d'accumulation. Confirmer les supports avant d'agir.",
    }
    if regime.regime in advice:
        parts.append(advice[regime.regime])

    return " ".join(parts) if parts else "Surveiller l'évolution des indicateurs clés."


# ── Top risks ──────────────────────────────────────────────────────────────

def _build_top_risks(board, regime, changes) -> List[TopRisk]:
    risks: List[TopRisk] = []

    # Concentration risk
    high_conf_bull = [e for e in board if e.direction == "bullish" and e.confidence >= 75]
    if len(high_conf_bull) >= 4:
        risks.append(TopRisk(
            symbol="market",
            category="concentration",
            severity="high",
            score=70,
            description=f"Crowding haussier: {len(high_conf_bull)} actifs avec confiance > 75%. Risque de correction si sentiment bascule.",
        ))

    # Weak assets
    weak = [e for e in board if e.confidence <= 35]
    for w in weak[:2]:
        risks.append(TopRisk(
            symbol=w.symbol,
            category="technical",
            severity="moderate",
            score=50,
            description=f"{w.symbol} en faiblesse (confiance {w.confidence}%). Risque de poursuite baissière.",
        ))

    # Regime risk
    if regime.regime in ("panic", "risk_off"):
        risks.append(TopRisk(
            symbol="market",
            category="macro",
            severity="high",
            score=80,
            description=f"Régime {regime.regime} actif. Volatilité et risque systémique élevés.",
        ))

    # Divergence risk
    leader_dirs = {e.direction for e in board if e.is_leader}
    if len(leader_dirs) >= 2 and "bullish" in leader_dirs and "bearish" in leader_dirs:
        risks.append(TopRisk(
            symbol="market",
            category="concentration",
            severity="moderate",
            score=55,
            description="Divergence entre leaders : signaux contradictoires. Risque de rotation sectorielle.",
        ))

    return risks


# ── Top opportunities ──────────────────────────────────────────────────────

def _build_top_opportunities(board, leaders) -> List[TopOpportunity]:
    opps: List[TopOpportunity] = []

    for l in leaders[:3]:
        score = int((l.confidence + l.reliability + l.momentum_score) / 3)
        reason = f"{l.symbol}: biais {l.direction}, confiance {l.confidence}%, fiabilité {l.reliability}%."
        if l.momentum_score >= 60:
            reason += " Momentum fort."
        opps.append(TopOpportunity(
            symbol=l.symbol,
            direction=l.direction,
            confidence=l.confidence,
            reliability=l.reliability,
            score=score,
            reason=reason,
        ))

    return opps


# ── Voice ──────────────────────────────────────────────────────────────────

def _build_voice_one_liner(regime: str, board, leaders, laggards) -> str:
    regime_fr = {
        "risk_on": "Risk-On", "risk_off": "Risk-Off", "panic": "Panique",
        "expansion": "Expansion", "compression": "Compression",
        "recovery": "Reprise",
    }.get(regime, regime)

    bullish = sum(1 for e in board if e.direction == "bullish")
    total = len(board)
    leader_str = ", ".join(l.symbol for l in leaders[:2])
    top_risk = "dollar" if regime in ("risk_on", "expansion") else "volatilité"

    line = f"Marché en régime {regime_fr}. {leader_str} en tête. {bullish} actifs sur {total} haussiers. Risque principal: {top_risk}."
    if len(line) > 300:
        line = line[:297] + "..."
    return line


def _build_voice_briefing(regime, board, leaders, laggards, changes) -> str:
    regime_fr = {
        "risk_on": "Risk-On", "risk_off": "Risk-Off", "panic": "Panique",
        "expansion": "Expansion", "compression": "Compression",
        "recovery": "Reprise",
    }.get(regime.regime, regime.regime)

    parts = [f"Régime de marché {regime_fr} avec {regime.confidence}% de confiance."]

    if leaders:
        parts.append(f"Les leaders sont {', '.join(l.symbol for l in leaders[:3])}.")
    if laggards:
        parts.append(f"Les actifs en retard sont {', '.join(l.symbol for l in laggards[:3])}.")

    # Add change summary
    major_changes = [c for c in changes if c.magnitude == "major" and c.field != "initialization"]
    if major_changes:
        parts.append(major_changes[0].description)

    parts.append("Surveillance recommandée sur tous les actifs. Aucun ordre automatique.")

    text = ". ".join(parts)
    if len(text) > 600:
        text = text[:597] + "..."
    return text
