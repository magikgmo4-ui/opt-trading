import json
import unittest

from modules.vision.coinglass.vision_context_v1 import (
    Detection,
    VisionContextCoinglassV1,
    VisionRefs,
)


def _make_refs() -> VisionRefs:
    return VisionRefs(
        raw_screenshot="data/vision/coinglass/raw/screenshot_20260523_060000.png",
        normalized="data/vision/coinglass/normalized/vision_20260523_060000.json",
        latest="data/vision/coinglass/latest.json",
        events="data/vision/coinglass/events.jsonl",
    )


def _make_detection(**kwargs) -> Detection:
    defaults = dict(
        detected_metric_type="liquidations_long",
        extracted_value=48_500_000.0,
        unit="USD",
        confidence=0.82,
        evidence_ref="data/vision/coinglass/raw/screenshot_20260523_060000.png",
        notes="OCR from liquidation bar chart — value readable",
    )
    defaults.update(kwargs)
    return Detection(**defaults)


def _make_valid(**kwargs) -> VisionContextCoinglassV1:
    defaults = dict(
        contract_version="v1",
        input_class="vision_context.coinglass.v1",
        source_id="coinglass_headless_bot",
        screenshot_ts="2026-05-23T06:00:00Z",
        symbol="BTCUSDT",
        timeframe="1H",
        board="liquidations",
        page="liquidation_heatmap",
        freshness_state="fresh",
        detections=[_make_detection()],
        refs=_make_refs(),
        warnings=[],
    )
    defaults.update(kwargs)
    return VisionContextCoinglassV1(**defaults)


class TestVisionContextV1Schema(unittest.TestCase):

    # TC-SCHEMA-01: payload minimal valide
    def test_valid_minimal_payload(self):
        ctx = _make_valid()
        ctx.validate()  # must not raise

    # TC-SCHEMA-02: extracted_value = null autorisé
    def test_null_extracted_value_allowed(self):
        det = _make_detection(extracted_value=None, confidence=0.75)
        ctx = _make_valid(detections=[det])
        ctx.validate()  # must not raise

    # TC-SCHEMA-03: confidence < 0.5 sans warning → BLOCKED
    def test_low_confidence_without_warning_raises(self):
        det = _make_detection(confidence=0.4, extracted_value=None)
        ctx = _make_valid(detections=[det], warnings=[])
        with self.assertRaises(ValueError):
            ctx.validate()

    # TC-SCHEMA-03 (positive): confidence < 0.5 avec warning → OK
    def test_low_confidence_with_warning_passes(self):
        det = _make_detection(confidence=0.4, extracted_value=None)
        ctx = _make_valid(detections=[det], warnings=["low confidence on liquidations_long"])
        ctx.validate()  # must not raise

    # TC-SCHEMA-04: input_class incorrect → BLOCKED
    def test_wrong_input_class_raises(self):
        ctx = _make_valid(input_class="market_metrics.v1")
        with self.assertRaises(ValueError):
            ctx.validate()

    # TC-SCHEMA-04 (contract_version): bad version → BLOCKED
    def test_wrong_contract_version_raises(self):
        ctx = _make_valid(contract_version="v2")
        with self.assertRaises(ValueError):
            ctx.validate()

    # TC-SCHEMA-05: extracted_value non-null mais confidence=0 → BLOCKED
    def test_non_null_value_with_zero_confidence_raises(self):
        det = _make_detection(extracted_value=12345.0, confidence=0.0)
        ctx = _make_valid(detections=[det], warnings=["confidence=0"])
        with self.assertRaises(ValueError):
            ctx.validate()

    # TC-SCHEMA-05 (null + confidence=0): null + confidence=0 → OK
    def test_null_value_with_zero_confidence_allowed(self):
        det = _make_detection(extracted_value=None, confidence=0.0)
        ctx = _make_valid(detections=[det], warnings=["confidence=0, value unreadable"])
        ctx.validate()  # must not raise

    # TC-SCHEMA-06: JSON roundtrip
    def test_json_roundtrip(self):
        ctx = _make_valid()
        payload = json.loads(ctx.to_json())
        self.assertEqual(payload["input_class"], "vision_context.coinglass.v1")
        self.assertEqual(payload["contract_version"], "v1")
        self.assertEqual(len(payload["detections"]), 1)
        det = payload["detections"][0]
        self.assertEqual(det["detected_metric_type"], "liquidations_long")
        self.assertAlmostEqual(det["extracted_value"], 48_500_000.0)
        self.assertEqual(det["confidence"], 0.82)
        self.assertIn("raw_screenshot", payload["refs"])

    def test_multiple_detections_valid(self):
        dets = [
            _make_detection(detected_metric_type="liquidations_long", confidence=0.82),
            _make_detection(detected_metric_type="liquidations_short", extracted_value=21_300_000.0, confidence=0.78),
        ]
        ctx = _make_valid(detections=dets)
        ctx.validate()

    def test_to_dict_structure(self):
        ctx = _make_valid()
        d = ctx.to_dict()
        self.assertIsInstance(d["detections"], list)
        self.assertIsInstance(d["refs"], dict)
        self.assertIn("latest", d["refs"])


if __name__ == "__main__":
    unittest.main()
