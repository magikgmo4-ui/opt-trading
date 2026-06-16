"""
News builder — PR4.

Builds the NewsSection from MarketContextInput.
Aggregates sentiment from news, telegram, CDP signals.
Never crashes — uses defaults for missing data.
"""

from __future__ import annotations

from typing import List

from ..context_aggregator import MarketContextInput
from ..models import NewsSection
from ..narrative import news_narrative


def build_news(ctx: MarketContextInput) -> NewsSection:
    """Build a NewsSection from aggregated data."""

    sentiment = "unknown"
    sentiment_score = 0.0
    key_drivers: List[str] = []

    # ── Aggregate from telegram signals ─────────────────────────────────
    tg_signals = ctx.telegram_inputs
    tg_buy = sum(1 for s in tg_signals if s.direction.upper() in ("LONG", "BUY"))
    tg_sell = sum(1 for s in tg_signals if s.direction.upper() in ("SHORT", "SELL"))

    # ── Aggregate from CDP events ──────────────────────────────────────
    cdp_events = [e for e in ctx.news_inputs if e.source == "cdp"]
    cdp_up = sum(1 for e in cdp_events if e.event_type in (
        "VWAP_RECLAIM", "ORB_HIGH_BREAK", "BOS_BULL", "CHOCH_BULL",
        "TREND_CONTINUATION", "SUPPORT_TEST",
    ))
    cdp_down = sum(1 for e in cdp_events if e.event_type in (
        "VWAP_LOSS", "ORB_LOW_BREAK", "BOS_BEAR", "CHOCH_BEAR",
        "TREND_REVERSAL", "RESISTANCE_TEST",
    ))

    # ── Aggregate from webhook events ──────────────────────────────────
    wh_events = [e for e in ctx.raw_events if e.source == "webhook"]
    wh_buy = sum(1 for e in wh_events if e.direction.upper() in ("BUY", "LONG"))
    wh_sell = sum(1 for e in wh_events if e.direction.upper() in ("SELL", "SHORT"))

    # ── Aggregate from vision analysis ─────────────────────────────────
    for v in ctx.vision_inputs:
        if v.analysis_summary:
            summary_lower = v.analysis_summary.lower()
            if "bullish" in summary_lower:
                sentiment_score += 0.2
            if "bearish" in summary_lower:
                sentiment_score -= 0.2
            if "consolidation" in summary_lower or "range" in summary_lower:
                sentiment_score *= 0.8  # dampen

    # ── Compute sentiment from signal counts ───────────────────────────
    total_bullish = tg_buy + cdp_up + wh_buy
    total_bearish = tg_sell + cdp_down + wh_sell
    total_signals = total_bullish + total_bearish

    if total_signals > 0:
        signal_sentiment = (total_bullish - total_bearish) / total_signals
        sentiment_score += signal_sentiment * 0.5

    # ── Clamp sentiment score ──────────────────────────────────────────
    sentiment_score = max(-1.0, min(1.0, sentiment_score))

    # ── Determine overall sentiment ────────────────────────────────────
    if sentiment_score > 0.3:
        sentiment = "positive"
    elif sentiment_score < -0.3:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # ── Key drivers ────────────────────────────────────────────────────
    # From signal events
    for e in wh_events[:3]:
        if e.raw_reason:
            key_drivers.append(e.raw_reason[:100])

    # From CDP events
    for e in cdp_events[:3]:
        event_name = e.event_type.replace("_", " ").title()
        key_drivers.append(f"CDP {event_name}")

    # From telegram
    for e in tg_signals[:2]:
        if e.raw_reason:
            key_drivers.append(f"TG: {e.raw_reason[:80]}")

    # From setups
    for s in ctx.priority_inputs[:2]:
        for reason in s.reasons[:1]:
            key_drivers.append(reason[:100])

    # Deduplicate and cap
    seen = set()
    unique_drivers = []
    for d in key_drivers:
        if d not in seen:
            seen.add(d)
            unique_drivers.append(d)
    key_drivers = unique_drivers[:5]

    # ── Narrative ───────────────────────────────────────────────────────
    narrative = news_narrative(
        sentiment=sentiment,
        sentiment_score=sentiment_score,
        key_drivers=key_drivers,
        total_signals=total_signals,
        tg_count=len(tg_signals),
        cdp_count=len(cdp_events),
    )

    return NewsSection(
        sentiment=sentiment,  # type: ignore[arg-type]
        sentiment_score=sentiment_score,
        key_drivers=key_drivers,
        narrative=narrative,
    )
