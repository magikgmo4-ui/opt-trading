import json
import os
import shutil
import unittest
from datetime import datetime, timezone
from pathlib import Path

from modules.vision.coinglass.headless_capture import capture_screenshot
from modules.vision.coinglass.runner import run_capture
from modules.vision.coinglass.vision_context_v1 import Detection

FIXTURE_PNG = Path("tests/fixtures/vision/coinglass/screenshot_mock_liquidations.png")

_FIXED_TS = datetime(2026, 5, 23, 6, 0, 0, tzinfo=timezone.utc)

# ── mock fns ──────────────────────────────────────────────────────────────────

def _browser_fn_ok(url: str, dest_dir: Path, ts: datetime) -> Path:
    dest = dest_dir / f"screenshot_{ts.strftime('%Y%m%d_%H%M%S')}.png"
    shutil.copy(FIXTURE_PNG, dest)
    return dest


def _extraction_fn_two(path: Path):
    return [
        Detection("liquidations_long", 48_500_000.0, "USD", 0.82, str(path), ""),
        Detection("liquidations_short", 21_300_000.0, "USD", 0.78, str(path), ""),
    ]


def _extraction_fn_empty(path: Path):
    return []


# ── helpers ───────────────────────────────────────────────────────────────────

def _enable_gate():
    os.environ["VISION_BOT_ENABLED"] = "true"


def _disable_gate():
    os.environ.pop("VISION_BOT_ENABLED", None)


class TestGate(unittest.TestCase):

    def setUp(self):
        _disable_gate()

    def tearDown(self):
        _disable_gate()

    # Gate OFF → RuntimeError
    def test_capture_screenshot_without_gate_raises(self):
        with self.assertRaises(RuntimeError):
            capture_screenshot(browser_fn=_browser_fn_ok)

    def test_run_capture_without_gate_raises(self, tmp_path=None):
        with self.assertRaises(RuntimeError):
            run_capture(
                browser_fn=_browser_fn_ok,
                extraction_fn=_extraction_fn_two,
            )


class TestRunCapture(unittest.TestCase):

    def setUp(self):
        _enable_gate()
        # Override write roots to tmp dirs for isolation
        import modules.vision.coinglass.runner as r
        self._runner = r

    def tearDown(self):
        _disable_gate()

    def _run(self, tmp_path: Path, extraction_fn=None):
        import modules.vision.coinglass.runner as r
        # Monkey-patch write paths to tmp_path
        orig_vision = r._VISION_DIR
        orig_deskpro = r._DESKPRO_INPUT
        r._VISION_DIR = tmp_path / "data/vision/coinglass"
        r._DESKPRO_INPUT = tmp_path / "data/deskpro/inputs/vision_context/coinglass/latest.json"
        try:
            ctx = run_capture(
                browser_fn=_browser_fn_ok,
                extraction_fn=extraction_fn or _extraction_fn_two,
                run_ts=_FIXED_TS,
            )
        finally:
            r._VISION_DIR = orig_vision
            r._DESKPRO_INPUT = orig_deskpro
        return ctx

    # TC-B1: screenshot produit — PNG non vide dans raw/
    def test_screenshot_written_non_empty(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            self._run(tmp)
            raws = list((tmp / "data/vision/coinglass/raw").glob("*.png"))
            self.assertEqual(len(raws), 1)
            self.assertGreater(raws[0].stat().st_size, 0)

    # TC-B1: parsing non vide — au moins 1 détection confidence ≥ 0.6
    def test_detections_returned(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            ctx = self._run(Path(td))
            self.assertGreaterEqual(len(ctx.detections), 1)
            self.assertTrue(all(d.confidence >= 0.60 for d in ctx.detections))

    # TC-B1: latest.json mis à jour — screenshot_ts = run_ts ± 60s
    def test_latest_json_screenshot_ts(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            self._run(tmp)
            latest = tmp / "data/vision/coinglass/latest.json"
            self.assertTrue(latest.exists())
            data = json.loads(latest.read_text())
            self.assertEqual(data["screenshot_ts"], "2026-05-23T06:00:00Z")
            self.assertEqual(data["input_class"], "vision_context.coinglass.v1")

    # TC-B1: events.jsonl appended
    def test_events_jsonl_appended(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            self._run(tmp)
            self._run(tmp)  # second run
            events = tmp / "data/vision/coinglass/events.jsonl"
            lines = [l for l in events.read_text().splitlines() if l.strip()]
            self.assertEqual(len(lines), 2)

    # TC-B1: Desk Pro input written
    def test_deskpro_input_written(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            self._run(tmp)
            dp = tmp / "data/deskpro/inputs/vision_context/coinglass/latest.json"
            self.assertTrue(dp.exists())
            data = json.loads(dp.read_text())
            self.assertEqual(data["input_class"], "vision_context.coinglass.v1")

    # TC-B1: no write outside vision/ and deskpro/inputs/vision_context/
    def test_no_write_outside_allowed_dirs(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            self._run(tmp)
            all_written = set(tmp.rglob("*"))
            for f in all_written:
                if f.is_file():
                    rel = f.relative_to(tmp)
                    parts = rel.parts
                    allowed = (
                        parts[:4] == ("data", "vision", "coinglass", "raw")
                        or parts[:4] == ("data", "vision", "coinglass", "normalized")
                        or (parts[:3] == ("data", "vision", "coinglass") and len(parts) == 4)
                        or parts[:5] == ("data", "deskpro", "inputs", "vision_context", "coinglass")
                    )
                    self.assertTrue(allowed, f"unexpected write: {rel}")

    # Empty extraction → context with 0 detections, still writes files
    def test_empty_extraction_writes_files(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            ctx = self._run(tmp, extraction_fn=_extraction_fn_empty)
            self.assertEqual(len(ctx.detections), 0)
            self.assertTrue((tmp / "data/vision/coinglass/latest.json").exists())


if __name__ == "__main__":
    unittest.main()
