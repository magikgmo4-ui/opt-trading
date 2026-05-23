import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from modules.vision.coinglass.ai_extraction import (
    _parse_ai_response,
    make_ai_extraction_fn,
)

FIXTURE_PNG = Path("tests/fixtures/vision/coinglass/screenshot_mock_liquidations.png")

_VALID_RESPONSE = json.dumps({
    "detections": [
        {
            "detected_metric_type": "liquidations_long",
            "extracted_value": 48_500_000.0,
            "unit": "USD",
            "confidence": 0.82,
            "notes": "",
        },
        {
            "detected_metric_type": "liquidations_short",
            "extracted_value": 21_300_000.0,
            "unit": "USD",
            "confidence": 0.78,
            "notes": "",
        },
    ]
})

_LOW_CONF_RESPONSE = json.dumps({
    "detections": [
        {
            "detected_metric_type": "liquidations_long",
            "extracted_value": 99_000_000.0,  # should be nulled
            "unit": "USD",
            "confidence": 0.45,
            "notes": "unreadable",
        }
    ]
})

_NULL_VALUE_RESPONSE = json.dumps({
    "detections": [
        {
            "detected_metric_type": "open_interest",
            "extracted_value": None,
            "unit": "USD",
            "confidence": 0.72,
            "notes": "value not visible",
        }
    ]
})


class TestParseAiResponse(unittest.TestCase):

    def test_valid_response_returns_detections(self):
        dets = _parse_ai_response(_VALID_RESPONSE, "ref.png")
        self.assertEqual(len(dets), 2)
        types = {d.detected_metric_type for d in dets}
        self.assertIn("liquidations_long", types)
        self.assertIn("liquidations_short", types)

    def test_values_match_response(self):
        dets = _parse_ai_response(_VALID_RESPONSE, "ref.png")
        long_det = next(d for d in dets if d.detected_metric_type == "liquidations_long")
        self.assertAlmostEqual(long_det.extracted_value, 48_500_000.0)
        self.assertAlmostEqual(long_det.confidence, 0.82)

    # confidence < 0.60 → extracted_value forcé à null
    def test_low_confidence_sets_null(self):
        dets = _parse_ai_response(_LOW_CONF_RESPONSE, "ref.png")
        self.assertEqual(len(dets), 1)
        self.assertIsNone(dets[0].extracted_value)
        self.assertAlmostEqual(dets[0].confidence, 0.45)

    # extracted_value null dans la réponse → null préservé
    def test_null_value_preserved(self):
        dets = _parse_ai_response(_NULL_VALUE_RESPONSE, "ref.png")
        self.assertEqual(len(dets), 1)
        self.assertIsNone(dets[0].extracted_value)

    # JSON malformé → liste vide
    def test_malformed_json_returns_empty(self):
        dets = _parse_ai_response("NOT JSON {{", "ref.png")
        self.assertEqual(dets, [])

    # JSON sans 'detections' key → liste vide
    def test_missing_detections_key_returns_empty(self):
        dets = _parse_ai_response(json.dumps({"result": "ok"}), "ref.png")
        self.assertEqual(dets, [])

    # evidence_ref propagé
    def test_evidence_ref_set(self):
        dets = _parse_ai_response(_VALID_RESPONSE, "data/vision/coinglass/raw/screenshot.png")
        for d in dets:
            self.assertEqual(d.evidence_ref, "data/vision/coinglass/raw/screenshot.png")


class TestMakeAiExtractionFn(unittest.TestCase):

    def setUp(self):
        os.environ.pop("VISION_AI_PROVIDER", None)
        os.environ.pop("OPENAI_API_KEY", None)

    def tearDown(self):
        os.environ.pop("VISION_AI_PROVIDER", None)
        os.environ.pop("OPENAI_API_KEY", None)

    # Provider non set → liste vide, pas d'exception
    def test_no_provider_returns_empty(self):
        fn = make_ai_extraction_fn()
        result = fn(FIXTURE_PNG)
        self.assertEqual(result, [])

    # Provider inconnu → liste vide
    def test_unknown_provider_returns_empty(self):
        fn = make_ai_extraction_fn(provider="tesseract")
        result = fn(FIXTURE_PNG)
        self.assertEqual(result, [])

    # Provider openai sans API key → liste vide
    def test_openai_without_api_key_returns_empty(self):
        fn = make_ai_extraction_fn(provider="openai")
        result = fn(FIXTURE_PNG)
        self.assertEqual(result, [])

    # Provider openai avec _call_fn mock → détections retournées
    def test_openai_with_mock_call_returns_detections(self):
        def _mock_call(path, api_key, model):
            return _VALID_RESPONSE

        os.environ["OPENAI_API_KEY"] = "sk-test"
        fn = make_ai_extraction_fn(provider="openai", _call_fn=_mock_call)
        dets = fn(FIXTURE_PNG)
        self.assertEqual(len(dets), 2)

    # _call_fn lève exception → liste vide, pas de propagation
    def test_call_fn_exception_returns_empty(self):
        def _boom(path, api_key, model):
            raise ConnectionError("timeout")

        os.environ["OPENAI_API_KEY"] = "sk-test"
        fn = make_ai_extraction_fn(provider="openai", _call_fn=_boom)
        result = fn(FIXTURE_PNG)
        self.assertEqual(result, [])

    # VISION_AI_PROVIDER depuis env
    def test_provider_read_from_env(self):
        os.environ["VISION_AI_PROVIDER"] = "openai"
        os.environ["OPENAI_API_KEY"] = "sk-test"

        def _mock_call(path, api_key, model):
            return _VALID_RESPONSE

        fn = make_ai_extraction_fn(_call_fn=_mock_call)
        dets = fn(FIXTURE_PNG)
        self.assertEqual(len(dets), 2)

    # low conf via mock → null dans sortie
    def test_low_confidence_detection_nulled_via_mock(self):
        def _mock_call(path, api_key, model):
            return _LOW_CONF_RESPONSE

        os.environ["OPENAI_API_KEY"] = "sk-test"
        fn = make_ai_extraction_fn(provider="openai", _call_fn=_mock_call)
        dets = fn(FIXTURE_PNG)
        self.assertEqual(len(dets), 1)
        self.assertIsNone(dets[0].extracted_value)


if __name__ == "__main__":
    unittest.main()
