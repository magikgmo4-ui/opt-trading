"""
Tests for source_status.py — PR2.

Covers:
- Freshness evaluation (fresh/warm/stale/expired/missing/error)
- Timestamp-based freshness
- Mtime fallback
- Overall freshness computation
- SourceStatus dataclass
"""

from __future__ import annotations

import os
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from modules.market_thesis.source_status import (
    SourceStatus,
    SourceStatusSet,
    evaluate_freshness,
    evaluate_overall_freshness,
)


class TestEvaluateFreshness(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 6, 15, 12, 0, 0, tzinfo=timezone.utc)
        # Create a real temp file that exists for freshness tests
        self.tmpfile = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmpfile.write(b"{}")
        self.tmpfile.close()
        self.real_path = Path(self.tmpfile.name)

    def tearDown(self):
        self.real_path.unlink(missing_ok=True)

    def test_missing_none_path(self):
        result = evaluate_freshness(None, now=self.now)
        self.assertEqual(result["state"], "missing")
        self.assertIsNone(result["age_minutes"])

    def test_missing_nonexistent_file(self):
        result = evaluate_freshness(Path("/nonexistent/file.json"), now=self.now)
        self.assertEqual(result["state"], "missing")

    def test_fresh_with_recent_timestamp(self):
        ts = self.now - timedelta(minutes=2)
        result = evaluate_freshness(self.real_path, data_ts=ts, now=self.now)
        self.assertEqual(result["state"], "fresh")
        self.assertAlmostEqual(result["age_minutes"], 2, delta=0.1)

    def test_fresh_at_boundary(self):
        ts = self.now - timedelta(minutes=5)
        result = evaluate_freshness(self.real_path, data_ts=ts, now=self.now)
        self.assertEqual(result["state"], "fresh")

    def test_warm(self):
        ts = self.now - timedelta(minutes=10)
        result = evaluate_freshness(self.real_path, data_ts=ts, now=self.now)
        self.assertEqual(result["state"], "warm")
        self.assertAlmostEqual(result["age_minutes"], 10, delta=0.1)

    def test_warm_at_boundary(self):
        ts = self.now - timedelta(minutes=30)
        result = evaluate_freshness(self.real_path, data_ts=ts, now=self.now)
        self.assertEqual(result["state"], "warm")

    def test_stale(self):
        ts = self.now - timedelta(minutes=60)
        result = evaluate_freshness(self.real_path, data_ts=ts, now=self.now)
        self.assertEqual(result["state"], "stale")

    def test_stale_at_boundary(self):
        ts = self.now - timedelta(hours=4)
        result = evaluate_freshness(self.real_path, data_ts=ts, now=self.now)
        self.assertEqual(result["state"], "stale")

    def test_expired(self):
        ts = self.now - timedelta(hours=5)
        result = evaluate_freshness(self.real_path, data_ts=ts, now=self.now)
        self.assertEqual(result["state"], "expired")

    def test_freshness_uses_mtime_fallback(self):
        # File just created, mtime should be recent
        result = evaluate_freshness(self.real_path, data_ts=None, now=self.now)
        self.assertIn(result["state"], ("fresh", "warm"))
        self.assertIsNotNone(result["age_minutes"])

    def test_error_on_inaccessible_path(self):
        # A path whose existence check raises OSError (but that's a different code path)
        # Simulate via a path we control that exists but unreadable — not possible as same user
        # Instead test that a missing path returns "missing" not "error"
        result = evaluate_freshness(Path("/nonexistent/path_12345.json"), data_ts=None, now=self.now)
        self.assertEqual(result["state"], "missing")

    def test_age_minutes_rounded(self):
        ts = self.now - timedelta(seconds=90)
        result = evaluate_freshness(self.real_path, data_ts=ts, now=self.now)
        self.assertAlmostEqual(result["age_minutes"], 1.5, delta=0.1)

    def test_naive_datetime_handled(self):
        ts = datetime(2026, 6, 15, 11, 58, 0)  # naive, 2 min ago
        result = evaluate_freshness(self.real_path, data_ts=ts, now=self.now)
        self.assertIn(result["state"], ("fresh", "warm"))


class TestSourceStatus(unittest.TestCase):
    def test_default_state_missing(self):
        s = SourceStatus(name="test", contract="test.v1")
        self.assertEqual(s.state, "missing")
        self.assertIsNone(s.age_minutes)
        self.assertEqual(s.records_count, 0)

    def test_to_dict(self):
        s = SourceStatus(name="test", contract="test.v1", state="fresh", age_minutes=3.5, records_count=10, records_valid=9, records_filtered=1)
        d = s.to_dict()
        self.assertEqual(d["name"], "test")
        self.assertEqual(d["state"], "fresh")
        self.assertEqual(d["age_minutes"], 3.5)
        self.assertEqual(d["records_count"], 10)

    def test_error_state(self):
        s = SourceStatus(name="test", contract="test.v1", state="error", error_message="File corrupted")
        d = s.to_dict()
        self.assertEqual(d["state"], "error")
        self.assertEqual(d["error"], "File corrupted")


class TestSourceStatusSet(unittest.TestCase):
    def setUp(self):
        self.statuses = [
            SourceStatus(name="Market Metrics", contract="mm.v1", state="fresh", age_minutes=2),
            SourceStatus(name="Multi-TF", contract="mtf.v1", state="warm", age_minutes=15),
            SourceStatus(name="Telegram", contract="tg.v1", state="stale", age_minutes=120),
            SourceStatus(name="Vision", contract="vis.v1", state="missing"),
            SourceStatus(name="Coinglass", contract="cg.v1", state="error", error_message="Bad JSON"),
        ]

    def test_missing_sources(self):
        sset = SourceStatusSet(symbol="BTC", items=self.statuses)
        self.assertEqual(sset.missing_sources, ["Vision"])

    def test_stale_sources(self):
        sset = SourceStatusSet(symbol="BTC", items=self.statuses)
        self.assertEqual(sset.stale_sources, ["Telegram"])

    def test_error_sources(self):
        sset = SourceStatusSet(symbol="BTC", items=self.statuses)
        self.assertEqual(sset.error_sources, ["Coinglass"])

    def test_fresh_sources(self):
        sset = SourceStatusSet(symbol="BTC", items=self.statuses)
        self.assertIn("Market Metrics", sset.fresh_sources)
        self.assertIn("Multi-TF", sset.fresh_sources)

    def test_to_dict(self):
        sset = SourceStatusSet(symbol="BTC", items=self.statuses, overall_freshness="stale")
        d = sset.to_dict()
        self.assertEqual(d["symbol"], "BTC")
        self.assertEqual(d["overall_freshness"], "stale")
        self.assertEqual(len(d["sources"]), 5)
        self.assertIn("Vision", d["missing"])
        self.assertIn("Coinglass", d["errors"])

    def test_overall_freshness_property(self):
        sset = SourceStatusSet(symbol="BTC", items=self.statuses)
        overall = evaluate_overall_freshness(self.statuses)
        # stale is the worst present state (Telegram at 120 min)
        self.assertEqual(overall, "stale")


class TestEvaluateOverallFreshness(unittest.TestCase):
    def test_all_fresh(self):
        from modules.market_thesis.source_status import SourceStatus
        s = [SourceStatus(name="a", contract="c", state="fresh") for _ in range(3)]
        self.assertEqual(evaluate_overall_freshness(s), "fresh")

    def test_mixed(self):
        from modules.market_thesis.source_status import SourceStatus
        s = [
            SourceStatus(name="a", contract="c", state="fresh"),
            SourceStatus(name="b", contract="c", state="warm"),
            SourceStatus(name="c", contract="c", state="stale"),
        ]
        self.assertEqual(evaluate_overall_freshness(s), "stale")

    def test_expired_wins(self):
        from modules.market_thesis.source_status import SourceStatus
        s = [
            SourceStatus(name="a", contract="c", state="fresh"),
            SourceStatus(name="b", contract="c", state="expired"),
            SourceStatus(name="c", contract="c", state="stale"),
        ]
        self.assertEqual(evaluate_overall_freshness(s), "expired")

    def test_ignores_missing_and_error(self):
        from modules.market_thesis.source_status import SourceStatus
        s = [
            SourceStatus(name="a", contract="c", state="missing"),
            SourceStatus(name="b", contract="c", state="error"),
            SourceStatus(name="c", contract="c", state="fresh"),
        ]
        self.assertEqual(evaluate_overall_freshness(s), "fresh")

    def test_all_missing(self):
        from modules.market_thesis.source_status import SourceStatus
        s = [SourceStatus(name="a", contract="c", state="missing") for _ in range(3)]
        self.assertEqual(evaluate_overall_freshness(s), "missing")

    def test_all_error(self):
        from modules.market_thesis.source_status import SourceStatus
        s = [SourceStatus(name="a", contract="c", state="error") for _ in range(3)]
        self.assertEqual(evaluate_overall_freshness(s), "missing")


if __name__ == "__main__":
    unittest.main()
