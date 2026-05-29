import json
from pathlib import Path

from modules.telegram_screener.service.signal_context_reader import read_signal_context


_FIXTURE = {
    "schema": "market_metrics.v1",
    "contract_version": "v1",
    "input_class": "market_metrics.v1",
    "module_id": "derivatives_collector",
    "provider_id": "binance_derivatives",
    "symbol": "BTCUSDT",
    "metrics_ts": "2026-05-28T00:00:00Z",
    "freshness_state": "fresh",
    "provider_coverage": {
        "status": "full",
        "collectable_metrics": ["open_interest", "funding_rate"],
        "missing_metrics": [],
    },
    "metrics": {"open_interest": 1.0, "funding_rate": 0.1},
    "refs": {"primary_output": "a", "meta_output": "b", "latest": "c", "status": "d"},
    "produced_at": "2026-05-28T00:00:00+00:00",
    "warnings": [],
}


def test_missing_file_returns_none(tmp_path: Path):
    assert read_signal_context(tmp_path / "missing.json") is None


def test_invalid_json_returns_none(tmp_path: Path):
    path = tmp_path / "bad.json"
    path.write_text("{bad", encoding="utf-8")
    assert read_signal_context(path) is None


def test_wrong_input_class_returns_none(tmp_path: Path):
    path = tmp_path / "wrong.json"
    payload = dict(_FIXTURE)
    payload["input_class"] = "other.v1"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert read_signal_context(path) is None


def test_valid_payload_returns_context(tmp_path: Path):
    path = tmp_path / "latest.json"
    path.write_text(json.dumps(_FIXTURE), encoding="utf-8")
    data = read_signal_context(path)
    assert data is not None
    assert data["symbol"] == "BTCUSDT"
    assert data["provider_id"] == "binance_derivatives"
    assert data["metrics"]["open_interest"] == 1.0
    assert data["collectable_metrics"] == ["open_interest", "funding_rate"]
