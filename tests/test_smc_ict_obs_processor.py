import json
import pytest
from modules.smc_ict_obs_processor.app.smc_ict_obs_processor import (
    score_confidence,
    build_obs_event,
    from_summary_json,
)


# ---- score_confidence ----

def test_score_full_setup_high():
    detail = {
        "choch_observed": True, "mss_observed": True,
        "htf_alignment_confirmed": True, "htf_alignment_4h_confirmed": True,
        "sweep_observed": True, "sweep_type": "PDH_sweep",
        "sweep_htf_confirmed": True, "sweep_fast_return": True,
        "fvg_valid": True, "fvg_retest_confirmed": True,
        "ob_valid": True, "fvg_ob_confluence": True,
        "ote_zone_active": True, "premium_discount_filter": "DISCOUNT",
    }
    assert score_confidence(detail) >= 0.80


def test_score_bos_only_low():
    assert score_confidence({"bos_observed": True}) < 0.30


def test_score_choch_fvg_pd_medium():
    detail = {"choch_observed": True, "fvg_valid": True, "premium_discount_filter": "DISCOUNT"}
    s = score_confidence(detail)
    assert 0.35 <= s <= 0.55


def test_score_capped_at_1():
    detail = {
        "choch_observed": True, "mss_observed": True,
        "htf_alignment_confirmed": True, "htf_alignment_4h_confirmed": True,
        "sweep_observed": True, "sweep_type": "PDH_sweep",
        "sweep_htf_confirmed": True, "sweep_fast_return": True,
        "fvg_valid": True, "fvg_retest_confirmed": True,
        "ob_valid": True, "fvg_ob_confluence": True,
        "ote_zone_active": True, "premium_discount_filter": "DISCOUNT",
    }
    assert score_confidence(detail) <= 1.0


def test_score_empty_zero():
    assert score_confidence({}) == 0.0


def test_score_eq_filter_no_pd_bonus():
    detail = {"choch_observed": True, "premium_discount_filter": "EQ"}
    without = score_confidence({"choch_observed": True})
    with_eq = score_confidence(detail)
    assert with_eq == without


def test_score_pdh_sweep_higher_than_bsl():
    pdh = score_confidence({"choch_observed": True, "sweep_observed": True, "sweep_type": "PDH_sweep"})
    bsl = score_confidence({"choch_observed": True, "sweep_observed": True, "sweep_type": "BSL_sweep"})
    assert pdh > bsl


# ---- build_obs_event ----

def _min_detail():
    return {"choch_observed": True, "bos_observed": False}


def test_build_valid_event():
    ev = build_obs_event(_min_detail(), "LONG_WATCH", "close_below_swing_low")
    assert ev["strategy"]["strategy_id"] == "SMC_ICT_CHOCH_BOS_RETEST"
    assert ev["signal"]["direction"] == "LONG_WATCH"
    assert ev["signal"]["symbol"] == "BTCUSDT"


def test_build_requires_choch_or_bos():
    with pytest.raises(ValueError, match="choch_observed or bos_observed"):
        build_obs_event({"choch_observed": False, "bos_observed": False}, "LONG_WATCH", "inv")


def test_build_requires_invalidation():
    with pytest.raises(ValueError, match="invalidation_rule"):
        build_obs_event(_min_detail(), "LONG_WATCH", "")


def test_build_confidence_nonzero():
    ev = build_obs_event(_min_detail(), "LONG_WATCH", "inv")
    assert 0.0 < ev["signal"]["confidence"] <= 1.0


def test_build_gates_active_paper():
    ev = build_obs_event(_min_detail(), "LONG_WATCH", "inv")
    assert ev["gates"]["observation_status"] == "ACTIVE_PAPER"
    assert ev["gates"]["perf_status"] == "UNMEASURED"


def test_build_risk_profile_paper_only():
    ev = build_obs_event(_min_detail(), "LONG_WATCH", "inv")
    assert ev["trade_plan"]["risk_profile"] == "paper_only"


def test_build_direction_uppercased():
    ev = build_obs_event(_min_detail(), "long_watch", "inv")
    assert ev["signal"]["direction"] == "LONG_WATCH"


# ---- from_summary_json ----

def test_from_summary_valid(tmp_path):
    summary = {"run_id": "run_abc123", "ts": "2026-05-30T10:00:00Z", "signals": {}}
    p = tmp_path / "summary.json"
    p.write_text(json.dumps(summary))
    ev = from_summary_json(str(p), _min_detail(), "LONG_WATCH", "close_below_swing")
    assert ev["run_id"] == "run_abc123"
    assert ev["signal"]["signal_source"] == "bot_vision"


def test_from_summary_missing_file():
    with pytest.raises(FileNotFoundError):
        from_summary_json("/nonexistent/summary.json", _min_detail(), "LONG_WATCH", "inv")


def test_from_summary_evidence_includes_path(tmp_path):
    p = tmp_path / "summary.json"
    p.write_text(json.dumps({"run_id": "r1"}))
    ev = from_summary_json(str(p), _min_detail(), "LONG_WATCH", "inv")
    types = [e["type"] for e in ev["evidence"]]
    assert "vision_summary" in types
