"""
Thesis Engine — PR5.

Main orchestrator: aggregates data, runs all builders, produces a
complete MarketThesis (market_thesis.v1).

This is the canonical entry point for generating a thesis.
No API, no DeskPro, no Voice — pure computation.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from .builders.action_builder import build_action
from .builders.flows_builder import build_flows
from .builders.news_builder import build_news
from .builders.probabilities_builder import build_probabilities
from .builders.risks_builder import build_risks
from .builders.technique_builder import build_technique
from .config import CANONICAL_SYMBOLS
from .context_aggregator import MarketContextInput, aggregate
from .context_builder import build_context
from .models import (
    FreshnessStatus,
    MarketThesis,
    SourceRef,
    ThesisMetadata,
)
from .source_status import SourceStatus


def build_thesis(symbol: str) -> MarketThesis:
    """Build a complete MarketThesis for a single symbol.

    Args:
        symbol: Canonical symbol (BTC, ETH, SOL, XRP, XAU, SPCX, NVDA, AVGO, MU)

    Returns:
        A fully populated MarketThesis with all sections.
        Missing data produces sections with defaults, never crashes.
    """
    now = datetime.now(timezone.utc)

    # ── Aggregate raw data ─────────────────────────────────────────────
    ctx = aggregate(symbol)

    # ── Build all sections ─────────────────────────────────────────────
    context = build_context(ctx)
    technique = build_technique(ctx)
    flows = build_flows(ctx)
    news = build_news(ctx)
    risks = build_risks(ctx)
    probabilities = build_probabilities(ctx)

    # ── Build action ───────────────────────────────────────────────────
    has_high_risk = any(r.severity == "high" for r in risks)
    has_setups = bool(technique.active_setups)

    action = build_action(
        ctx,
        htf_bias=technique.htf_bias,
        ltf_bias=technique.ltf_bias,
        alignment=technique.alignment,
        probability_bull=probabilities.bull,
        probability_bear=probabilities.bear,
        has_setups=has_setups,
        has_high_risk=has_high_risk,
    )

    # ── Build sources ──────────────────────────────────────────────────
    sources = _build_sources(ctx.source_statuses)

    # ── Build freshness ────────────────────────────────────────────────
    freshness = _build_freshness(ctx, now)

    # ── Compute confidence ─────────────────────────────────────────────
    confidence = _compute_confidence(
        technique=technique,
        flows=flows,
        probabilities=probabilities,
        risks=risks,
        source_statuses=ctx.source_statuses,
    )

    # ── Assemble ───────────────────────────────────────────────────────
    thesis_id = f"thesis_{symbol}_{now.strftime('%Y%m%dT%H%M%SZ')}"

    return MarketThesis(
        metadata=ThesisMetadata(
            thesis_id=thesis_id,
            generated_at=now,
        ),
        symbol=symbol,
        context=context,
        technical=technique,
        flow=flows,
        news=news,
        risks=risks,
        probabilities=probabilities,
        action=action,
        sources=sources,
        freshness=freshness,
        confidence=confidence,
    )


def build_all() -> List[MarketThesis]:
    """Build theses for all 9 canonical symbols."""
    return [build_thesis(sym) for sym in CANONICAL_SYMBOLS]


# ── Helpers ────────────────────────────────────────────────────────────────

def _build_sources(statuses: List[SourceStatus]) -> List[SourceRef]:
    refs: List[SourceRef] = []
    for s in statuses:
        # Map SourceStatus.state to SourceRef.status literal
        state = s.state
        if state in ("fresh", "warm"):
            ref_state = "used"
        elif state in ("stale", "expired"):
            ref_state = "stale"
        elif state == "error":
            ref_state = "missing"
        else:
            ref_state = "missing"

        refs.append(SourceRef(
            name=s.name,
            contract=s.contract,
            status=ref_state,  # type: ignore[arg-type]
            age_minutes=s.age_minutes,
        ))
    return refs


def _build_freshness(ctx: MarketContextInput, now: datetime) -> FreshnessStatus:
    max_age = 0.0
    fresh_count = 0
    for s in ctx.source_statuses:
        if s.state in ("fresh", "warm"):
            fresh_count += 1
        if s.age_minutes is not None and s.age_minutes > max_age:
            max_age = s.age_minutes

    # Map freshness_summary to FreshnessStatus literal
    summary = ctx.freshness_summary
    if summary == "warm":
        overall = "fresh"
    elif summary == "missing":
        overall = "stale"
    elif summary in ("fresh", "stale", "partial", "expired"):
        overall = summary
    else:
        overall = "stale"

    return FreshnessStatus(
        overall=overall,  # type: ignore[arg-type]
        max_age_minutes=max_age,
        source_count=len(ctx.source_statuses),
        fresh_count=fresh_count,
    )


def _compute_confidence(
    technique,
    flows,
    probabilities,
    risks,
    source_statuses: List[SourceStatus],
) -> int:
    """Compute overall thesis confidence (0-100)."""
    score = 50.0  # base

    # Source availability: up to +20
    total = len(source_statuses) or 1
    available = sum(1 for s in source_statuses if s.state not in ("missing", "error"))
    score += (available / total) * 20

    # Setup quality: up to +15
    if technique.active_setups:
        score += min(15, len(technique.active_setups) * 5)

    # Probability conviction: up to +10
    max_prob = max(probabilities.bull, probabilities.range, probabilities.bear)
    if max_prob >= 60:
        score += 10
    elif max_prob >= 45:
        score += 5

    # Risk penalty: up to -15
    high_risks = sum(1 for r in risks if r.severity == "high")
    score -= min(15, high_risks * 5)

    # Alignment bonus: up to +5
    if technique.alignment in ("aligned_bullish", "aligned_bearish"):
        score += 5

    return max(0, min(100, int(round(score))))
