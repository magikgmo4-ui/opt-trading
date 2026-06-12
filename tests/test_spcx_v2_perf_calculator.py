"""Tests for SPCX V2 perf calculator — MFE, MAE, R-multiple, stats."""

import pytest
from modules.spcx_v2.perf_calculator import (
    calculate_mfe,
    calculate_mae,
    calculate_r_multiple,
    check_tp1_hit,
    check_tp2_hit,
    check_sl_hit,
    compute_stats,
    compute_stats_by_setup,
    compute_stats_by_grade,
)


# ── MFE ──────────────────────────────────────────────────────────────
def test_mfe_long_profit():
    assert calculate_mfe(100, [101, 105, 103, 108], "long") == pytest.approx(0.08)


def test_mfe_long_no_change():
    assert calculate_mfe(100, [100, 100, 100], "long") == 0.0


def test_mfe_long_loss():
    assert calculate_mfe(100, [99, 98, 97], "long") == pytest.approx(-0.01)


def test_mfe_empty_series():
    assert calculate_mfe(100, [], "long") == 0.0


def test_mfe_short_profit():
    assert calculate_mfe(100, [99, 95, 97], "short") == pytest.approx(0.05)


# ── MAE ──────────────────────────────────────────────────────────────
def test_mae_long_loss():
    assert calculate_mae(100, [99, 95, 97, 102], "long") == pytest.approx(0.05)


def test_mae_long_profit():
    assert calculate_mae(100, [101, 102, 103], "long") == pytest.approx(-0.01)


def test_mae_empty_series():
    assert calculate_mae(100, [], "long") == 0.0


# ── R-multiple ───────────────────────────────────────────────────────
def test_r_multiple_long_win():
    assert calculate_r_multiple(100, 98, 104, "long") == 2.0


def test_r_multiple_long_loss():
    assert calculate_r_multiple(100, 98, 97, "long") == -1.5


def test_r_multiple_short_win():
    assert calculate_r_multiple(100, 102, 96, "short") == 2.0


def test_r_multiple_sl_equals_entry():
    assert calculate_r_multiple(100, 100, 105, "long") == 0.0


# ── TP/SL hits ───────────────────────────────────────────────────────
def test_tp1_hit_long():
    assert check_tp1_hit([100, 101, 102, 103], 102, "long") is True


def test_tp1_not_hit_long():
    assert check_tp1_hit([100, 101], 102, "long") is False


def test_tp2_hit_long():
    assert check_tp2_hit([100, 104, 102, 106], 105, "long") is True


def test_sl_hit_long():
    assert check_sl_hit([100, 99, 97, 101], 98, "long") is True


def test_sl_not_hit_long():
    assert check_sl_hit([100, 101, 102], 98, "long") is False


def test_tp1_short():
    assert check_tp1_hit([100, 99, 97], 98, "short") is True


# ── Stats ────────────────────────────────────────────────────────────
def test_compute_stats_empty():
    stats = compute_stats([])
    assert stats["total_trades"] == 0
    assert stats["winrate"] == 0


def test_compute_stats_basic():
    candidates = [
        {"r_multiple": 2.0, "mfe": 0.03, "mae": 0.01, "hit_tp1": True, "hit_tp2": False, "hit_sl": False},
        {"r_multiple": -1.0, "mfe": 0.01, "mae": 0.02, "hit_tp1": False, "hit_tp2": False, "hit_sl": True},
        {"r_multiple": 1.5, "mfe": 0.025, "mae": 0.005, "hit_tp1": True, "hit_tp2": False, "hit_sl": False},
    ]
    stats = compute_stats(candidates)
    assert stats["total_trades"] == 3
    assert stats["win_count"] == 2
    assert stats["loss_count"] == 1
    assert stats["winrate"] == pytest.approx(66.67, 0.1)
    assert stats["expectancy_R"] == pytest.approx(0.833, 0.01)
    assert stats["profit_factor"] == pytest.approx(3.5, 0.01)
    assert stats["tp1_hit_rate"] == pytest.approx(66.67, 0.1)


def test_compute_stats_drawdown():
    candidates = [
        {"r_multiple": -1.0},
        {"r_multiple": -0.5},
        {"r_multiple": 2.0},
    ]
    stats = compute_stats(candidates)
    assert stats["max_drawdown_R"] == 1.5


def test_compute_stats_by_setup():
    candidates = [
        {"setup_type": "ORB_5M", "r_multiple": 2.0},
        {"setup_type": "ORB_5M", "r_multiple": -1.0},
        {"setup_type": "VWAP", "r_multiple": 1.0},
    ]
    by_setup = compute_stats_by_setup(candidates)
    assert "ORB_5M" in by_setup
    assert "VWAP" in by_setup
    assert by_setup["ORB_5M"]["total_trades"] == 2


def test_compute_stats_by_grade():
    candidates = [
        {"grade": "A+", "r_multiple": 2.0},
        {"grade": "A+", "r_multiple": 1.5},
        {"grade": "A", "r_multiple": -1.0},
    ]
    by_grade = compute_stats_by_grade(candidates)
    assert "A+" in by_grade
    assert by_grade["A+"]["total_trades"] == 2
    assert by_grade["A+"]["expectancy_R"] == 1.75
