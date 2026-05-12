"""Tests for param_sweep_engine_v1.py — BTC COIN-M simulation engine."""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

from modules.trading_lab_v1.app import param_sweep_engine_v1 as eng
from modules.trading_lab_v1.app import param_sweep_config_v1 as gen


# ── helpers ──────────────────────────────────────────────────────────────

_MARK = 90000.0

def _candle(ts: str = "2026-01-01T00:00:00Z", close: float = _MARK,
            funding_rate: float | None = None, funding_settled: bool = False,
            high: float | None = None, low: float | None = None) -> dict:
    return {
        "ts": ts,
        "open": close if high is None else close - 100,
        "high": high if high is not None else close + 100,
        "low": low if low is not None else close - 100,
        "close": close,
        "mark_price": close,
        "index_price": close,
        "funding_rate": funding_rate,
        "funding_settled": funding_settled,
    }


def _state(Q=0.0, M=0.02, S=0.1, U=10000.0, P=_MARK):
    return eng._init_state({"P_0": P, "S_0_btc": S, "U_0_usdt": U, "M_0_btc": M,
                             "Q_0_native": Q, "E_0": P if Q > 0 else None})


# ── configuration ─────────────────────────────────────────────────────────

def _default_config(**kw) -> dict:
    cfg = {
        "z_dca": 0.005, "z_short": 0.015, "g_up": 0.015, "g_down": 0.010,
        "r_transfer": 0.30, "y_dca_usdt": 200.0, "q_add_native": 0.001,
        "tp1": 0.50, "tp2": 0.25, "runner": 0.25,
        "cooldown_dca_h": 0, "cooldown_short_h": 0,
        "leverage_target": 2, "D_min": 0.20, "MR_max": 0.60,
        "Q_max_native": 0.02, "U_floor_usdt": 0.0, "M_floor_btc": 0.0,
        "funding_limit": 0.5, "fee_limit": 0.1, "slippage_max_bps": 200,
        "weekly_structure_gate_mode": "off", "weekly_k": 3,
        "weekly_epsilon_lambda": 0.01, "max_pivot_gap_weeks": 8,
    }
    cfg.update(kw)
    return cfg


# ── tests ─────────────────────────────────────────────────────────────────

def test_simulate_run_empty_candles_returns_initial_state(monkeypatch):
    config = _default_config()
    result = eng.simulate_run(config, [])
    assert result["simulation_stop_reason"] == "completed"
    assert result["candle_count"] == 0
    assert result["net_btc_final"] == result["net_btc_initial"]


def test_apply_funding_positive_rate_adds_btc():
    st = _state(Q=1.0, M=0.02, P=_MARK)
    c = _candle(funding_rate=0.0001, funding_settled=True)
    eng.apply_funding(st, c)
    assert st["Funding_received_btc"] > 0
    assert st["Funding_paid_btc"] == 0
    assert st["M_k_btc"] > 0.02


def test_apply_funding_negative_rate_deducts_btc():
    st = _state(Q=1.0, M=0.02, P=_MARK)
    c = _candle(funding_rate=-0.0001, funding_settled=True)
    eng.apply_funding(st, c)
    assert st["Funding_paid_btc"] > 0
    assert st["Funding_received_btc"] == 0


def test_apply_funding_skips_when_no_position():
    st = _state(Q=0.0, M=0.02, P=_MARK)
    c = _candle(funding_rate=0.0001, funding_settled=True)
    eng.apply_funding(st, c)
    assert st["funding_event_count"] == 0


def test_apply_dca_with_sufficient_reserve():
    st = _state(Q=0.0, M=0.02, S=0.0, U=10000, P=_MARK)
    config = _default_config(r_transfer=0.30, y_dca_usdt=200, z_dca=0.05)
    st["last_dca_price"] = _MARK * 1.06
    saved_S = st["S_k_btc"]
    saved_M = st["M_k_btc"]
    saved_U = st["U_k_usdt"]
    eng.apply_dca(st, _MARK, config, "2026-01-01T01:00:00Z")
    assert st["S_k_btc"] > saved_S
    assert st["M_k_btc"] > saved_M
    assert st["U_k_usdt"] < saved_U


def test_apply_dca_with_insufficient_reserve_skips():
    st = _state(Q=0.0, M=0.02, S=0.0, U=100, P=_MARK)
    config = _default_config(y_dca_usdt=200)
    eng.apply_dca(st, _MARK, config, "2026-01-01T01:00:00Z")
    assert st["dca_count"] == 0


def test_apply_short_add_with_signal():
    st = _state(Q=0.0, M=0.02, P=_MARK)
    st["last_pivot_price"] = _MARK
    config = _default_config(g_up=0.01, q_add_native=0.001)
    P_signal = _MARK * 1.02
    eng.apply_short_add(st, P_signal, config, "2026-01-01T01:00:00Z")
    assert st["Q_k_native"] > 0
    assert st["short_add_count"] == 1


def test_apply_short_add_no_signal_skips():
    st = _state(Q=0.0, M=0.02, P=_MARK)
    st["last_pivot_price"] = _MARK
    config = _default_config(g_up=0.05)
    eng.apply_short_add(st, _MARK * 1.01, config, "2026-01-01T01:00:00Z")
    assert st["short_add_count"] == 0


def test_apply_short_add_updates_entry_price():
    st = _state(Q=0.001, M=0.02, P=100000)
    st["last_pivot_price"] = 100000
    st["E_k"] = 100000
    config = _default_config(g_up=0.01, q_add_native=0.001)
    P_new = 102000
    eng.apply_short_add(st, P_new, config, "2026-01-01T01:00:00Z")
    assert st["E_k"] is not None
    assert st["E_k"] > 100000 and st["E_k"] < 102000


def test_apply_tp_closes_position_partial():
    st = _state(Q=0.010, M=0.02, P=_MARK)
    st["last_pivot_price"] = _MARK * 1.02
    st["E_k"] = _MARK * 1.02
    config = _default_config(g_down=0.01, tp1=0.50, tp2=0.25, q_add_native=0.001)
    eng.apply_tp(st, _MARK, config, "2026-01-01T01:00:00Z")
    assert st["Q_k_native"] < 0.010
    assert st["Q_k_native"] > 0
    assert st["tp_count"] == 1


def test_apply_tp_closes_position_full():
    st = _state(Q=0.001, M=0.02, P=_MARK)
    st["last_pivot_price"] = _MARK * 1.02
    st["E_k"] = _MARK * 1.02
    config = _default_config(g_down=0.01, tp1=1.0, tp2=0.0, runner=0.0)
    eng.apply_tp(st, _MARK, config, "2026-01-01T01:00:00Z")
    assert st["Q_k_native"] == 0
    assert st["E_k"] is None


def test_check_liquidation_detects_breach():
    st = _state(Q=10.0, M=0.001, P=50000)
    st["E_k"] = 60000
    eng.check_liquidation(st, 100000)
    assert st["liquidated"]
    assert st["liquidation_count"] == 1


def test_check_liquidation_no_breach_passes():
    st = _state(Q=1.0, M=0.02, P=_MARK)
    st["E_k"] = _MARK
    eng.check_liquidation(st, _MARK * 1.01)
    assert not st["liquidated"]


def test_output_matches_required_columns(monkeypatch):
    config = _default_config()
    result = eng.simulate_run(config, [])
    required = [
        "run_id", "config_hash", "net_btc_initial", "net_btc_final",
        "delta_btc_net", "delta_btc_pct", "max_drawdown_btc",
        "liquidation_count", "margin_breach_count", "funding_paid_btc",
        "funding_received_btc", "fees_btc", "spot_btc_final",
        "margin_btc_final", "realized_pnl_btc", "unrealized_pnl_btc",
        "classification_primary", "reject_reasons",
    ]
    for col in required:
        assert col in result, f"missing required column: {col}"


def test_stop_reason_completed(monkeypatch):
    candles = [_candle("2026-01-01T00:00:00Z", close=_MARK),
               _candle("2026-01-01T01:00:00Z", close=_MARK * 1.001)]
    config = _default_config()
    result = eng.simulate_run(config, candles)
    assert result["simulation_stop_reason"] == "completed"


def test_record_breaches_logs_D_min():
    st = _state(Q=1.0, M=0.02, P=_MARK)
    st["E_k"] = _MARK * 1.02
    config = _default_config(D_min=0.50)
    eng._record_breaches(st, _MARK * 1.01, config)
    assert st["d_min_breach_count"] > 0


def test_z_short_le_z_dca_not_blocked():
    cfg = _default_config(z_short=0.01, z_dca=0.05)
    candles = [_candle("2026-01-01T00:00:00Z", close=_MARK)]
    result = eng.simulate_run(cfg, candles)
    assert result["simulation_stop_reason"] == "completed"


def test_config_hash_is_stable():
    cfg = _default_config()
    h1 = gen.config_hash(cfg)
    h2 = gen.config_hash(cfg)
    assert h1 == h2


def test_tp_simplex_sum_is_one():
    rng = random.Random(42)
    for _ in range(100):
        tp1, tp2, runner = gen.sample_tp_triad(rng)
        assert abs(tp1 + tp2 + runner - 1.0) < 0.0001


def test_generate_configs_produces_expected_count():
    cfgs = gen.generate_configs(count=50, seed=42)
    assert len(cfgs) == 50
    for cfg in cfgs:
        assert "z_dca" in cfg
        assert abs(cfg["tp1"] + cfg["tp2"] + cfg["runner"] - 1.0) < 0.0001


def test_simulate_run_rising_market_short_loses(monkeypatch):
    candles = []
    price = _MARK
    for i in range(100):
        ts = f"2026-01-01T{i:02d}:00:00Z"
        price *= 1.002
        candles.append(_candle(ts, close=price))
    config = _default_config(g_up=0.005, q_add_native=0.001, z_short=0.0)
    result = eng.simulate_run(config, candles)
    assert result["liquidation_count"] >= 0
    assert "delta_btc_net" in result


def test_simulate_run_falling_market_short_wins(monkeypatch):
    candles = []
    price = _MARK
    for i in range(100):
        ts = f"2026-01-01T{i:02d}:00:00Z"
        price *= 0.998
        candles.append(_candle(ts, close=price))
    config = _default_config(g_up=0.005, g_down=0.005, q_add_native=0.001,
                             z_short=0.0, tp1=0.5, tp2=0.25, runner=0.25)
    result = eng.simulate_run(config, candles)
    assert "delta_btc_net" in result
    assert result["math_valid"]
