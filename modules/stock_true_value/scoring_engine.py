"""Pure scoring functions for SpaceX True Value Final.

No live collectors. No broker/order integration. No active Data Center writes.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .models import ScoreSnapshot, SourceHealth

MODEL_VERSION = "spacex_true_value_final_v1"


def clamp_score(value: float | int | None, default: float = 50.0) -> float:
    if value is None:
        return default
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return default
    return round(max(0.0, min(100.0, numeric)), 2)


def weighted_average(values: dict[str, float | None], weights: dict[str, float]) -> float:
    numerator = 0.0
    denominator = 0.0
    for key, weight in weights.items():
        if values.get(key) is None:
            continue
        numerator += clamp_score(values[key]) * weight
        denominator += weight
    if denominator <= 0:
        return 50.0
    return round(numerator / denominator, 2)


def compute_true_value_score(
    fundamental_score: float | None,
    valuation_score: float | None,
    flow_score: float | None,
    surprise_score: float | None,
) -> float:
    return weighted_average(
        {
            "fundamental_score": fundamental_score,
            "valuation_score": valuation_score,
            "flow_score": flow_score,
            "surprise_score": surprise_score,
        },
        {
            "fundamental_score": 0.35,
            "valuation_score": 0.35,
            "flow_score": 0.15,
            "surprise_score": 0.15,
        },
    )


def compute_hype_score(
    speculation_score: float | None,
    social_trend_score: float | None = None,
    options_pressure_score: float | None = None,
) -> float:
    if social_trend_score is None and options_pressure_score is None:
        return clamp_score(speculation_score)
    return weighted_average(
        {
            "speculation_score": speculation_score,
            "social_trend_score": social_trend_score,
            "options_pressure_score": options_pressure_score,
        },
        {
            "speculation_score": 0.60,
            "social_trend_score": 0.20,
            "options_pressure_score": 0.20,
        },
    )


def compute_risk_score(
    hype_score: float,
    valuation_overextension_risk: float | None = None,
    earnings_event_risk: float | None = None,
    data_confidence_penalty: float | None = None,
) -> float:
    return weighted_average(
        {
            "hype_score": hype_score,
            "valuation_overextension_risk": valuation_overextension_risk,
            "earnings_event_risk": earnings_event_risk,
            "data_confidence_penalty": data_confidence_penalty,
        },
        {
            "hype_score": 0.40,
            "valuation_overextension_risk": 0.25,
            "earnings_event_risk": 0.20,
            "data_confidence_penalty": 0.15,
        },
    )


def compute_confidence_score(
    required_sources_available: int,
    required_sources_total: int,
    stale_sources_count: int = 0,
    data_conflicts_count: int = 0,
) -> float:
    if required_sources_total <= 0:
        coverage = 50.0
    else:
        coverage = 100.0 * required_sources_available / required_sources_total
    freshness_penalty = min(30.0, stale_sources_count * 10.0)
    conflict_penalty = min(20.0, data_conflicts_count * 10.0)
    return round(max(0.0, min(100.0, coverage - freshness_penalty - conflict_penalty)), 2)


def compute_final_score(
    true_value_score: float,
    risk_score: float,
    surprise_score: float | None = None,
    flow_score: float | None = None,
    catalyst_score: float | None = None,
    ecosystem_score: float | None = None,
    spacex_context: bool = False,
) -> float:
    inverse_risk = 100.0 - clamp_score(risk_score)
    if spacex_context:
        return weighted_average(
            {
                "catalyst_score": catalyst_score,
                "ecosystem_score": ecosystem_score,
                "true_value_score": true_value_score,
                "surprise_score": surprise_score,
                "inverse_risk_score": inverse_risk,
            },
            {
                "catalyst_score": 0.25,
                "ecosystem_score": 0.20,
                "true_value_score": 0.25,
                "surprise_score": 0.15,
                "inverse_risk_score": 0.15,
            },
        )
    return weighted_average(
        {
            "true_value_score": true_value_score,
            "flow_score": flow_score,
            "surprise_score": surprise_score,
            "inverse_risk_score": inverse_risk,
        },
        {
            "true_value_score": 0.45,
            "flow_score": 0.20,
            "surprise_score": 0.20,
            "inverse_risk_score": 0.15,
        },
    )


def assign_grade(final_score: float, risk_score: float, confidence_score: float) -> str:
    if confidence_score < 60:
        return "RESEARCH_REQUIRED"
    if final_score >= 85 and risk_score <= 70 and confidence_score >= 70:
        return "A+"
    if final_score >= 75 and confidence_score >= 65:
        return "A"
    if final_score >= 60:
        return "B"
    if final_score >= 45:
        return "C"
    return "D"


def assign_action_bias(true_value_score: float, hype_score: float, risk_score: float, confidence_score: float) -> str:
    if confidence_score < 60:
        return "deep_research_required"
    if true_value_score >= 80 and hype_score <= 65 and risk_score <= 65:
        return "accumulation_candidate"
    if true_value_score >= 80 and hype_score > 75:
        return "watch_for_pullback"
    if true_value_score < 60 and hype_score > 80:
        return "avoid_chasing"
    if risk_score >= 80:
        return "risk_high_monitor_only"
    return "watchlist_monitor"


def compute_score_snapshot(
    ticker: str,
    universe: str,
    raw_scores: dict[str, float | None],
    source_health_payload: dict[str, Any] | None = None,
    asof: datetime | None = None,
) -> ScoreSnapshot:
    asof = asof or datetime.now(timezone.utc)
    source_health_payload = source_health_payload or {}

    fundamental_score = raw_scores.get("fundamental_score")
    valuation_score = raw_scores.get("valuation_score")
    flow_score = raw_scores.get("flow_score")
    speculation_score = raw_scores.get("speculation_score")
    surprise_score = raw_scores.get("surprise_score")
    catalyst_score = raw_scores.get("catalyst_score")
    ecosystem_score = raw_scores.get("ecosystem_score")

    true_value_score = compute_true_value_score(fundamental_score, valuation_score, flow_score, surprise_score)
    hype_score = compute_hype_score(
        speculation_score,
        raw_scores.get("social_trend_score"),
        raw_scores.get("options_pressure_score"),
    )

    required_available = int(source_health_payload.get("required_sources_available", 0))
    required_total = int(source_health_payload.get("required_sources_total", max(1, required_available)))
    missing_sources = tuple(source_health_payload.get("missing_sources", ()))
    stale_sources = tuple(source_health_payload.get("stale_sources", ()))
    data_conflicts = tuple(source_health_payload.get("data_conflicts", ()))

    confidence_score = compute_confidence_score(
        required_sources_available=required_available,
        required_sources_total=required_total,
        stale_sources_count=len(stale_sources),
        data_conflicts_count=len(data_conflicts),
    )
    risk_score = compute_risk_score(
        hype_score=hype_score,
        valuation_overextension_risk=raw_scores.get("valuation_overextension_risk"),
        earnings_event_risk=raw_scores.get("earnings_event_risk"),
        data_confidence_penalty=100.0 - confidence_score,
    )
    spacex_context = ticker.upper() == "SPCX" or universe in {"CORE_SPACE", "CORE_WATCHLIST_PRIORITY"}
    final_score = compute_final_score(
        true_value_score=true_value_score,
        risk_score=risk_score,
        surprise_score=surprise_score,
        flow_score=flow_score,
        catalyst_score=catalyst_score,
        ecosystem_score=ecosystem_score,
        spacex_context=spacex_context,
    )

    flags: list[str] = []
    if confidence_score < 60:
        flags.append("LOW_CONFIDENCE_SCORE")
    if hype_score >= 85:
        flags.append("EXTREME_HYPE")
    if missing_sources:
        flags.append("MISSING_SOURCES")
    if stale_sources:
        flags.append("STALE_SOURCES")
    if data_conflicts:
        flags.append("SOURCE_CONFLICT")
    if ticker.upper() == "SPCX":
        flags.append("SPCX_SPECIAL_CASE_VERIFY_LISTING_STATUS")

    return ScoreSnapshot(
        ticker=ticker.upper(),
        asof=asof,
        model_version=MODEL_VERSION,
        universe=universe,
        fundamental_score=clamp_score(fundamental_score) if fundamental_score is not None else None,
        valuation_score=clamp_score(valuation_score) if valuation_score is not None else None,
        flow_score=clamp_score(flow_score) if flow_score is not None else None,
        speculation_score=clamp_score(speculation_score) if speculation_score is not None else None,
        surprise_score=clamp_score(surprise_score) if surprise_score is not None else None,
        catalyst_score=clamp_score(catalyst_score) if catalyst_score is not None else None,
        ecosystem_score=clamp_score(ecosystem_score) if ecosystem_score is not None else None,
        true_value_score=true_value_score,
        hype_score=hype_score,
        risk_score=risk_score,
        confidence_score=confidence_score,
        final_score=final_score,
        final_grade=assign_grade(final_score, risk_score, confidence_score),
        action_bias=assign_action_bias(true_value_score, hype_score, risk_score, confidence_score),
        flags=tuple(flags),
        source_health=SourceHealth(
            required_sources_available=required_available,
            optional_sources_available=int(source_health_payload.get("optional_sources_available", 0)),
            missing_sources=missing_sources,
            stale_sources=stale_sources,
            data_conflicts=data_conflicts,
        ),
    )
