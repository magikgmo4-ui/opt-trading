"""
Market Regime Engine — PR3.

Detects the current market regime from cross-asset data and individual theses.
Classifies into: risk_on, risk_off, expansion, compression, distribution,
accumulation, panic, recovery, unknown.

Read-only. No trade execution.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from .cross_asset_engine import build_leaderboard, compute_influences
from .models import MarketRegime, RegimeEvidence


def detect_regime() -> MarketRegime:
    """Detect the current market regime from all available data.

    Returns a MarketRegime with classification, confidence, risk_score,
    evidence, and narrative.
    """
    now = datetime.now(timezone.utc)

    # Gather data
    board = build_leaderboard()
    influences = compute_influences()

    # ── Evidence ──────────────────────────────────────────────────────
    evidence = _gather_evidence(board, influences)

    # ── Classify ──────────────────────────────────────────────────────
    regime, confidence = _classify_regime(board, evidence)

    # ── Risk score ────────────────────────────────────────────────────
    risk_score = _compute_risk_score(board, evidence, regime)

    # ── Transition ────────────────────────────────────────────────────
    next_regime, transition_prob = _predict_transition(regime, board, evidence)

    # ── Narrative ─────────────────────────────────────────────────────
    narrative = _build_narrative(regime, confidence, evidence, board)

    return MarketRegime(
        regime=regime,  # type: ignore[arg-type]
        confidence=confidence,
        risk_score=risk_score,
        evidence=evidence,
        narrative=narrative,
        next_likely_regime=next_regime,
        transition_probability=transition_prob,
        generated_at=now,
    )


# ── Evidence gathering ─────────────────────────────────────────────────────

def _gather_evidence(board, influences) -> RegimeEvidence:
    """Extract regime evidence from leaderboard and influences."""
    bullish = sum(1 for e in board if e.direction == "bullish")
    bearish = sum(1 for e in board if e.direction == "bearish")

    # DXY / VIX / SPY — check if they're in the tracked symbols
    dxy_trend = "unknown"
    vix_level = "unknown"
    spy_trend = "unknown"
    btc_dominance = None
    fear_greed = None

    # Derive from leaderboard
    if bullish >= 6:
        spy_trend = "bullish"
        dxy_trend = "bearish"  # risk-on: dollar weak
        vix_level = "low"
    elif bearish >= 6:
        spy_trend = "bearish"
        dxy_trend = "bullish"  # risk-off: dollar strong
        vix_level = "elevated"
    elif bullish >= 4 and bearish >= 3:
        spy_trend = "neutral"
        vix_level = "normal"
        dxy_trend = "neutral"

    # Volatility regime from momentum dispersion
    momentums = [e.momentum_score for e in board if e.momentum_score > 0]
    if momentums:
        avg_momentum = sum(momentums) / len(momentums)
        if avg_momentum > 70:
            volatility_regime = "high"
        elif avg_momentum > 40:
            volatility_regime = "normal"
        else:
            volatility_regime = "low"
    else:
        volatility_regime = "unknown"

    # BTC dominance — estimate from leaderboard position
    btc = next((e for e in board if e.symbol == "BTC"), None)
    if btc and btc.rank <= 2:
        btc_dominance = 58.0  # BTC leading
    elif btc and btc.rank >= 6:
        btc_dominance = 45.0  # BTC lagging

    # Fear & Greed proxy from confidence dispersion
    confidences = [e.confidence for e in board if e.confidence > 0]
    if confidences:
        avg_conf = sum(confidences) / len(confidences)
        # Higher avg confidence → greed, lower → fear
        fear_greed = int(min(90, max(10, avg_conf)))

    return RegimeEvidence(
        dxy_trend=dxy_trend,
        vix_level=vix_level,
        spy_trend=spy_trend,
        btc_dominance=btc_dominance,
        fear_greed=fear_greed,
        asset_count_bullish=bullish,
        asset_count_bearish=bearish,
        volatility_regime=volatility_regime,
    )


# ── Classification ─────────────────────────────────────────────────────────

def _classify_regime(board, evidence: RegimeEvidence) -> tuple[str, int]:
    """Classify the regime and compute confidence."""
    bullish = evidence.asset_count_bullish
    bearish = evidence.asset_count_bearish
    total = bullish + bearish

    if total == 0:
        return "unknown", 0

    # Leaderboard metrics
    leaders = [e for e in board if e.is_leader]
    laggards = [e for e in board if e.is_laggard]
    avg_leader_conf = sum(l.confidence for l in leaders) / len(leaders) if leaders else 50
    avg_leader_momentum = sum(l.momentum_score for l in leaders) / len(leaders) if leaders else 30

    # ── Panic ─────────────────────────────────────────────────────────
    if bearish >= 7 and bullish <= 1:
        return "panic", 85

    # ── Risk-On ──────────────────────────────────────────────────────
    if bullish >= 6 and avg_leader_conf >= 65 and avg_leader_momentum >= 50:
        return "risk_on", int(min(90, avg_leader_conf + 10))

    # ── Risk-Off ──────────────────────────────────────────────────────
    if bearish >= 5 and avg_leader_conf < 55:
        return "risk_off", int(max(40, 90 - avg_leader_conf))

    # ── Expansion ─────────────────────────────────────────────────────
    if bullish >= 5 and avg_leader_momentum >= 60:
        return "expansion", int(min(85, avg_leader_momentum))

    # ── Recovery ──────────────────────────────────────────────────────
    if bearish <= 2 and bullish >= 4 and avg_leader_momentum > 40 and avg_leader_conf > 55:
        return "recovery", 60

    # ── Compression ───────────────────────────────────────────────────
    if abs(bullish - bearish) <= 2 and total >= 6:
        return "compression", 50

    # ── Distribution ──────────────────────────────────────────────────
    if bullish >= 3 and bearish >= 2 and avg_leader_momentum < 45:
        return "distribution", 45

    # ── Accumulation ──────────────────────────────────────────────────
    if bearish >= 3 and bullish >= 2 and avg_leader_momentum < 50:
        return "accumulation", 40

    # ── Default ───────────────────────────────────────────────────────
    return "compression", 30


# ── Risk score ─────────────────────────────────────────────────────────────

def _compute_risk_score(board, evidence: RegimeEvidence, regime: str) -> int:
    """Compute a risk score 0-100 based on regime and evidence."""
    score = 50  # base

    # Regime-based
    if regime == "panic":
        score += 35
    elif regime == "risk_off":
        score += 20
    elif regime == "recovery":
        score += 10
    elif regime == "risk_on":
        score -= 15
    elif regime == "expansion":
        score -= 10

    # Evidence-based
    if evidence.vix_level in ("elevated", "high"):
        score += 15
    if evidence.dxy_trend == "bullish":
        score += 10
    if evidence.asset_count_bearish > evidence.asset_count_bullish:
        score += 10

    # Leader gap
    leaders = [e for e in board if e.is_leader]
    laggards = [e for e in board if e.is_laggard]
    if leaders and laggards:
        leader_avg = sum(l.confidence for l in leaders) / len(leaders)
        laggard_avg = sum(l.confidence for l in laggards) / len(laggards)
        dispersion = leader_avg - laggard_avg
        if dispersion > 30:
            score += 10  # high dispersion = fragility

    return max(0, min(100, score))


# ── Transition prediction ──────────────────────────────────────────────────

def _predict_transition(regime: str, board, evidence) -> tuple[Optional[str], int]:
    """Predict the next likely regime transition."""
    bullish = evidence.asset_count_bullish
    bearish = evidence.asset_count_bearish
    leaders = [e for e in board if e.is_leader]
    avg_momentum = sum(l.momentum_score for l in leaders) / len(leaders) if leaders else 30

    transitions = {
        "risk_on": ("compression", 30) if avg_momentum < 50 else ("expansion", 50),
        "risk_off": ("recovery", 30) if bullish > bearish else ("panic", 40),
        "expansion": ("risk_on", 40) if avg_momentum > 60 else ("distribution", 35),
        "compression": ("expansion", 40) if bullish > bearish else ("distribution", 35),
        "distribution": ("risk_off", 45) if bearish > bullish else ("compression", 30),
        "accumulation": ("expansion", 50) if bullish > bearish else ("compression", 30),
        "panic": ("recovery", 40) if bullish > bearish else ("risk_off", 50),
        "recovery": ("risk_on", 50) if bullish >= 5 else ("compression", 30),
    }

    next_r, prob = transitions.get(regime, ("unknown", 0))
    return next_r, prob


# ── Narrative ──────────────────────────────────────────────────────────────

def _build_narrative(regime: str, confidence: int, evidence: RegimeEvidence, board) -> str:
    """Generate French narrative for the detected regime."""
    parts = []

    regime_names = {
        "risk_on": "Risk-On",
        "risk_off": "Risk-Off",
        "expansion": "Expansion",
        "compression": "Compression",
        "distribution": "Distribution",
        "accumulation": "Accumulation",
        "panic": "Panique",
        "recovery": "Reprise",
        "unknown": "Indéterminé",
    }
    name = regime_names.get(regime, regime)
    parts.append(f"Régime {name} détecté avec {confidence}% de confiance")

    if evidence.dxy_trend != "unknown":
        dxy_fr = {"bullish": "haussier", "bearish": "baissier", "neutral": "stable"}.get(evidence.dxy_trend, evidence.dxy_trend)
        parts.append(f"DXY {dxy_fr}")

    if evidence.vix_level != "unknown":
        vix_fr = {"low": "bas", "normal": "normal", "elevated": "élevé", "high": "très élevé"}.get(evidence.vix_level, evidence.vix_level)
        parts.append(f"VIX {vix_fr}")

    parts.append(
        f"{evidence.asset_count_bullish} actifs haussiers, "
        f"{evidence.asset_count_bearish} actifs baissiers "
        f"sur {evidence.asset_count_bullish + evidence.asset_count_bearish} suivis"
    )

    if evidence.fear_greed is not None:
        if evidence.fear_greed >= 70:
            parts.append(f"Fear & Greed {evidence.fear_greed} (greed)")
        elif evidence.fear_greed <= 30:
            parts.append(f"Fear & Greed {evidence.fear_greed} (peur)")

    leaders = [e for e in board if e.is_leader]
    if leaders:
        leader_names = [l.symbol for l in leaders[:3]]
        parts.append(f"Leaders: {', '.join(leader_names)}")

    return ". ".join(parts) + "."
