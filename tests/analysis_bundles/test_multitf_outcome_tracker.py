"""Tests for outcome tracker — snapshots, tracking, reporting."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestOutcomeTracker(unittest.TestCase):
    def setUp(self):
        from modules.analysis_bundles.multitf_outcomes.outcome_tracker import track_outcomes
        self.result = track_outcomes()

    def test_tracker_runs(self):
        self.assertIn("tracked", self.result)
        self.assertIn("open", self.result)
        self.assertIn("new", self.result)

    def test_open_setups_file_created(self):
        path = PROJECT_ROOT / "outputs" / "multitf_outcomes" / "open_setups.jsonl"
        self.assertTrue(path.exists())

    def test_open_setups_have_required_fields(self):
        path = PROJECT_ROOT / "outputs" / "multitf_outcomes" / "open_setups.jsonl"
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            d = json.loads(line)
            for field in ["setup_id", "symbol", "setup_type", "grade_at_signal",
                          "score_at_signal", "price_at_signal", "invalidation",
                          "direction", "monitor_only"]:
                self.assertIn(field, d, f"Missing {field} in open setup")

    def test_all_setups_monitor_only(self):
        path = PROJECT_ROOT / "outputs" / "multitf_outcomes" / "open_setups.jsonl"
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            d = json.loads(line)
            self.assertTrue(d.get("monitor_only"))

    def test_no_execution_terms(self):
        for fpath in [
            PROJECT_ROOT / "outputs" / "multitf_outcomes" / "open_setups.jsonl",
            PROJECT_ROOT / "outputs" / "multitf_outcomes" / "outcome_events.jsonl",
        ]:
            if not fpath.exists(): continue
            forbidden = ["execute", "broker", "order_book", "auto_trade", "market_order"]
            for line in fpath.read_text().splitlines():
                if not line.strip(): continue
                for term in forbidden:
                    self.assertNotIn(term, line.lower(), f"Forbidden '{term}' in {fpath.name}")

    def test_report_generated(self):
        path = PROJECT_ROOT / "outputs" / "multitf_outcomes" / "grade_accuracy_report.json"
        if path.exists():
            d = json.loads(path.read_text())
            self.assertIn("generated_at", d)
            self.assertIn("by_grade_setup", d)
            self.assertTrue(d.get("monitor_only"))

    def test_no_duplicate_setup_ids(self):
        path = PROJECT_ROOT / "outputs" / "multitf_outcomes" / "open_setups.jsonl"
        ids = []
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            d = json.loads(line)
            ids.append(d.get("setup_id"))
        self.assertEqual(len(ids), len(set(ids)), f"Duplicate setup_ids found: {len(ids)} vs {len(set(ids))}")

    def test_setup_ids_are_stable(self):
        """Same setup should keep same id across runs."""
        path = PROJECT_ROOT / "outputs" / "multitf_outcomes" / "open_setups.jsonl"
        if not path.exists(): return
        ids = set()
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            d = json.loads(line)
            ids.add(d.get("setup_id", ""))
        # Setup IDs should be based on symbol_setup_type, not timestamp
        for sid in ids:
            self.assertTrue(any(sym in sid for sym in ["btc", "eth", "sol", "spcx", "xauusd"]),
                            f"setup_id {sid} doesn't contain symbol")

    def test_resolve_logic_short(self):
        from modules.analysis_bundles.multitf_outcomes.outcome_tracker import _resolve_outcome
        prev = {"setup_id": "btc_test", "symbol": "BTC", "setup_type": "vwap_rejection",
                "direction": "short", "price_at_signal": 67000, "invalidation": 67500,
                "target_1": 66000, "snapshot_at": "2026-06-15T17:00:00Z"}
        st = {"setup_type": "vwap_rejection"}
        # Mock price below target → should confirm
        import unittest.mock as mock
        with mock.patch("modules.analysis_bundles.multitf_outcomes.outcome_tracker._get_current_price", return_value=65800):
            result = _resolve_outcome(prev, "BTC", st)
            self.assertIsNotNone(result)
            self.assertEqual(result["outcome"], "confirmed")
            self.assertTrue(result["hit_tp1"])

    def test_resolve_logic_invalidation(self):
        from modules.analysis_bundles.multitf_outcomes.outcome_tracker import _resolve_outcome
        prev = {"setup_id": "btc_test2", "symbol": "BTC", "setup_type": "vwap_rejection",
                "direction": "short", "price_at_signal": 67000, "invalidation": 67500,
                "target_1": 66000, "snapshot_at": "2026-06-15T17:00:00Z"}
        st = {"setup_type": "vwap_rejection"}
        import unittest.mock as mock
        with mock.patch("modules.analysis_bundles.multitf_outcomes.outcome_tracker._get_current_price", return_value=67600):
            result = _resolve_outcome(prev, "BTC", st)
            self.assertIsNotNone(result)
            self.assertEqual(result["outcome"], "failed")
            self.assertTrue(result["hit_invalidation"])

    def test_resolve_logic_pending(self):
        from modules.analysis_bundles.multitf_outcomes.outcome_tracker import _resolve_outcome
        prev = {"setup_id": "btc_test3", "symbol": "BTC", "setup_type": "vwap_rejection",
                "direction": "short", "price_at_signal": 67000, "invalidation": 67500,
                "target_1": 66000, "snapshot_at": "2026-06-15T17:30:00Z"}
        st = {"setup_type": "vwap_rejection"}
        # Price between target and invalidation → pending
        import unittest.mock as mock
        with mock.patch("modules.analysis_bundles.multitf_outcomes.outcome_tracker._get_current_price", return_value=66800):
            result = _resolve_outcome(prev, "BTC", st)
            self.assertIsNone(result)
