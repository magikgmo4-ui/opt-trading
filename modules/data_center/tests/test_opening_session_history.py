from __future__ import annotations

"""Unit tests for opening session history logger."""

import json
import tempfile
import unittest
from pathlib import Path

from modules.data_center.opening_session_history import (
    log_opening_event,
    read_opening_history,
    update_outcome,
)


class TestHistoryLogger(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()) / "history.jsonl"

    def test_log_opening_event_creates_entry(self):
        entry = log_opening_event(
            event={"symbol": "SPCX", "event": "VWAP_RECLAIM", "price": 173.77, "_ts": "2026-06-16T14:30:00Z"},
            opening_metrics={"opening_gap_pct": 0.5, "risk_score": 20},
            score_result={"score": 55, "grade": "B", "events": ["VWAP_RECLAIM"], "setup_state": "active",
                          "opening_components": {"dynamic_boost": 10}},
            history_path=self.tmp,
        )
        self.assertEqual(entry["symbol"], "SPCX")
        self.assertEqual(entry["event"], "VWAP_RECLAIM")
        self.assertEqual(entry["score"], 55)
        self.assertEqual(entry["opening_gap_pct"], 0.5)
        self.assertEqual(entry["risk_score"], 20)
        self.assertIsNone(entry["outcome_5m"])
        self.assertTrue(entry["monitor_only"])

    def test_read_opening_history_returns_entries(self):
        log_opening_event(
            event={"symbol": "SPCX", "event": "VWAP_RECLAIM", "price": 173.77, "_ts": "2026-06-16T14:30:00Z"},
            opening_metrics={},
            score_result={"score": 55, "grade": "B", "events": [], "setup_state": "watch",
                          "opening_components": {"dynamic_boost": 0}},
            history_path=self.tmp,
        )
        entries = read_opening_history(limit=10, history_path=self.tmp)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["event"], "VWAP_RECLAIM")

    def test_update_outcome_modifies_entry(self):
        entry = log_opening_event(
            event={"symbol": "SPCX", "event": "VWAP_RECLAIM", "price": 173.77, "_ts": "2026-06-16T14:30:00Z"},
            opening_metrics={},
            score_result={"score": 55, "grade": "B", "events": [], "setup_state": "watch",
                          "opening_components": {"dynamic_boost": 0}},
            history_path=self.tmp,
        )
        ts = entry["timestamp"]
        updated = update_outcome(ts, "outcome_5m", {"price": 175.0, "direction": "up"},
                                 history_path=self.tmp)
        self.assertTrue(updated)
        entries = read_opening_history(limit=10, history_path=self.tmp)
        self.assertEqual(entries[0]["outcome_5m"]["price"], 175.0)
        self.assertEqual(entries[0]["outcome_5m"]["direction"], "up")

    def test_update_outcome_nonexistent_returns_false(self):
        result = update_outcome("nonexistent_ts", "outcome_5m", {}, history_path=self.tmp)
        self.assertFalse(result)

    def test_empty_history_returns_empty_list(self):
        entries = read_opening_history(limit=10, history_path=self.tmp)
        self.assertEqual(entries, [])

    def test_malformed_lines_skipped(self):
        self.tmp.parent.mkdir(parents=True, exist_ok=True)
        self.tmp.write_text("{bad json\n{also bad\n", encoding="utf-8")
        entries = read_opening_history(limit=10, history_path=self.tmp)
        self.assertEqual(entries, [])


if __name__ == "__main__":
    unittest.main()
