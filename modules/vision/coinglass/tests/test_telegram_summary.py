import json
import unittest
from pathlib import Path

from modules.vision.coinglass.telegram_summary import format_vision_summary, load_and_format
from modules.vision.coinglass.vision_context_v1 import Detection, VisionContextCoinglassV1, VisionRefs

FIXTURE_DIR = Path("tests/fixtures/vision/coinglass")


def _make_refs() -> VisionRefs:
    return VisionRefs(
        raw_screenshot="data/vision/coinglass/raw/screenshot.png",
        normalized="data/vision/coinglass/normalized/v.json",
        latest="data/vision/coinglass/latest.json",
        events="data/vision/coinglass/events.jsonl",
    )


def _make_ctx(detections=None, warnings=None) -> VisionContextCoinglassV1:
    return VisionContextCoinglassV1(
        contract_version="v1",
        input_class="vision_context.coinglass.v1",
        source_id="coinglass_headless_bot",
        screenshot_ts="2026-05-23T06:00:00Z",
        symbol="BTCUSDT",
        timeframe="1H",
        board="liquidations",
        page="liquidation_heatmap",
        freshness_state="fresh",
        detections=detections or [],
        refs=_make_refs(),
        warnings=warnings or [],
    )


class TestFormatVisionSummary(unittest.TestCase):

    # TC-B2-01: message contient uniquement les valeurs extraites — pas d'invention
    def test_values_match_detections_exactly(self):
        dets = [
            Detection("liquidations_long", 48_500_000.0, "USD", 0.82, "ref.png", ""),
            Detection("liquidations_short", 21_300_000.0, "USD", 0.78, "ref.png", ""),
        ]
        ctx = _make_ctx(detections=dets)
        msg = format_vision_summary(ctx)
        self.assertIn("$48.50M", msg)
        self.assertIn("$21.30M", msg)
        # No extra invented numbers
        self.assertNotIn("$0.00", msg)

    # TC-B2-02: confidence < 0.85 → warning explicite dans message
    def test_partial_confidence_flagged(self):
        dets = [Detection("liquidations_long", 48_500_000.0, "USD", 0.82, "ref.png", "")]
        ctx = _make_ctx(detections=dets)
        msg = format_vision_summary(ctx)
        self.assertIn("conf=82%", msg)
        self.assertIn("⚠", msg)

    # TC-B2-02: confidence ≥ 0.85 → pas de tag warning
    def test_high_confidence_no_warning_tag(self):
        dets = [Detection("liquidations_long", 48_500_000.0, "USD", 0.90, "ref.png", "")]
        ctx = _make_ctx(detections=dets)
        msg = format_vision_summary(ctx)
        self.assertNotIn("⚠", msg)
        self.assertNotIn("conf=", msg)

    # TC-B2-02: confidence < 0.60 → tag ✗ low
    def test_low_confidence_flagged_with_x(self):
        dets = [Detection("liquidations_long", None, "USD", 0.45, "ref.png", "unreadable")]
        ctx = _make_ctx(detections=dets, warnings=["low confidence"])
        msg = format_vision_summary(ctx)
        self.assertIn("✗", msg)
        self.assertIn("(low)", msg)

    # extracted_value null → "N/A" dans le message, pas d'invention
    def test_null_value_shows_na(self):
        dets = [Detection("liquidations_short", None, "USD", 0.72, "ref.png", "not visible")]
        ctx = _make_ctx(detections=dets)
        msg = format_vision_summary(ctx)
        self.assertIn("N/A", msg)
        self.assertNotIn("$0", msg)

    # Warnings globaux apparaissent dans le message
    def test_global_warnings_shown(self):
        ctx = _make_ctx(
            detections=[Detection("liquidations_long", None, "USD", 0.35, "ref.png", "")],
            warnings=["liquidations_long: confidence 0.35 < 0.5 — value set to null"],
        )
        msg = format_vision_summary(ctx)
        self.assertIn("Warnings", msg)
        self.assertIn("liquidations_long", msg)

    # Aucune détection → "No detections."
    def test_empty_detections_message(self):
        ctx = _make_ctx(detections=[])
        msg = format_vision_summary(ctx)
        self.assertIn("No detections", msg)

    # Header contient symbole, timeframe, board
    def test_header_contains_symbol_and_timeframe(self):
        ctx = _make_ctx()
        msg = format_vision_summary(ctx)
        self.assertIn("BTCUSDT", msg)
        self.assertIn("1H", msg)
        self.assertIn("liquidations", msg)
        self.assertIn("2026-05-23T06:00:00Z", msg)

    # Format USD : millions → $xM
    def test_usd_format_millions(self):
        dets = [Detection("open_interest", 2_500_000_000.0, "USD", 0.88, "ref.png", "")]
        ctx = _make_ctx(detections=dets)
        msg = format_vision_summary(ctx)
        self.assertIn("$2500.00M", msg)

    # load_and_format: fichier absent → None
    def test_load_absent_file_returns_none(self, tmp_path=None):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            result = load_and_format(path=Path(td) / "missing.json")
            self.assertIsNone(result)

    # load_and_format: input_class incorrect → None
    def test_load_wrong_input_class_returns_none(self):
        import tempfile, json
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "latest.json"
            p.write_text(json.dumps({"input_class": "market_metrics.v1"}))
            self.assertIsNone(load_and_format(path=p))

    # load_and_format: fixture valide → message non vide
    def test_load_valid_fixture_returns_message(self):
        fixture = FIXTURE_DIR / "vision_coinglass_v1_valid.json"
        if not fixture.exists():
            self.skipTest("fixture not present")
        msg = load_and_format(path=fixture)
        self.assertIsNotNone(msg)
        self.assertIn("BTCUSDT", msg)
        self.assertGreater(len(msg), 50)


if __name__ == "__main__":
    unittest.main()
