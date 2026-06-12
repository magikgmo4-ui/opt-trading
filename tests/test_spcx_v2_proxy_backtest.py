"""Tests for SPCX V2 proxy IPO backtest engine."""

import csv
import tempfile
from pathlib import Path

import pytest
from modules.spcx_v2.proxy_backtest import (
    load_csv,
    candle_to_snapshot,
    replay_csv,
    run_proxy_backtest,
    PROXY_SYMBOLS,
)


def _make_csv(rows: list[dict]) -> Path:
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
    writer = csv.DictWriter(tmp, fieldnames=["ts", "open", "high", "low", "close", "volume", "vwap"])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    tmp.close()
    return Path(tmp.name)


@pytest.fixture(autouse=True)
def temp_output_dir(monkeypatch, tmp_path):
    monkeypatch.setattr("modules.spcx_v2.paper_logger.OUTPUT_DIR", tmp_path)
    monkeypatch.setattr("modules.spcx_v2.proxy_backtest.PROJECT_ROOT", tmp_path)
    return tmp_path


# ── CSV loading ───────────────────────────────────────────────────────
def test_load_csv():
    csv_path = _make_csv([
        {"ts": "2024-01-01", "open": "40", "high": "42", "low": "39", "close": "41", "volume": "1000000", "vwap": "40.5"},
    ])
    rows = load_csv(str(csv_path))
    assert len(rows) == 1
    csv_path.unlink()


def test_load_csv_missing():
    rows = load_csv("/nonexistent/file.csv")
    assert rows == []


# ── candle_to_snapshot ────────────────────────────────────────────────
def test_candle_to_snapshot_basic():
    candle = {"ts": "2024-01-01T14:30", "open": "40", "high": "42", "low": "39", "close": "41", "volume": "500000", "vwap": "40.5"}
    snap = candle_to_snapshot(candle, "RKLB", 0, 0)
    assert snap.symbol == "RKLB"
    assert snap.price == 41.0
    assert snap.price_status == "live"
    assert snap.volume == 500000
    assert snap.vwap == 40.5
    assert snap.bars_count == 1
    assert snap.price_trust == 90


def test_candle_to_snapshot_vwap_fallback():
    candle = {"ts": "t", "open": "40", "high": "42", "low": "39", "close": "41", "volume": "1000"}
    snap = candle_to_snapshot(candle, "ASTS", 0)
    expected_vwap = (42 + 39 + 41) / 3
    assert abs(snap.vwap - expected_vwap) < 0.01


def test_candle_to_snapshot_smc_structures():
    candle = {"ts": "t", "open": "40", "high": "42", "low": "39", "close": "41", "volume": "500000"}
    snap = candle_to_snapshot(candle, "RKLB", 5, prev_volume=100000)
    assert any(s["type"] == "BOS" for s in snap.smc_structures)
    assert any(s["type"] == "FVG_BULLISH" for s in snap.smc_structures)


def test_candle_to_snapshot_first_candle_no_bos():
    candle = {"ts": "t", "open": "40", "high": "42", "low": "39", "close": "41", "volume": "1000"}
    snap = candle_to_snapshot(candle, "RKLB", 0)
    assert not any(s["type"] == "BOS" for s in snap.smc_structures)


# ── replay ────────────────────────────────────────────────────────────
def test_replay_csv_basic(tmp_path):
    csv_path = _make_csv([
        {"ts": "2024-01-01T09:30", "open": "40", "high": "42", "low": "39", "close": "41.5", "volume": "500000", "vwap": "40.5"},
        {"ts": "2024-01-01T09:35", "open": "41.5", "high": "43", "low": "41", "close": "42.5", "volume": "600000", "vwap": "42.0"},
        {"ts": "2024-01-01T09:40", "open": "42.5", "high": "44", "low": "42", "close": "43.0", "volume": "700000", "vwap": "43.0"},
        {"ts": "2024-01-01T09:45", "open": "43.0", "high": "43.5", "low": "42", "close": "42.8", "volume": "400000", "vwap": "42.8"},
    ])
    results = replay_csv(str(csv_path), "RKLB")
    csv_path.unlink()
    assert isinstance(results, list)


def test_replay_csv_empty():
    csv_path = _make_csv([])
    results = replay_csv(str(csv_path), "RKLB")
    csv_path.unlink()
    assert results == []


def test_run_proxy_backtest(tmp_path):
    csv_path = _make_csv([
        {"ts": "2024-01-01T09:30", "open": "40", "high": "42", "low": "39", "close": "41", "volume": "500000", "vwap": "40.5"},
        {"ts": "2024-01-01T09:35", "open": "41", "high": "43", "low": "40.5", "close": "42.5", "volume": "600000", "vwap": "42.0"},
        {"ts": "2024-01-01T09:40", "open": "42.5", "high": "44", "low": "42", "close": "43", "volume": "700000", "vwap": "43.0"},
        {"ts": "2024-01-01T09:45", "open": "43", "high": "45", "low": "42.5", "close": "44", "volume": "800000", "vwap": "44.0"},
        {"ts": "2024-01-01T09:50", "open": "44", "high": "46", "low": "43.5", "close": "45", "volume": "900000", "vwap": "45.0"},
    ])
    result = run_proxy_backtest("RKLB", str(csv_path))
    csv_path.unlink()
    assert result["symbol"] == "RKLB"
    assert isinstance(result["results"], list)
    assert "summary" in result


def test_proxy_symbols_list():
    assert len(PROXY_SYMBOLS) == 13
    assert "RKLB" in PROXY_SYMBOLS
    assert "PLTR" in PROXY_SYMBOLS
