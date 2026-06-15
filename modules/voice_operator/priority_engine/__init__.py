"""
Voice Operator Priority Engine
GO_VOICE_OPERATOR_PRIORITY_ENGINE_01

Deterministic scoring of existing data. No LLM, no trading logic.
Ranks items by: score, confidence, freshness, source quality, risk.
"""
from __future__ import annotations
from typing import Any


def score_priority(
    item: dict,
    *,
    score: float | None = None,
    confidence: float | None = None,
    freshness: str | None = None,
    source_quality: str | None = None,
    risk: float | None = None,
) -> float:
    """Score a single item for priority ranking.

    Weights:
      - score/edge_score: 0.35
      - confidence: 0.25
      - freshness (LIVE > STALE > MARKET_CLOSED): 0.20
      - source_quality (direct > delayed > fallback): 0.15
      - risk (inverted): 0.05

    Returns 0-100 score. Higher = more important to look at.
    """
    total = 0.0

    # Score (0-100)
    s = score if score is not None else item.get("edge_score", item.get("trade_ready", item.get("score", 0)))
    try: s = float(s)
    except: s = 0
    total += min(abs(s), 100) * 0.35

    # Confidence (0-1 or 0-100)
    c = confidence if confidence is not None else item.get("confidence", 0)
    try: c = float(c)
    except: c = 0
    if c <= 1: c *= 100
    total += min(c, 100) * 0.25

    # Freshness
    fresh = freshness or item.get("freshness_state", item.get("freshness", "UNKNOWN"))
    fresh_map = {"LIVE": 100, "live": 100, "fresh": 100, "STALE": 40, "stale": 40, "MARKET_CLOSED": 20, "NO_DATA": 0}
    total += fresh_map.get(str(fresh).upper(), 50) * 0.20

    # Source quality
    sq = source_quality or item.get("source_quality", "unknown")
    sq_map = {"direct": 100, "delayed": 70, "fallback": 40, "synthetic": 20, "unknown": 30}
    total += sq_map.get(str(sq).lower(), 30) * 0.15

    # Risk (inverted — higher risk = lower priority)
    r = risk if risk is not None else item.get("risk", item.get("risk_score", 50))
    try: r = float(r)
    except: r = 50
    total += max(0, 100 - min(r, 100)) * 0.05

    return round(total, 1)


def rank_items(items: list[dict]) -> list[dict]:
    """Rank items by priority score. Returns sorted list with _priority field."""
    for item in items:
        item["_priority"] = score_priority(item)
    return sorted(items, key=lambda x: x.get("_priority", 0), reverse=True)


def rank_setups(setups: list[dict]) -> list[dict]:
    """Rank setup candidates by priority."""
    for s in setups:
        s["_priority"] = score_priority(s)
    return sorted(setups, key=lambda x: x["_priority"], reverse=True)[:3]


def rank_attention(items: list[dict]) -> list[dict]:
    """Find items requiring attention (low scores, stale, risk warnings)."""
    for item in items:
        item["_attention"] = 100 - score_priority(item)  # Invert: low priority = high attention
    return sorted(items, key=lambda x: x.get("_attention", 0), reverse=True)[:3]
