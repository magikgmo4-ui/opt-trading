import json
import pytest
from pathlib import Path

from modules.desk_pro.service.vision_context_reader import read_vision_context_coinglass

FIXTURE_DIR = Path("tests/fixtures/vision/coinglass")


def _write_tmp(tmp_path: Path, payload: dict) -> Path:
    p = tmp_path / "latest.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


def _valid_payload(**kwargs) -> dict:
    base = {
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
            {
                "detected_metric_type": "liquidations_long",
                "extracted_value": 48500000.0,
                "unit": "USD",
                "confidence": 0.82,
                "evidence_ref": "data/vision/coinglass/raw/screenshot.png",
                "notes": "",
            },
            {
                "detected_metric_type": "liquidations_short",
                "extracted_value": 21300000.0,
                "unit": "USD",
                "confidence": 0.78,
                "evidence_ref": "data/vision/coinglass/raw/screenshot.png",
                "notes": "",
            },
        ],
        "warnings": [],
        "refs": {
            "raw_screenshot": "data/vision/coinglass/raw/screenshot.png",
            "normalized": "data/vision/coinglass/normalized/v.json",
            "latest": "data/vision/coinglass/latest.json",
            "events": "data/vision/coinglass/events.jsonl",
        },
    }
    base.update(kwargs)
    return base


# TC-DESKPRO-01: lecture latest.json → métriques injectées dans snapshot
class TestReadVisionContextCoinglass:

    def test_valid_file_returns_metrics(self, tmp_path):
        p = _write_tmp(tmp_path, _valid_payload())
        metrics = read_vision_context_coinglass(path=p)
        assert len(metrics) == 2
        types = {m.metric for m in metrics}
        assert "liquidations_long" in types
        assert "liquidations_short" in types

    def test_metrics_have_correct_source_and_asset(self, tmp_path):
        p = _write_tmp(tmp_path, _valid_payload())
        metrics = read_vision_context_coinglass(path=p)
        for m in metrics:
            assert m.source == "coinglass_headless_bot"
            assert m.asset == "BTCUSDT"
            assert m.window == "vision"

    # TC-DESKPRO-02: fichier absent → liste vide, pas d'exception
    def test_absent_file_returns_empty(self, tmp_path):
        result = read_vision_context_coinglass(path=tmp_path / "missing.json")
        assert result == []

    # TC-DESKPRO-03: input_class incorrect → ignoré, pas d'injection
    def test_wrong_input_class_returns_empty(self, tmp_path):
        payload = _valid_payload(input_class="market_metrics.v1")
        p = _write_tmp(tmp_path, payload)
        result = read_vision_context_coinglass(path=p)
        assert result == []

    def test_missing_input_class_returns_empty(self, tmp_path):
        payload = _valid_payload()
        del payload["input_class"]
        p = _write_tmp(tmp_path, payload)
        result = read_vision_context_coinglass(path=p)
        assert result == []

    # TC-DESKPRO-04: confidence < seuil → Metric.quality bas (≤ 0.5)
    def test_low_confidence_yields_low_quality(self, tmp_path):
        payload = _valid_payload(detections=[
            {
                "detected_metric_type": "liquidations_long",
                "extracted_value": 10_000_000.0,
                "unit": "USD",
                "confidence": 0.45,
                "evidence_ref": "data/vision/coinglass/raw/screenshot.png",
                "notes": "low confidence",
            }
        ], warnings=["low confidence"])
        p = _write_tmp(tmp_path, payload)
        metrics = read_vision_context_coinglass(path=p)
        assert len(metrics) == 1
        assert metrics[0].quality <= 0.5

    def test_high_confidence_yields_high_quality(self, tmp_path):
        payload = _valid_payload(detections=[
            {
                "detected_metric_type": "liquidations_long",
                "extracted_value": 48_500_000.0,
                "unit": "USD",
                "confidence": 0.90,
                "evidence_ref": "data/vision/coinglass/raw/screenshot.png",
                "notes": "",
            }
        ])
        p = _write_tmp(tmp_path, payload)
        metrics = read_vision_context_coinglass(path=p)
        assert len(metrics) == 1
        assert metrics[0].quality >= 0.85

    def test_partial_confidence_yields_mid_quality(self, tmp_path):
        payload = _valid_payload(detections=[
            {
                "detected_metric_type": "liquidations_short",
                "extracted_value": 5_000_000.0,
                "unit": "USD",
                "confidence": 0.72,
                "evidence_ref": "data/vision/coinglass/raw/screenshot.png",
                "notes": "",
            }
        ])
        p = _write_tmp(tmp_path, payload)
        metrics = read_vision_context_coinglass(path=p)
        assert len(metrics) == 1
        assert 0.5 < metrics[0].quality < 0.9

    # TC-DESKPRO-05: extracted_value = null → pas d'injection, pas d'exception
    def test_null_extracted_value_skipped(self, tmp_path):
        payload = _valid_payload(detections=[
            {
                "detected_metric_type": "liquidations_long",
                "extracted_value": None,
                "unit": "USD",
                "confidence": 0.75,
                "evidence_ref": "data/vision/coinglass/raw/screenshot.png",
                "notes": "not visible",
            }
        ])
        p = _write_tmp(tmp_path, payload)
        result = read_vision_context_coinglass(path=p)
        assert result == []

    # TC-DESKPRO-05: aucun write dans market_metrics/latest.json
    def test_no_write_to_market_metrics(self, tmp_path):
        mm_path = tmp_path / "market_metrics_latest.json"
        mm_path.write_text('{"input_class": "market_metrics.v1"}', encoding="utf-8")
        original_content = mm_path.read_text()

        p = _write_tmp(tmp_path, _valid_payload())
        read_vision_context_coinglass(path=p)

        assert mm_path.read_text() == original_content

    def test_malformed_json_returns_empty(self, tmp_path):
        p = tmp_path / "latest.json"
        p.write_text("not json {{{{", encoding="utf-8")
        result = read_vision_context_coinglass(path=p)
        assert result == []

    def test_reads_fixture_valid_json(self):
        fixture = FIXTURE_DIR / "vision_coinglass_v1_valid.json"
        if not fixture.exists():
            pytest.skip("fixture not present")
        metrics = read_vision_context_coinglass(path=fixture)
        assert len(metrics) >= 2

    def test_reads_fixture_null_vals_skips_nulls(self):
        fixture = FIXTURE_DIR / "vision_coinglass_v1_null_vals.json"
        if not fixture.exists():
            pytest.skip("fixture not present")
        metrics = read_vision_context_coinglass(path=fixture)
        assert metrics == []

    def test_reads_fixture_low_conf_quality(self):
        fixture = FIXTURE_DIR / "vision_coinglass_v1_low_conf.json"
        if not fixture.exists():
            pytest.skip("fixture not present")
        metrics = read_vision_context_coinglass(path=fixture)
        # low_conf fixture has extracted_value=null → skip
        assert metrics == []
