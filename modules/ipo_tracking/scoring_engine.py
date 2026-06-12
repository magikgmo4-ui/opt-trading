from __future__ import annotations
from typing import Any

from .io import utc_now

WEIGHTS = {
    "momentum": 0.20,
    "technical": 0.25,
    "fundamental": 0.20,
    "sentiment": 0.15,
    "risk": -0.20,
    "accumulation": 0.20,
}


def compute_composite_score(
    snapshot: dict[str, Any],
    accumulation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scores = snapshot.get("scores", {})

    momentum = scores.get("momentum", 0)
    technical = scores.get("smart_money", 0) * 0.5 + (scores.get("trade_ready", 0) or 0) * 0.5
    fundamental = scores.get("sec_activity", 0)
    sentiment = scores.get("news_velocity", 0)
    risk = scores.get("risk", 0)
    acc = accumulation.get("accumulation_score", 0.5) if accumulation else 0.5

    composite = (
        momentum * WEIGHTS["momentum"]
        + technical * WEIGHTS["technical"]
        + fundamental * WEIGHTS["fundamental"]
        + sentiment * WEIGHTS["sentiment"]
        - risk * abs(WEIGHTS["risk"])
        + acc * WEIGHTS["accumulation"]
    )

    return {
        "computed_at": utc_now(),
        "dimensions": {
            "momentum": {"raw": round(momentum, 3), "weighted": round(momentum * WEIGHTS["momentum"], 3)},
            "technical": {"raw": round(technical, 3), "weighted": round(technical * WEIGHTS["technical"], 3)},
            "fundamental": {"raw": round(fundamental, 3), "weighted": round(fundamental * WEIGHTS["fundamental"], 3)},
            "sentiment": {"raw": round(sentiment, 3), "weighted": round(sentiment * WEIGHTS["sentiment"], 3)},
            "risk": {"raw": round(risk, 3), "penalty": round(risk * abs(WEIGHTS["risk"]), 3)},
            "accumulation": {"raw": round(acc, 3), "weighted": round(acc * WEIGHTS["accumulation"], 3)},
        },
        "composite_score": round(max(0, min(1, composite)), 3),
        "rating": _rating(composite),
        "trade_confidence": _confidence(composite),
    }


def _rating(score: float) -> str:
    if score >= 0.85:
        return "A+"
    if score >= 0.75:
        return "A"
    if score >= 0.65:
        return "B+"
    if score >= 0.50:
        return "B"
    if score >= 0.35:
        return "C"
    return "D"


def _confidence(score: float) -> str:
    if score >= 0.80:
        return "HIGH_CONVICTION"
    if score >= 0.60:
        return "MODERATE_CONVICTION"
    if score >= 0.40:
        return "LOW_CONVICTION"
    return "NO_CONVICTION"
