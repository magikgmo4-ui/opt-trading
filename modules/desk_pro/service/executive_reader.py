"""
DeskPro Executive Reader — PR7.

Read-only bridge between DeskPro and Executive Intelligence.
No business logic. No recalculation. Pure pass-through.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def get_executive() -> Optional[Dict[str, Any]]:
    try:
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        return {
            "briefing_id": brief.briefing_id,
            "generated_at": brief.generated_at.isoformat(),
            "market_regime": brief.market_regime,
            "regime_confidence": brief.regime_confidence,
            "overall_confidence": brief.overall_confidence,
            "leaders": brief.leaders,
            "laggards": brief.laggards,
            "summary": brief.summary,
            "what_changed": brief.what_changed,
            "what_to_watch": brief.what_to_watch,
            "top_risks": brief.top_risks,
            "top_opportunities": brief.top_opportunities,
            "voice_one_liner": brief.voice_one_liner,
            "voice_briefing": brief.voice_briefing,
        }
    except Exception:
        return None


def get_executive_regime() -> Optional[Dict[str, Any]]:
    try:
        from modules.executive_intelligence.regime_engine import detect_regime
        r = detect_regime()
        return {
            "regime": r.regime,
            "confidence": r.confidence,
            "risk_score": r.risk_score,
            "narrative": r.narrative,
            "dxy_trend": r.evidence.dxy_trend,
            "vix_level": r.evidence.vix_level,
            "spy_trend": r.evidence.spy_trend,
            "fear_greed": r.evidence.fear_greed,
            "bullish_count": r.evidence.asset_count_bullish,
            "bearish_count": r.evidence.asset_count_bearish,
        }
    except Exception:
        return None


def get_executive_leaders() -> Optional[Dict[str, Any]]:
    try:
        from modules.executive_intelligence.cross_asset_engine import build_leaderboard, compute_influences
        board = build_leaderboard()
        infs = compute_influences()
        return {
            "leaders": [{"symbol": e.symbol, "rank": e.rank, "direction": e.direction, "confidence": e.confidence, "momentum": e.momentum_score} for e in board if e.is_leader],
            "laggards": [{"symbol": e.symbol, "rank": e.rank, "direction": e.direction, "confidence": e.confidence, "momentum": e.momentum_score} for e in board if e.is_laggard],
            "full_board": [{"symbol": e.symbol, "rank": e.rank, "direction": e.direction, "confidence": e.confidence, "momentum": e.momentum_score} for e in board],
            "cross_asset": [f"{i.source}→{i.target}: {i.direction} ({i.influence_score})" for i in infs[:6]],
        }
    except Exception:
        return None


def get_executive_risks() -> Optional[Dict[str, Any]]:
    try:
        from modules.executive_intelligence.briefing_engine import build_briefing
        from modules.executive_intelligence.regime_engine import detect_regime
        brief = build_briefing()
        regime = detect_regime()
        return {
            "top_risks": brief.top_risks,
            "regime_risk": regime.risk_score,
            "regime_risk_label": "high" if regime.risk_score >= 70 else "moderate" if regime.risk_score >= 40 else "low",
        }
    except Exception:
        return None
