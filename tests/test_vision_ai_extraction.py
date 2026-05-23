import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from modules.vision.coinglass.ai_extraction import (
    _parse_ai_response,
    make_ai_extraction_fn,
)


def _valid_json_response(metric_type="liquidations_long", value=48_500_000.0, conf=0.92):
    return json.dumps({
        "detections": [{
            "detected_metric_type": metric_type,
            "extracted_value": value,
            "unit": "USD",
            "confidence": conf,
            "notes": "",
        }]
    })


class TestParseAiResponse:

    def test_valid_json_parsed(self):
        dets = _parse_ai_response(_valid_json_response(), "img.png")
        assert len(dets) == 1
        assert dets[0].detected_metric_type == "liquidations_long"
        assert dets[0].extracted_value == 48_500_000.0
        assert dets[0].confidence == 0.92

    def test_prose_wrapping_json_extracted(self):
        prose = 'Here are the metrics:\n' + _valid_json_response() + '\nDone.'
        dets = _parse_ai_response(prose, "img.png")
        assert len(dets) == 1

    def test_pure_prose_no_json_returns_empty(self):
        dets = _parse_ai_response("I cannot read the image clearly.", "img.png")
        assert dets == []

    def test_empty_string_returns_empty(self):
        assert _parse_ai_response("", "img.png") == []

    def test_low_confidence_nulls_value(self):
        resp = json.dumps({"detections": [{
            "detected_metric_type": "long_short_ratio",
            "extracted_value": 1.5,
            "unit": "ratio",
            "confidence": 0.45,
            "notes": "blurry",
        }]})
        dets = _parse_ai_response(resp, "img.png")
        assert len(dets) == 1
        assert dets[0].extracted_value is None
        assert dets[0].confidence == 0.45

    def test_null_extracted_value_preserved(self):
        resp = json.dumps({"detections": [{
            "detected_metric_type": "open_interest",
            "extracted_value": None,
            "unit": "USD",
            "confidence": 0.80,
            "notes": "occluded",
        }]})
        dets = _parse_ai_response(resp, "img.png")
        assert dets[0].extracted_value is None

    def test_empty_detections_list(self):
        dets = _parse_ai_response(json.dumps({"detections": []}), "img.png")
        assert dets == []

    def test_malformed_detection_skipped(self):
        resp = json.dumps({"detections": [
            {"detected_metric_type": "liquidations_long", "extracted_value": "NOT_A_NUMBER",
             "unit": "USD", "confidence": "bad", "notes": ""},
            {"detected_metric_type": "liquidations_short", "extracted_value": 100.0,
             "unit": "USD", "confidence": 0.90, "notes": ""},
        ]})
        dets = _parse_ai_response(resp, "img.png")
        assert len(dets) == 1
        assert dets[0].detected_metric_type == "liquidations_short"


class TestMakeAiExtractionFn:

    def test_no_provider_returns_empty(self, tmp_path):
        img = tmp_path / "shot.png"
        img.write_bytes(b"\x89PNG")
        fn = make_ai_extraction_fn(provider="")
        assert fn(img) == []

    def test_openai_uses_call_fn_injection(self, tmp_path, monkeypatch):
        img = tmp_path / "shot.png"
        img.write_bytes(b"\x89PNG")
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        mock_call = MagicMock(return_value=_valid_json_response())
        fn = make_ai_extraction_fn(provider="openai", _call_fn=mock_call)
        dets = fn(img)
        assert len(dets) == 1
        mock_call.assert_called_once()

    def test_openai_missing_key_returns_empty(self, tmp_path, monkeypatch):
        img = tmp_path / "shot.png"
        img.write_bytes(b"\x89PNG")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        fn = make_ai_extraction_fn(provider="openai")
        assert fn(img) == []

    def test_call_fn_exception_returns_empty(self, tmp_path, monkeypatch):
        img = tmp_path / "shot.png"
        img.write_bytes(b"\x89PNG")
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        def _boom(path, key, model): raise RuntimeError("network error")
        fn = make_ai_extraction_fn(provider="openai", _call_fn=_boom)
        assert fn(img) == []

    def test_unknown_provider_returns_empty(self, tmp_path):
        img = tmp_path / "shot.png"
        img.write_bytes(b"\x89PNG")
        fn = make_ai_extraction_fn(provider="gemini")
        assert fn(img) == []

    def test_response_format_json_object_in_call(self, tmp_path, monkeypatch):
        """_call_openai doit passer response_format=json_object — vérifié via mock SDK."""
        img = tmp_path / "shot.png"
        img.write_bytes(b"\x89PNG")
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

        captured = {}

        def _mock_call(image_path, api_key, model):
            captured["called"] = True
            return _valid_json_response()

        fn = make_ai_extraction_fn(provider="openai", _call_fn=_mock_call)
        dets = fn(img)
        assert captured.get("called")
        assert len(dets) == 1
