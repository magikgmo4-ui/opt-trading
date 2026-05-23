import json
import pytest
from pathlib import Path

from modules.desk_pro.service.vision_panel import read_vision_panel_data

FIXTURE_VALID = Path("tests/fixtures/vision/coinglass/vision_coinglass_v1_valid.json")


def _write(tmp_path: Path, payload: dict) -> Path:
    p = tmp_path / "latest.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


def _valid_payload() -> dict:
    return {
        "contract_version": "v1",
        "input_class": "vision_context.coinglass.v1",
        "source_id": "coinglass_headless_bot",
        "screenshot_ts": "2026-05-23T06:00:00Z",
        "symbol": "BTCUSDT",
        "timeframe": "1H",
        "board": "liquidations",
        "page": "liquidation_heatmap",
        "freshness_state": "fresh",
        "detections": [
            {"detected_metric_type": "liquidations_long", "extracted_value": 48_500_000.0,
             "unit": "USD", "confidence": 0.82, "evidence_ref": "r.png", "notes": ""},
        ],
        "warnings": [],
        "refs": {"raw_screenshot": "r.png", "normalized": "n.json",
                 "latest": "l.json", "events": "e.jsonl"},
    }


class TestReadVisionPanelData:

    # ok=True avec données complètes
    def test_valid_file_returns_ok(self, tmp_path):
        p = _write(tmp_path, _valid_payload())
        result = read_vision_panel_data(path=p)
        assert result["ok"] is True
        assert result["vision"] is not None
        assert result["vision"]["symbol"] == "BTCUSDT"

    # age_hours calculé (screenshot old → grand nombre)
    def test_age_hours_computed(self, tmp_path):
        p = _write(tmp_path, _valid_payload())
        result = read_vision_panel_data(path=p)
        assert result["age_hours"] is not None
        assert result["age_hours"] > 0

    # Fichier absent → ok=False, reason=no_data
    def test_absent_file_returns_not_ok(self, tmp_path):
        result = read_vision_panel_data(path=tmp_path / "missing.json")
        assert result["ok"] is False
        assert result["reason"] == "no_data"
        assert result["vision"] is None

    # input_class incorrect → ok=False, reason=wrong_input_class
    def test_wrong_input_class(self, tmp_path):
        payload = _valid_payload()
        payload["input_class"] = "market_metrics.v1"
        p = _write(tmp_path, payload)
        result = read_vision_panel_data(path=p)
        assert result["ok"] is False
        assert result["reason"] == "wrong_input_class"

    # JSON malformé → ok=False, reason=read_error
    def test_malformed_json(self, tmp_path):
        p = tmp_path / "latest.json"
        p.write_text("NOT JSON {{{", encoding="utf-8")
        result = read_vision_panel_data(path=p)
        assert result["ok"] is False
        assert result["reason"] == "read_error"

    # Données complètes transmises intactes
    def test_vision_data_passed_through(self, tmp_path):
        p = _write(tmp_path, _valid_payload())
        result = read_vision_panel_data(path=p)
        v = result["vision"]
        assert v["freshness_state"] == "fresh"
        assert len(v["detections"]) == 1
        assert v["detections"][0]["detected_metric_type"] == "liquidations_long"

    # Fixture valide du repo → ok=True
    def test_valid_repo_fixture(self):
        if not FIXTURE_VALID.exists():
            pytest.skip("fixture not present")
        result = read_vision_panel_data(path=FIXTURE_VALID)
        assert result["ok"] is True
        assert result["vision"]["symbol"] == "BTCUSDT"

    # screenshot_ts invalide → age_hours=None, pas d'exception
    def test_bad_timestamp_age_none(self, tmp_path):
        payload = _valid_payload()
        payload["screenshot_ts"] = "not-a-date"
        p = _write(tmp_path, payload)
        result = read_vision_panel_data(path=p)
        assert result["ok"] is True
        assert result["age_hours"] is None
