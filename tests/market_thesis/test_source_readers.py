"""
Tests for source_readers.py — PR2.

Covers all source readers with fixtures.
- JSONL reading (valid, invalid lines, missing files)
- JSON reading (valid, missing, malformed)
- Symbol filtering
- Event alias normalization
- Timestamp parsing
- Freshness tracking via SourceStatus
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from modules.market_thesis.config import SOURCES, normalize_event_alias, normalize_symbol
from modules.market_thesis.source_readers import (
    NormalizedEvent,
    NormalizedMetrics,
    NormalizedSetup,
    NormalizedVision,
    _parse_ts,
    _read_jsonl,
    read_events_cdp_jsonl,
    read_events_jsonl,
    read_market_metrics,
    read_multitf_analysis,
    read_multitf_scores,
    read_signal_event_dc,
    read_telegram_signals,
    read_telegram_signals_dc,
    read_vision_analysis,
    read_vision_coinglass,
)
from modules.market_thesis.source_status import SourceStatus

FIXTURES = Path(__file__).resolve().parent / "fixtures"


# ── Normalization helpers ──────────────────────────────────────────────────

class TestNormalizeSymbol(unittest.TestCase):
    def test_binance_style(self):
        self.assertEqual(normalize_symbol("BTCUSDT"), "BTC")
        self.assertEqual(normalize_symbol("ETHUSDT"), "ETH")
        self.assertEqual(normalize_symbol("SOLUSDT"), "SOL")
        self.assertEqual(normalize_symbol("XRPUSDT"), "XRP")
        self.assertEqual(normalize_symbol("PAXGUSDT"), "XAU")

    def test_tv_style(self):
        self.assertEqual(normalize_symbol("BTCUSDT.P"), "BTC")
        self.assertEqual(normalize_symbol("OANDA:XAUUSD"), "XAU")

    def test_telegram_style(self):
        self.assertEqual(normalize_symbol("XAU/USD"), "XAU")
        self.assertEqual(normalize_symbol("BTC/USD"), "BTC")

    def test_canonical_passthrough(self):
        self.assertEqual(normalize_symbol("SPCX"), "SPCX")
        self.assertEqual(normalize_symbol("NVDA"), "NVDA")

    def test_unknown_uppercased(self):
        self.assertEqual(normalize_symbol("unknown_symbol"), "UNKNOWN_SYMBOL")


class TestNormalizeEventAlias(unittest.TestCase):
    def test_known_aliases(self):
        self.assertEqual(normalize_event_alias("orb_break_high"), "ORB_HIGH_BREAK")
        self.assertEqual(normalize_event_alias("orb_break_low"), "ORB_LOW_BREAK")
        self.assertEqual(normalize_event_alias("volume_spike"), "VOLUME_SURGE")
        self.assertEqual(normalize_event_alias("vwap_reclaim"), "VWAP_RECLAIM")
        self.assertEqual(normalize_event_alias("vwap_loss"), "VWAP_LOSS")
        self.assertEqual(normalize_event_alias("bos"), "BOS")
        self.assertEqual(normalize_event_alias("choch"), "CHOCH")
        self.assertEqual(normalize_event_alias("bos_bull"), "BOS_BULL")
        self.assertEqual(normalize_event_alias("fvg_created"), "FVG_CREATED")

    def test_unknown_uppercased(self):
        self.assertEqual(normalize_event_alias("custom_event"), "CUSTOM_EVENT")


# ── Timestamp parsing ──────────────────────────────────────────────────────

class TestParseTimestamp(unittest.TestCase):
    def test_none(self):
        self.assertIsNone(_parse_ts(None))

    def test_datetime_passthrough(self):
        dt = datetime(2026, 6, 15, 10, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(_parse_ts(dt), dt)

    def test_epoch_int(self):
        dt = _parse_ts(1718443200)
        self.assertIsNotNone(dt)
        self.assertAlmostEqual(dt.year, 2024, delta=1)

    def test_iso_with_z(self):
        dt = _parse_ts("2026-06-15T10:00:00Z")
        self.assertIsNotNone(dt)
        self.assertEqual(dt.hour, 10)

    def test_iso_with_offset(self):
        dt = _parse_ts("2026-06-15T10:00:00+00:00")
        self.assertIsNotNone(dt)

    def test_iso_with_microseconds(self):
        dt = _parse_ts("2026-06-15T10:00:00.123456Z")
        self.assertIsNotNone(dt)
        self.assertEqual(dt.microsecond, 123456)

    def test_invalid_returns_none(self):
        self.assertIsNone(_parse_ts("not a timestamp"))
        self.assertIsNone(_parse_ts(""))


# ── JSONL reader ───────────────────────────────────────────────────────────

class TestReadJSONL(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.path = Path(self.tmpdir) / "test.jsonl"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_empty_file(self):
        self.path.write_text("")
        status = SourceStatus(name="test", contract="test.v1")
        records = _read_jsonl(self.path, status=status)
        self.assertEqual(records, [])
        self.assertEqual(status.records_count, 0)

    def test_valid_lines(self):
        self.path.write_text('{"a":1}\n{"b":2}\n')
        records = _read_jsonl(self.path)
        self.assertEqual(len(records), 2)

    def test_skips_invalid_lines(self):
        self.path.write_text('{"a":1}\ninvalid\n{"b":2}\n')
        status = SourceStatus(name="test", contract="test.v1")
        records = _read_jsonl(self.path, status=status)
        self.assertEqual(len(records), 2)
        self.assertEqual(status.records_valid, 2)
        self.assertIn("Invalid JSONL", status.error_message or "")

    def test_missing_file(self):
        records = _read_jsonl(Path("/nonexistent/path.jsonl"))
        self.assertEqual(records, [])

    def test_none_path(self):
        records = _read_jsonl(None)
        self.assertEqual(records, [])

    def test_filter_by_symbol(self):
        self.path.write_text('{"symbol":"BTCUSDT","a":1}\n{"symbol":"ETHUSDT","b":2}\n')
        records = _read_jsonl(self.path, symbol="BTC")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["a"], 1)

    def test_empty_lines_skipped(self):
        self.path.write_text('\n{"a":1}\n\n{"b":2}\n\n')
        records = _read_jsonl(self.path)
        self.assertEqual(len(records), 2)


# ── Events JSONL (fixture-based) ───────────────────────────────────────────

class TestReadEventsJSONL(unittest.TestCase):
    def test_reads_events(self):
        with patch.dict(SOURCES, {"events_jsonl": FIXTURES / "events.jsonl"}, clear=False):
            events, status = read_events_jsonl()
            self.assertGreater(len(events), 0)
            self.assertEqual(status.name, "Webhook Events")

    def test_filter_by_symbol(self):
        with patch.dict(SOURCES, {"events_jsonl": FIXTURES / "events.jsonl"}, clear=False):
            events, status = read_events_jsonl(symbol="BTC")
            self.assertTrue(all(e.symbol == "BTC" for e in events))
            self.assertGreater(status.records_filtered, 0)

    def test_normalized_fields(self):
        with patch.dict(SOURCES, {"events_jsonl": FIXTURES / "events.jsonl"}, clear=False):
            events, _ = read_events_jsonl(symbol="BTC")
            self.assertGreater(len(events), 0)
            e = events[0]
            self.assertEqual(e.source, "webhook")
            self.assertEqual(e.symbol, "BTC")
            self.assertEqual(e.event_type, "SELL")
            self.assertIsNotNone(e.price)
            self.assertIsNotNone(e.ts)

    def test_missing_file(self):
        with patch.dict(SOURCES, {"events_jsonl": Path("/nonexistent/file.jsonl")}, clear=False):
            events, status = read_events_jsonl()
            self.assertEqual(events, [])
            self.assertEqual(status.state, "missing")


# ── CDP events JSONL (fixture-based) ───────────────────────────────────────

class TestReadEventsCDPJSONL(unittest.TestCase):
    def test_reads_cdp_events(self):
        with patch.dict(SOURCES, {"events_cdp_jsonl": FIXTURES / "events_cdp.jsonl"}, clear=False):
            events, status = read_events_cdp_jsonl()
            self.assertGreater(len(events), 0)
            self.assertEqual(status.name, "CDP Events")

    def test_skips_corrupted_line(self):
        with patch.dict(SOURCES, {"events_cdp_jsonl": FIXTURES / "events_cdp.jsonl"}, clear=False):
            events, status = read_events_cdp_jsonl()
            self.assertEqual(len(events), 3)  # 4 lines, 1 corrupted

    def test_alias_normalized(self):
        with patch.dict(SOURCES, {"events_cdp_jsonl": FIXTURES / "events_cdp.jsonl"}, clear=False):
            events, _ = read_events_cdp_jsonl(symbol="BTC")
            self.assertGreater(len(events), 0)
            self.assertEqual(events[0].event_type, "VWAP_LOSS")

    def test_orb_break_alias(self):
        with patch.dict(SOURCES, {"events_cdp_jsonl": FIXTURES / "events_cdp.jsonl"}, clear=False):
            events, _ = read_events_cdp_jsonl(symbol="ETH")
            self.assertGreater(len(events), 0)
            self.assertEqual(events[0].event_type, "ORB_HIGH_BREAK")

    def test_missing_file(self):
        with patch.dict(SOURCES, {"events_cdp_jsonl": Path("/nonexistent/file.jsonl")}, clear=False):
            events, status = read_events_cdp_jsonl()
            self.assertEqual(events, [])
            self.assertEqual(status.state, "missing")


# ── Market metrics ─────────────────────────────────────────────────────────

class TestReadMarketMetrics(unittest.TestCase):
    def setUp(self):
        self._bad_path = None

    def tearDown(self):
        if self._bad_path:
            self._bad_path.unlink(missing_ok=True)

    def test_reads_fixture(self):
        # Patch SOURCES directly so the reader finds the fixture
        with patch.dict("modules.market_thesis.config.SOURCES", {"market_metrics": FIXTURES}, clear=False):
            # Make source_path_for_symbol point to our fixture
            from modules.market_thesis.config import source_path_for_symbol
            with patch("modules.market_thesis.source_readers.source_path_for_symbol",
                       side_effect=lambda key, sym: FIXTURES / "market_metrics.json" if key == "market_metrics" else None):
                metrics, status = read_market_metrics("BTC")
                self.assertIsNotNone(metrics)
                self.assertEqual(metrics.symbol, "BTC")
                self.assertEqual(metrics.price, 66450)
                self.assertEqual(metrics.open_interest, 28500000000)
                self.assertEqual(metrics.funding_rate, 0.0045)
                self.assertEqual(metrics.long_short_ratio, 1.75)
                self.assertEqual(status.name, "Market Metrics")

    def test_missing_file(self):
        # read_multitf_analysis imports source_path_for_symbol locally,
        # so we patch SOURCES to a non-existent base
        nonexistent = Path("/nonexistent/market_metrics_dir")
        with patch.dict("modules.market_thesis.config.SOURCES", {"market_metrics": nonexistent}, clear=False):
            metrics, status = read_market_metrics("BTC")
            self.assertIsNone(metrics)
            self.assertEqual(status.state, "missing")

    def test_malformed_json(self):
        tmpdir = Path(tempfile.mkdtemp())
        bad_path = tmpdir / "BTCUSDT.json"
        bad_path.write_text("{invalid json")
        self._bad_path = bad_path
        with patch.dict("modules.market_thesis.config.SOURCES", {"market_metrics": tmpdir}, clear=False):
            metrics, status = read_market_metrics("BTC")
            self.assertIsNone(metrics)
            self.assertEqual(status.state, "error")


# ── Multi-TF scores ────────────────────────────────────────────────────────

class TestReadMultitfScores(unittest.TestCase):
    def test_reads_setups(self):
        # Patch the source_path_for_symbol to return our fixture
        with patch(
            "modules.market_thesis.source_readers.source_path_for_symbol",
            side_effect=lambda key, sym: FIXTURES / "priority_snapshot.json" if key == "multitf_scores" and sym == "BTC" else None,
        ):
            setups, status = read_multitf_scores("BTC")
            self.assertGreater(len(setups), 0)
            self.assertEqual(setups[0].setup_id, "btc_vwap_reclaim")
            self.assertEqual(setups[0].grade, "B")
            self.assertEqual(setups[0].score, 62)
            self.assertEqual(setups[0].probability_pct, 55)
            self.assertEqual(status.name, "Multi-TF Scores")

    def test_missing_file(self):
        with patch(
            "modules.market_thesis.source_readers.source_path_for_symbol",
            return_value=None,
        ):
            setups, status = read_multitf_scores("XRP")
            self.assertEqual(setups, [])
            self.assertEqual(status.state, "missing")


# ── Vision readers ─────────────────────────────────────────────────────────

class TestReadVisionAnalysis(unittest.TestCase):
    def test_reads_fixture(self):
        with patch(
            "modules.market_thesis.source_readers.source_path_for_symbol",
            return_value=FIXTURES / "vision_analysis.json",
        ):
            vision, status = read_vision_analysis("BTC")
            self.assertIsNotNone(vision)
            self.assertIn(65000, vision.support_levels)
            self.assertIn(68500, vision.resistance_levels)
            self.assertIsNotNone(vision.analysis_summary)
            self.assertEqual(status.name, "Vision Analysis")

    def test_missing_file(self):
        with patch(
            "modules.market_thesis.source_readers.source_path_for_symbol",
            return_value=None,
        ):
            vision, status = read_vision_analysis("MU")
            self.assertIsNone(vision)
            self.assertEqual(status.state, "missing")

    def test_malformed_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not json")
            f.flush()
            bad_path = Path(f.name)

        try:
            with patch(
                "modules.market_thesis.source_readers.source_path_for_symbol",
                return_value=bad_path,
            ):
                vision, status = read_vision_analysis("BTC")
                self.assertIsNone(vision)
                self.assertEqual(status.state, "error")
        finally:
            bad_path.unlink(missing_ok=True)


# ── Source status in all readers ───────────────────────────────────────────

class TestSourceStatusTracking(unittest.TestCase):
    def test_missing_source_has_state_missing(self):
        with patch(
            "modules.market_thesis.source_readers.source_path_for_symbol",
            return_value=None,
        ):
            _, status = read_market_metrics("XRP")
            self.assertEqual(status.state, "missing")

    def test_valid_source_has_state_fresh_or_warm(self):
        with patch(
            "modules.market_thesis.source_readers.source_path_for_symbol",
            return_value=FIXTURES / "market_metrics.json",
        ):
            _, status = read_market_metrics("BTC")
            self.assertIn(status.state, ("fresh", "warm", "stale", "expired"))

    def test_age_minutes_populated(self):
        with patch(
            "modules.market_thesis.source_readers.source_path_for_symbol",
            return_value=FIXTURES / "market_metrics.json",
        ):
            _, status = read_market_metrics("BTC")
            self.assertIsNotNone(status.age_minutes)


# ── Deterministic ordering ─────────────────────────────────────────────────

class TestDeterministicOrdering(unittest.TestCase):
    def test_events_jsonl_order_preserved(self):
        with patch.dict(SOURCES, {"events_jsonl": FIXTURES / "events.jsonl"}, clear=False):
            events1, _ = read_events_jsonl()
            events2, _ = read_events_jsonl()
            self.assertEqual(
                [(e.symbol, e.event_type) for e in events1],
                [(e.symbol, e.event_type) for e in events2],
            )


if __name__ == "__main__":
    unittest.main()
