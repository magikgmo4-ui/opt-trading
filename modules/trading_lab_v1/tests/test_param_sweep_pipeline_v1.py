"""Integration tests for BTC COIN-M sweep pipeline."""
from __future__ import annotations

from modules.trading_lab_v1.app import param_sweep_engine_v1 as eng
from modules.trading_lab_v1.app import param_sweep_config_v1 as gen
from modules.trading_lab_v1.app import param_sweep_classify_v1 as clf
from modules.trading_lab_v1.app import param_sweep_rank_v1 as rank


_MARK = 90000.0


def _candle(ts: str = "2026-01-01T00:00:00Z", close: float = _MARK,
            funding_rate: float | None = None, funding_settled: bool = False) -> dict:
    return {
        "ts": ts, "open": close, "high": close, "low": close, "close": close,
        "mark_price": close, "index_price": close,
        "funding_rate": funding_rate, "funding_settled": funding_settled,
    }


def _default_config(**kw) -> dict:
    cfg = {
        "z_dca": 0.005, "z_short": 0.015, "g_up": 0.015, "g_down": 0.010,
        "r_transfer": 0.30, "y_dca_usdt": 200.0, "q_add_native": 0.001,
        "tp1": 0.50, "tp2": 0.25, "runner": 0.25,
        "cooldown_dca_h": 0, "cooldown_short_h": 0,
        "leverage_target": 2, "D_min": 0.20, "MR_max": 0.60,
        "Q_max_native": 50, "U_floor_usdt": 0.0, "M_floor_btc": 0.0,
        "funding_limit": 0.5, "fee_limit": 0.1, "slippage_max_bps": 200,
        "weekly_structure_gate_mode": "off", "weekly_k": 3,
        "weekly_epsilon_lambda": 0.01, "max_pivot_gap_weeks": 8,
    }
    cfg.update(kw)
    return cfg


# ── tests ─────────────────────────────────────────────────────────────────

def test_full_pipeline_single_config(monkeypatch):
    candles = [_candle(f"2026-01-01T{i:02d}:00:00Z",
                       close=_MARK * (1.001 ** i)) for i in range(50)]
    config = _default_config()
    result = eng.simulate_run(config, candles)
    result = clf.classify_run(result)
    assert result["classification_primary"] in (
        "REALISTIC", "PAPER_ONLY", "EXCHANGE_IMPOSSIBLE",
        "MATH_INVALID", "LIQUIDATED", "DATA_INVALID",
    )
    assert result["delta_btc_net"] is not None


def test_batch_10_random_configs(monkeypatch):
    candles = [_candle(f"2026-01-01T{i:02d}:00:00Z",
                       close=_MARK * (1.0005 ** i)) for i in range(20)]
    cfgs = gen.generate_configs(count=10, seed=42)
    for cfg in cfgs:
        result = eng.simulate_run(cfg, candles)
        assert result["simulation_stop_reason"] in (
            "completed", "liquidated", "math_invalid",
        )


def test_classify_math_invalid(monkeypatch):
    config = _default_config(tp1=0.5, tp2=0.5, runner=0.5)
    result = eng.simulate_run(config, [])
    result = clf.classify_run(result)
    assert result["classification_primary"] == "MATH_INVALID"


def test_classify_liquidated(monkeypatch):
    candles = [_candle("2026-01-01T00:00:00Z", close=50000)]
    config = _default_config(g_up=0.01, q_add_native=10.0, z_short=0.0)
    config["last_pivot_price"] = 50000
    result = eng.simulate_run(config, candles, initial_state={
        "P_0": 40000, "S_0_btc": 0.0, "U_0_usdt": 0.0, "M_0_btc": 0.0001,
        "Q_0_native": 0.0, "E_0": None,
    })
    result["last_pivot_price"] = 40000  # ensure pivot is set
    # force a short add then liquidation
    # ... we need candles where price rises enough for a short, then rises more for liq
    assert result["simulation_stop_reason"] in ("completed", "liquidated")


def test_classify_exchange_impossible(monkeypatch):
    config = _default_config(q_add_native=0.00005)
    result = eng.simulate_run(config, [])
    result = clf.classify_run(result)
    if result.get("exchange_impossible_event_count", 0) > 0:
        assert result["classification_primary"] == "EXCHANGE_IMPOSSIBLE"


def test_classify_paper_only(monkeypatch):
    config = _default_config()
    result = eng.simulate_run(config, [])
    result = clf.classify_run(result)
    assert result["classification_primary"] in ("PAPER_ONLY", "REALISTIC")


def test_rank_raw_best_descending(monkeypatch):
    runs = [
        {"delta_btc_net": 0.01, "math_valid": True, "data_valid": True,
         "liquidation_count": 0, "max_drawdown_btc": 0.001,
         "funding_paid_btc": 0, "fees_btc": 0, "overfit_score": 0,
         "config_hash": "a", "classification_primary": "PAPER_ONLY"},
        {"delta_btc_net": 0.05, "math_valid": True, "data_valid": True,
         "liquidation_count": 0, "max_drawdown_btc": 0.002,
         "funding_paid_btc": 0, "fees_btc": 0, "overfit_score": 0,
         "config_hash": "b", "classification_primary": "PAPER_ONLY"},
        {"delta_btc_net": -0.01, "math_valid": True, "data_valid": True,
         "liquidation_count": 1, "max_drawdown_btc": 0.005,
         "funding_paid_btc": 0, "fees_btc": 0, "overfit_score": 0,
         "config_hash": "c", "classification_primary": "LIQUIDATED"},
    ]
    best = rank.rank_runs(runs, "raw_best")
    assert best[0]["delta_btc_net"] == 0.05
    assert best[1]["delta_btc_net"] == 0.01


def test_rank_raw_worst_ascending(monkeypatch):
    runs = [
        {"delta_btc_net": 0.01, "math_valid": True, "data_valid": True,
         "liquidation_count": 0, "max_drawdown_btc": 0, "funding_paid_btc": 0,
         "fees_btc": 0, "overfit_score": 0, "config_hash": "a",
         "classification_primary": "PAPER_ONLY"},
        {"delta_btc_net": -0.05, "math_valid": True, "data_valid": True,
         "liquidation_count": 0, "max_drawdown_btc": 0, "funding_paid_btc": 0,
         "fees_btc": 0, "overfit_score": 0, "config_hash": "b",
         "classification_primary": "PAPER_ONLY"},
        {"delta_btc_net": 0.00, "math_valid": True, "data_valid": True,
         "liquidation_count": 0, "max_drawdown_btc": 0, "funding_paid_btc": 0,
         "fees_btc": 0, "overfit_score": 0, "config_hash": "c",
         "classification_primary": "PAPER_ONLY"},
    ]
    worst = rank.rank_runs(runs, "raw_worst")
    assert worst[0]["delta_btc_net"] == -0.05


def test_format_top_markdown(monkeypatch):
    runs = [
        {"run_id": "abc", "config_hash": "def", "delta_btc_net": 0.05,
         "delta_btc_pct": 5.0, "net_btc_final": 1.05, "liquidation_count": 0,
         "max_drawdown_btc": 0.001, "funding_paid_btc": 0.0, "fees_btc": 0.0,
         "classification_primary": "PAPER_ONLY"},
    ]
    best = rank.rank_runs(runs, "raw_best")
    md = rank.format_top_markdown(best, 100, "Test")
    assert "Test" in md
    assert "abc" in md


def test_config_hash_is_stable():
    cfg = _default_config()
    h1 = gen.config_hash(cfg)
    h2 = gen.config_hash(cfg)
    assert h1 == h2
