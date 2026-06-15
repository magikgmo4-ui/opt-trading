from __future__ import annotations

from datetime import datetime, timezone

from modules.stock_true_value.scoring_engine import (
    assign_action_bias,
    assign_grade,
    clamp_score,
    compute_final_score,
    compute_hype_score,
    compute_risk_score,
    compute_score_snapshot,
    compute_true_value_score,
    weighted_average,
)


def test_clamp_score_bounds() -> None:
    assert clamp_score(-10) == 0.0
    assert clamp_score(120) == 100.0
    assert clamp_score(55.555) == 55.55
    assert clamp_score(None) == 50.0


def test_weighted_average_skips_missing_and_renormalizes() -> None:
    assert weighted_average({"a": 100, "b": None, "c": 50}, {"a": 0.25, "b": 0.50, "c": 0.25}) == 75.0


def test_compute_true_value_score_expected_value() -> None:
    assert compute_true_value_score(92, 48, 82, 88) == 74.5


def test_compute_hype_score_composite() -> None:
    assert compute_hype_score(70, 90, 80) == 76.0


def test_compute_risk_score_includes_confidence_penalty() -> None:
    assert compute_risk_score(80, 70, 50, 25) == 63.25


def test_compute_final_score_spacex_context() -> None:
    score = compute_final_score(
        true_value_score=70,
        risk_score=50,
        surprise_score=80,
        catalyst_score=90,
        ecosystem_score=85,
        spacex_context=True,
    )
    assert score == 76.5


def test_grade_matrix() -> None:
    assert assign_grade(88, 60, 80) == "A+"
    assert assign_grade(80, 75, 80) == "A"
    assert assign_grade(65, 75, 80) == "B"
    assert assign_grade(50, 75, 80) == "C"
    assert assign_grade(30, 75, 80) == "D"
    assert assign_grade(90, 20, 50) == "RESEARCH_REQUIRED"


def test_action_bias() -> None:
    assert assign_action_bias(85, 50, 60, 80) == "accumulation_candidate"
    assert assign_action_bias(85, 80, 60, 80) == "watch_for_pullback"
    assert assign_action_bias(55, 90, 60, 80) == "avoid_chasing"
    assert assign_action_bias(75, 55, 60, 50) == "deep_research_required"


def test_compute_score_snapshot_spcx_special_case() -> None:
    snapshot = compute_score_snapshot(
        ticker="SPCX",
        universe="CORE_SPACE",
        raw_scores={
            "fundamental_score": 50,
            "valuation_score": None,
            "flow_score": 80,
            "speculation_score": 90,
            "surprise_score": 70,
            "catalyst_score": 92,
            "ecosystem_score": 88,
        },
        source_health_payload={
            "required_sources_available": 2,
            "required_sources_total": 4,
            "optional_sources_available": 1,
            "missing_sources": ["valuation_ratios", "official_listing_status"],
            "stale_sources": [],
            "data_conflicts": [],
        },
        asof=datetime(2026, 6, 15, 12, 30, tzinfo=timezone.utc),
    )
    payload = snapshot.to_dict()
    assert payload["ticker"] == "SPCX"
    assert payload["confidence_score"] == 50.0
    assert payload["final_grade"] == "RESEARCH_REQUIRED"
    assert "LOW_CONFIDENCE_SCORE" in payload["flags"]
    assert "MISSING_SOURCES" in payload["flags"]
    assert "SPCX_SPECIAL_CASE_VERIFY_LISTING_STATUS" in payload["flags"]
