import json
import unittest
from pathlib import Path

from modules.vision.coinglass.staging_validator import (
    RunResult,
    ValidationReport,
    validate_staging_runs,
)

_TS = "2026-05-23T06:00:00Z"


def _event(detections=None, ts=_TS) -> dict:
    return {
        "input_class": "vision_context.coinglass.v1",
        "screenshot_ts": ts,
        "detections": detections or [],
    }


def _det(confidence=0.82, value=48_500_000.0) -> dict:
    return {
        "detected_metric_type": "liquidations_long",
        "extracted_value": value,
        "unit": "USD",
        "confidence": confidence,
        "evidence_ref": "data/vision/coinglass/raw/screenshot.png",
        "notes": "",
    }


def _write_events(tmp_path: Path, events: list) -> Path:
    p = tmp_path / "events.jsonl"
    with p.open("w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")
    return p


class TestStagingValidator(unittest.TestCase):

    # 3 runs PASS → ok=True
    def test_three_pass_runs_returns_ok(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = _write_events(Path(td), [
                _event([_det(0.82)], "2026-05-23T04:00:00Z"),
                _event([_det(0.78)], "2026-05-23T05:00:00Z"),
                _event([_det(0.91)], "2026-05-23T06:00:00Z"),
            ])
            report = validate_staging_runs(p, required_passes=3)
            self.assertTrue(report.ok)
            self.assertEqual(report.evaluated, 3)
            self.assertIn("PASS", report.message)

    # 2 PASS + 1 FAIL → ok=False
    def test_one_fail_run_returns_not_ok(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = _write_events(Path(td), [
                _event([_det(0.82)], "2026-05-23T04:00:00Z"),
                _event([], "2026-05-23T05:00:00Z"),          # FAIL — no detections
                _event([_det(0.78)], "2026-05-23T06:00:00Z"),
            ])
            report = validate_staging_runs(p, required_passes=3)
            self.assertFalse(report.ok)
            self.assertIn("FAIL", report.message)

    # Fichier absent → ok=False
    def test_absent_file_returns_not_ok(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            report = validate_staging_runs(Path(td) / "missing.jsonl", required_passes=3)
            self.assertFalse(report.ok)
            self.assertEqual(report.evaluated, 0)

    # Fichier vide → ok=False
    def test_empty_file_returns_not_ok(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "events.jsonl"
            p.write_text("")
            report = validate_staging_runs(p, required_passes=3)
            self.assertFalse(report.ok)
            self.assertIn("empty", report.message)

    # Moins de N runs → INSUFFICIENT
    def test_fewer_than_required_runs_insufficient(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = _write_events(Path(td), [_event([_det(0.82)])])
            report = validate_staging_runs(p, required_passes=3)
            self.assertFalse(report.ok)
            self.assertIn("INSUFFICIENT", report.message)

    # confidence < 0.60 → FAIL (même si value non-null)
    def test_low_confidence_detection_fails(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = _write_events(Path(td), [
                _event([_det(0.45)], "2026-05-23T06:00:00Z"),
                _event([_det(0.82)], "2026-05-23T07:00:00Z"),
                _event([_det(0.78)], "2026-05-23T08:00:00Z"),
            ])
            report = validate_staging_runs(p, required_passes=3)
            self.assertFalse(report.ok)
            fail_runs = [r for r in report.results if not r.passed]
            self.assertEqual(len(fail_runs), 1)

    # null extracted_value → FAIL même si confidence OK
    def test_null_value_detection_fails(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = _write_events(Path(td), [
                _event([_det(0.82, value=None)]),
                _event([_det(0.78)]),
                _event([_det(0.91)]),
            ])
            report = validate_staging_runs(p, required_passes=3)
            self.assertFalse(report.ok)

    # Seuls les N derniers runs comptent
    def test_only_last_n_runs_evaluated(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            # 5 events: first 2 fail, last 3 pass
            p = _write_events(Path(td), [
                _event([], "2026-05-23T01:00:00Z"),           # old FAIL — ignored
                _event([], "2026-05-23T02:00:00Z"),           # old FAIL — ignored
                _event([_det(0.82)], "2026-05-23T03:00:00Z"),
                _event([_det(0.78)], "2026-05-23T04:00:00Z"),
                _event([_det(0.91)], "2026-05-23T05:00:00Z"),
            ])
            report = validate_staging_runs(p, required_passes=3)
            self.assertTrue(report.ok)
            self.assertEqual(report.evaluated, 3)

    # Ligne JSON malformée → RunResult.passed=False
    def test_malformed_json_line_counts_as_fail(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "events.jsonl"
            p.write_text(
                json.dumps(_event([_det(0.82)])) + "\n"
                + "NOT_JSON{{{\n"
                + json.dumps(_event([_det(0.78)])) + "\n"
            )
            report = validate_staging_runs(p, required_passes=3)
            self.assertFalse(report.ok)
            bad = [r for r in report.results if r.screenshot_ts == "?"]
            self.assertEqual(len(bad), 1)

    # required_passes=1 avec 1 bon run → ok=True
    def test_required_one_pass(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = _write_events(Path(td), [_event([_det(0.82)])])
            report = validate_staging_runs(p, required_passes=1)
            self.assertTrue(report.ok)


if __name__ == "__main__":
    unittest.main()
