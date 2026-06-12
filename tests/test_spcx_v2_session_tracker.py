"""Tests for SPCX V2 session tracker — counter, validation, graduation."""

import pytest
from pathlib import Path

from modules.spcx_v2.config import SetupCandidate, ScoreSet
from modules.spcx_v2.paper_logger import log_candidate, log_result


@pytest.fixture(autouse=True)
def temp_dirs(monkeypatch, tmp_path):
    monkeypatch.setattr("modules.spcx_v2.paper_logger.OUTPUT_DIR", tmp_path)
    monkeypatch.setattr("modules.spcx_v2.config.OUTPUT_DIR", tmp_path)
    monkeypatch.setattr("modules.spcx_v2.session_tracker.SESSION_FILE", tmp_path / "session_counter.json")
    monkeypatch.setattr("modules.spcx_v2.session_tracker.GRADUATION_FILE", tmp_path / "graduation.json")
    monkeypatch.setattr("modules.spcx_v2.session_tracker.PROJECT_ROOT", tmp_path)
    return tmp_path


def make_candidate(grade="A", setup_type="IPO_ORB_5M"):
    return SetupCandidate(
        symbol="SPCX",
        ts="t",
        setup_type=setup_type,
        grade=grade,
        status="paper_only",
        scores=ScoreSet(trade_ready=78, liquidity=72, risk=38, smart_money=70, catalyst=65),
    )


# ── Session counter ──────────────────────────────────────────────────
def test_bump_session(tmp_path):
    from modules.spcx_v2.session_tracker import get_session_count, bump_session
    assert get_session_count() == 0
    n = bump_session()
    assert n == 1
    assert get_session_count() == 1


def test_bump_session_multiple(tmp_path):
    from modules.spcx_v2.session_tracker import bump_session, get_session_count
    for i in range(5):
        n = bump_session()
        assert n == i + 1
    assert get_session_count() == 5


def test_bump_session_count_persistence(tmp_path):
    from modules.spcx_v2.session_tracker import bump_session, SESSION_FILE
    n1 = bump_session()
    n2 = bump_session()
    n3 = bump_session()
    assert n3 == 3
    assert SESSION_FILE.exists()


# ── Setup validation ─────────────────────────────────────────────────
def test_validate_setup_pass(monkeypatch, tmp_path):
    def mock_stats(candidates):
        return {"IPO_ORB_5M": {"total_trades": 10, "winrate": 55.0, "expectancy_R": 0.5, "profit_factor": 1.8}}
    monkeypatch.setattr("modules.spcx_v2.session_tracker.compute_stats_by_setup", mock_stats)
    monkeypatch.setattr("modules.spcx_v2.session_tracker.compute_stats_by_grade", lambda *a, **kw: {})

    from modules.spcx_v2.session_tracker import validate_setup
    result = validate_setup("IPO_ORB_5M", [])
    assert result["passed"] is True
    assert result["checks"]["enough_trades"] is True
    assert result["checks"]["winrate_ok"] is True
    assert result["checks"]["expectancy_ok"] is True
    assert result["checks"]["profit_factor_ok"] is True


def test_validate_setup_fail_winrate(monkeypatch, tmp_path):
    def mock_stats(candidates):
        return {"IPO_ORB_5M": {"total_trades": 10, "winrate": 30.0, "expectancy_R": -0.2, "profit_factor": 0.5}}
    monkeypatch.setattr("modules.spcx_v2.session_tracker.compute_stats_by_setup", mock_stats)

    from modules.spcx_v2.session_tracker import validate_setup
    result = validate_setup("IPO_ORB_5M", [])
    assert result["passed"] is False
    assert result["checks"]["winrate_ok"] is False


def test_validate_setup_insufficient_trades(monkeypatch, tmp_path):
    def mock_stats(candidates):
        return {"IPO_ORB_5M": {"total_trades": 2, "winrate": 60.0, "expectancy_R": 1.0, "profit_factor": 2.0}}
    monkeypatch.setattr("modules.spcx_v2.session_tracker.compute_stats_by_setup", mock_stats)

    from modules.spcx_v2.session_tracker import validate_setup
    result = validate_setup("IPO_ORB_5M", [])
    assert result["passed"] is False
    assert result["checks"]["enough_trades"] is False


def test_validate_setup_default_threshold(monkeypatch, tmp_path):
    def mock_stats(candidates):
        return {"UNKNOWN_SETUP": {"total_trades": 3, "winrate": 40.0, "expectancy_R": 0.2, "profit_factor": 1.2}}
    monkeypatch.setattr("modules.spcx_v2.session_tracker.compute_stats_by_setup", mock_stats)

    from modules.spcx_v2.session_tracker import validate_setup
    result = validate_setup("UNKNOWN_SETUP", [])
    assert result["passed"] is True
    assert result["metrics"]["trades"] == 3


def test_validate_setup_expectancy_zero(monkeypatch, tmp_path):
    def mock_stats(candidates):
        return {"VWAP_HOLD_LONG": {"total_trades": 5, "winrate": 45.0, "expectancy_R": 0.0, "profit_factor": 1.0}}
    monkeypatch.setattr("modules.spcx_v2.session_tracker.compute_stats_by_setup", mock_stats)

    from modules.spcx_v2.session_tracker import validate_setup
    result = validate_setup("VWAP_HOLD_LONG", [])
    assert result["passed"] is False
    assert result["checks"]["expectancy_ok"] is False


# ── Graduation report ────────────────────────────────────────────────
def test_graduation_report(monkeypatch, tmp_path):
    def mock_stats(candidates):
        return {"IPO_ORB_5M": {"total_trades": 10, "winrate": 55.0, "expectancy_R": 0.5, "profit_factor": 1.8}}
    monkeypatch.setattr("modules.spcx_v2.session_tracker.compute_stats_by_setup", mock_stats)
    monkeypatch.setattr("modules.spcx_v2.session_tracker._read_jsonl", lambda *a, **kw: [])

    c = make_candidate(setup_type="IPO_ORB_5M")
    cid = log_candidate(c)
    log_result(cid, {"r_multiple": 1.5, "mfe": 0.02, "mae": 0.01, "hit_tp1": True})

    from modules.spcx_v2.session_tracker import bump_session, get_session_count
    for i in range(6):
        bump_session()

    from modules.spcx_v2.session_tracker import graduation_report, GRADUATION_FILE
    report = graduation_report()
    assert "setups" in report
    assert report["summary"]["total_setups_tested"] >= 0
    assert GRADUATION_FILE.exists()


def test_thresholds_defined():
    from modules.spcx_v2.session_tracker import VALIDATION_THRESHOLDS
    assert "IPO_ORB_5M" in VALIDATION_THRESHOLDS
    assert "IPO_ORB_15M" in VALIDATION_THRESHOLDS
    assert "VWAP_HOLD_LONG" in VALIDATION_THRESHOLDS
    assert "FVG_BULLISH_RECLAIM" in VALIDATION_THRESHOLDS


def test_graduation_report_empty(monkeypatch, tmp_path):
    monkeypatch.setattr("modules.spcx_v2.session_tracker.compute_stats_by_setup", lambda *a, **kw: {})
    monkeypatch.setattr("modules.spcx_v2.session_tracker._read_jsonl", lambda *a, **kw: [])

    from modules.spcx_v2.session_tracker import graduation_report
    report = graduation_report()
    assert report["summary"]["total_setups_tested"] == 0
    assert report["summary"]["passed"] == 0
