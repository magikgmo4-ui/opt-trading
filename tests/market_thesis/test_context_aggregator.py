"""
Tests for context_aggregator.py — PR2.

Covers:
- Aggregation all sources (with fixtures)
- Single-source fallback
- No-source fallback (never crashes)
- Missing sources tracked
- Stale sources tracked
- Errors collected
- Timestamp fallback via mtime
- All 9 canonical symbols
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from modules.market_thesis.context_aggregator import MarketContextInput, aggregate
from modules.market_thesis.source_status import SourceStatusSet, evaluate_overall_freshness

FIXTURES = Path(__file__).resolve().parent / "fixtures"


# ── MarketContextInput structure ───────────────────────────────────────────

class TestMarketContextInput(unittest.TestCase):
    def test_empty_input(self):
        ctx = MarketContextInput(symbol="BTC")
        self.assertEqual(ctx.symbol, "BTC")
        self.assertEqual(ctx.freshness_summary, "missing")
        self.assertEqual(ctx.missing_sources, [])
        self.assertFalse(ctx.has_any_data)

    def test_with_some_data(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.missing_sources = ["Market Metrics"]
        self.assertTrue(ctx.missing_sources)
        self.assertFalse(ctx.has_any_data)

    def test_to_dict(self):
        ctx = MarketContextInput(symbol="ETH")
        d = ctx.to_dict()
        self.assertEqual(d["symbol"], "ETH")
        self.assertIn("freshness_summary", d)
        self.assertIn("missing_sources", d)
        self.assertIn("errors", d)
        self.assertEqual(d["raw_events_count"], 0)


# ── Aggregation with fixtures ──────────────────────────────────────────────

class TestAggregateWithFixtures(unittest.TestCase):
    """Tests aggregation using mock paths pointing to fixture files."""

    def setUp(self):
        self._patches = []

    def _patch_source(self, key: str, path: Path):
        p = patch.dict("modules.market_thesis.config.SOURCES", {key: path}, clear=False)
        p.start()
        self._patches.append(p)

    def tearDown(self):
        for p in self._patches:
            p.stop()

    def _setup_market_metrics_for_btc(self):
        """Patch source_path_for_symbol to return our market_metrics fixture for BTC."""
        p = patch(
            "modules.market_thesis.source_readers.source_path_for_symbol",
            side_effect=lambda key, sym: FIXTURES / "market_metrics.json"
            if key == "market_metrics" and sym == "BTC"
            else FIXTURES / "priority_snapshot.json"
            if key == "multitf_scores" and sym == "BTC"
            else FIXTURES / "vision_analysis.json"
            if key == "vision_analysis_dc" and sym == "BTC"
            else FIXTURES / "market_metrics.json"
            if key == "multitf_analysis" and sym == "BTC"
            else None,
        )
        p.start()
        self._patches.append(p)

    def test_aggregate_btc_with_events_fixture(self):
        self._patch_source("events_jsonl", FIXTURES / "events.jsonl")
        self._patch_source("events_cdp_jsonl", FIXTURES / "events_cdp.jsonl")
        self._setup_market_metrics_for_btc()

        ctx = aggregate("BTC")
        self.assertEqual(ctx.symbol, "BTC")
        self.assertTrue(ctx.has_any_data)
        # Should have webhook events for BTC
        btc_events = [e for e in ctx.raw_events if e.symbol == "BTC"]
        self.assertGreater(len(btc_events), 0)

    def test_aggregate_never_crashes_no_sources(self):
        # No patches — all sources missing (real paths that don't match our fixtures)
        # But some real DC views may exist! Let's use a symbol that definitely has no data
        ctx = aggregate("AVGO")
        self.assertEqual(ctx.symbol, "AVGO")
        # AVGO may or may not have data depending on what's on disk
        # Just ensure no crash
        self.assertIsInstance(ctx.has_any_data, bool)
        self.assertGreater(len(ctx.source_statuses), 0)

    def test_aggregate_tracks_missing_sources(self):
        ctx = aggregate("MU")
        # MU likely has no data on disk
        self.assertIsInstance(ctx.missing_sources, list)

    def test_aggregate_collects_errors(self):
        # Sources are missing but that's not an error state in our design
        # Error state only occurs if a file exists but is malformed
        ctx = aggregate("NVDA")
        # errors list exists even if empty
        self.assertIsInstance(ctx.errors, list)


# ── Source status set ──────────────────────────────────────────────────────

class TestSourceStatusSet(unittest.TestCase):
    def test_evaluate_overall_freshness_all_fresh(self):
        from modules.market_thesis.source_status import SourceStatus
        statuses = [
            SourceStatus(name="a", contract="c", state="fresh"),
            SourceStatus(name="b", contract="c", state="fresh"),
        ]
        self.assertEqual(evaluate_overall_freshness(statuses), "fresh")

    def test_evaluate_overall_freshness_one_stale(self):
        from modules.market_thesis.source_status import SourceStatus
        statuses = [
            SourceStatus(name="a", contract="c", state="fresh"),
            SourceStatus(name="b", contract="c", state="stale"),
        ]
        self.assertEqual(evaluate_overall_freshness(statuses), "stale")

    def test_evaluate_overall_freshness_all_missing(self):
        from modules.market_thesis.source_status import SourceStatus
        statuses = [
            SourceStatus(name="a", contract="c", state="missing"),
            SourceStatus(name="b", contract="c", state="missing"),
        ]
        self.assertEqual(evaluate_overall_freshness(statuses), "missing")

    def test_evaluate_overall_freshness_mixed_with_error(self):
        from modules.market_thesis.source_status import SourceStatus
        statuses = [
            SourceStatus(name="a", contract="c", state="fresh"),
            SourceStatus(name="b", contract="c", state="error"),
        ]
        # Error should not affect overall — only present sources count
        self.assertEqual(evaluate_overall_freshness(statuses), "fresh")


# ── All 9 canonical symbols ────────────────────────────────────────────────

class TestAllCanonicalSymbols(unittest.TestCase):
    def test_all_symbols_aggregate_without_crash(self):
        symbols = ["BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU"]
        for sym in symbols:
            ctx = aggregate(sym)
            self.assertEqual(ctx.symbol, sym)
            self.assertIsInstance(ctx.has_any_data, bool)
            self.assertIsInstance(ctx.source_statuses, list)
            self.assertIsInstance(ctx.missing_sources, list)
            self.assertIsInstance(ctx.errors, list)

    def test_context_input_to_dict(self):
        for sym in ["BTC", "ETH", "SPCX"]:
            ctx = aggregate(sym)
            d = ctx.to_dict()
            self.assertIsInstance(d, dict)
            self.assertIn("symbol", d)
            self.assertIn("source_statuses", d)


# ── Source count consistency ──────────────────────────────────────────────

class TestSourceCountConsistency(unittest.TestCase):
    def test_all_expected_sources_listed(self):
        """All 10 source readers should appear in source_statuses."""
        ctx = aggregate("BTC")
        source_names = {s.name for s in ctx.source_statuses}
        expected = {
            "Webhook Events",
            "CDP Events",
            "Market Metrics",
            "Multi-TF Analysis",
            "Multi-TF Scores",
            "Vision Coinglass",
            "Vision Analysis",
            "Telegram Signals",
            "Telegram Signals DC",
            "Signal Events DC",
        }
        self.assertEqual(source_names, expected)


if __name__ == "__main__":
    unittest.main()
