import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from modules.vision.coinglass.parser import parse_screenshot, CONFIDENCE_THRESHOLD
from modules.vision.coinglass.vision_context_v1 import Detection

FIXTURE_DIR = Path("tests/fixtures/vision/coinglass")
MOCK_IMAGE = FIXTURE_DIR / "screenshot_mock_liquidations.png"
ABSENT_IMAGE = FIXTURE_DIR / "does_not_exist.png"

_TS_FRESH = datetime.now(tz=timezone.utc) - timedelta(hours=1)
_TS_STALE = datetime.now(tz=timezone.utc) - timedelta(hours=5)


def _mock_extraction_two(path: Path):
    return [
        Detection("liquidations_long", 48_500_000.0, "USD", 0.82, str(path), ""),
        Detection("liquidations_short", 21_300_000.0, "USD", 0.78, str(path), ""),
    ]


def _mock_extraction_low_conf(path: Path):
    return [
        Detection("liquidations_long", 12_000_000.0, "USD", 0.45, str(path), ""),
        Detection("liquidations_short", 9_000_000.0, "USD", 0.82, str(path), ""),
    ]


def _mock_extraction_empty(path: Path):
    return []


class TestParserMock(unittest.TestCase):

    # TC-PARSER-01: mock extraction depuis fixture image → 2+ détections retournées
    def test_mock_extraction_returns_two_detections(self):
        dets, warnings, _ = parse_screenshot(
            MOCK_IMAGE, _TS_FRESH, _mock_extraction_two
        )
        self.assertGreaterEqual(len(dets), 2)
        types = {d.detected_metric_type for d in dets}
        self.assertIn("liquidations_long", types)
        self.assertIn("liquidations_short", types)

    # TC-PARSER-02: confidence threshold appliqué — valeur < 0.6 → null + warning
    def test_low_confidence_sets_null_and_warning(self):
        dets, warnings, _ = parse_screenshot(
            MOCK_IMAGE, _TS_FRESH, _mock_extraction_low_conf,
            confidence_threshold=CONFIDENCE_THRESHOLD,
        )
        low = [d for d in dets if d.detected_metric_type == "liquidations_long"]
        self.assertEqual(len(low), 1)
        self.assertIsNone(low[0].extracted_value)
        self.assertTrue(any("liquidations_long" in w for w in warnings))

        high = [d for d in dets if d.detected_metric_type == "liquidations_short"]
        self.assertEqual(len(high), 1)
        self.assertIsNotNone(high[0].extracted_value)

    # TC-PARSER-03: fichier absent → liste vide, pas d'exception
    def test_absent_file_returns_empty_no_exception(self):
        dets, warnings, freshness = parse_screenshot(
            ABSENT_IMAGE, _TS_FRESH, _mock_extraction_two
        )
        self.assertEqual(dets, [])
        self.assertEqual(freshness, "unknown")

    # TC-PARSER-04: freshness_state = "stale" si screenshot > 4h
    def test_stale_freshness_when_screenshot_over_4h(self):
        _, _, freshness = parse_screenshot(
            MOCK_IMAGE, _TS_STALE, _mock_extraction_two
        )
        self.assertEqual(freshness, "stale")

    # TC-PARSER-04 (positive): fresh quand < 4h
    def test_fresh_freshness_when_screenshot_under_4h(self):
        _, _, freshness = parse_screenshot(
            MOCK_IMAGE, _TS_FRESH, _mock_extraction_two
        )
        self.assertEqual(freshness, "fresh")

    # extraction_fn crash → silent degradation
    def test_extraction_fn_exception_returns_empty(self):
        def _boom(path):
            raise RuntimeError("OCR failure")

        dets, warnings, freshness = parse_screenshot(
            MOCK_IMAGE, _TS_FRESH, _boom
        )
        self.assertEqual(dets, [])
        self.assertEqual(freshness, "unknown")

    # extraction returns empty → still valid (no detections)
    def test_empty_extraction_passes(self):
        dets, warnings, freshness = parse_screenshot(
            MOCK_IMAGE, _TS_FRESH, _mock_extraction_empty
        )
        self.assertEqual(dets, [])
        self.assertEqual(warnings, [])
        self.assertEqual(freshness, "fresh")


if __name__ == "__main__":
    unittest.main()
