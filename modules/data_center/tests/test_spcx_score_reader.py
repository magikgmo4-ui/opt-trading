from __future__ import annotations

"""Unit tests for the SPCX score reader (spcx_score_reader.py).

Tests the full chain:
    events_cdp.jsonl + events.jsonl  ->  read_spcx_score()  ->  score_spcx()

No live file I/O -- all tests use temp files written in setUp.
No FastAPI app needed -- tests call read_spcx_score() directly.

Weights (2026-06-16): VWAP_RECLAIM=25, ORB_HIGH_BREAK=25, BREAK_174=20,
    VOLUME_SURGE=15, PREMARKET_HIGH_BREAK=15, SPACEX_WIRE=5, BOT_VISION_CONF=5.

Score now includes dynamic opening session boost (Phase 3):
    - vwap_acceptance (+10) for VWAP_RECLAIM
    - momentum_continuation (+10) for ORB_HIGH_BREAK
    - premarket_acceptance (+10) for PREMARKET_HIGH_BREAK
    - continuation_score >= 60 triggers strong_continuation (+5)
    - Score cap at 120 with boost enabled
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from modules.desk_pro.service.spcx_score_reader import read_spcx_score

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

def _cdp_event(event: str, price: float = 173.77, symbol: str = "SPCX", **flags) -> dict:
    """Build a minimal events_cdp.jsonl row."""
    return {
        "_schema": "signal_event.v1",
        "source": "tradingview",
        "symbol": symbol,
        "timeframe": "15m",
        "event": event,
        "price": price,
        "volume": None,
        "flags": flags or {},
        "_ts": "2026-06-12T17:30:00Z",
        "_ip": "127.0.0.1",
    }


def _wire_event(signal: str, symbol: str = "SPCX", price: float = 173.77) -> dict:
    """Build a minimal events.jsonl row (main webhook)."""
    return {
        "key": None,
        "engine": "TV_TEST",
        "signal": signal,
        "symbol": symbol,
        "tf": "15m",
        "price": price,
        "_ts": "2026-06-12T17:30:00Z",
        "_ip": "127.0.0.1",
    }


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


# ---------------------------------------------------------------------------
# 1. No-data / empty file cases
# ---------------------------------------------------------------------------

class TestNoData(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_missing_both_files_returns_zero_score(self):
        result = read_spcx_score(
            cdp_path=self.tmp / "nonexistent_cdp.jsonl",
            events_path=self.tmp / "nonexistent_events.jsonl",
        )
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["grade"], "C")
        self.assertEqual(result["setup_state"], "watch")
        self.assertTrue(result["monitor_only"])

    def test_empty_files_return_zero_score(self):
        cdp = self.tmp / "events_cdp.jsonl"
        ev = self.tmp / "events.jsonl"
        cdp.write_text("", encoding="utf-8")
        ev.write_text("", encoding="utf-8")
        result = read_spcx_score(cdp_path=cdp, events_path=ev)
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["data_source"]["cdp_events"], 0)
        self.assertEqual(result["data_source"]["wire_events"], 0)

    def test_malformed_json_lines_skipped(self):
        cdp = self.tmp / "events_cdp.jsonl"
        cdp.write_text("{bad json\n{also bad\n", encoding="utf-8")
        result = read_spcx_score(cdp_path=cdp, events_path=self.tmp / "nope.jsonl")
        self.assertEqual(result["score"], 0)

    def test_output_structure_complete_on_empty(self):
        result = read_spcx_score(
            cdp_path=self.tmp / "a.jsonl",
            events_path=self.tmp / "b.jsonl",
        )
        for key in ("symbol", "score", "grade", "events", "bias",
                    "setup_state", "levels", "risk_notes", "invalidation",
                    "monitor_only", "data_source"):
            self.assertIn(key, result, f"missing key: {key}")


# ---------------------------------------------------------------------------
# 2. CDP events (events_cdp.jsonl)
# ---------------------------------------------------------------------------

class TestCdpEvents(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.cdp = self.tmp / "events_cdp.jsonl"
        self.ev = self.tmp / "events.jsonl"
        self.ev.write_text("", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_vwap_reclaim_cdp_scores_25(self):
        _write_jsonl(self.cdp, [_cdp_event("vwap_reclaim")])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        # VWAP_RECLAIM(25) + vwap_acceptance boost(+10) = 35
        self.assertEqual(result["score"], 35)
        self.assertIn("VWAP_RECLAIM", result["events"])

    def test_orb_break_high_alias_to_orb_high_break(self):
        """CDP stores 'orb_break_high' -> scorer expects 'ORB_HIGH_BREAK'."""
        _write_jsonl(self.cdp, [_cdp_event("orb_break_high")])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        # ORB_HIGH_BREAK(25) + momentum_continuation(+10) = 35
        self.assertEqual(result["score"], 35)
        self.assertIn("ORB_HIGH_BREAK", result["events"])

    def test_volume_spike_alias_to_volume_surge(self):
        _write_jsonl(self.cdp, [_cdp_event("volume_spike")])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        self.assertIn("VOLUME_SURGE", result["events"])
        self.assertEqual(result["score"], 15)

    def test_premarket_high_break_alias_to_premarket_high_break(self):
        _write_jsonl(self.cdp, [_cdp_event("premarket_high_break")])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        self.assertIn("PREMARKET_HIGH_BREAK", result["events"])
        # PREMARKET_HIGH_BREAK(15) + premarket_acceptance boost(+10) = 25
        self.assertEqual(result["score"], 25)

    def test_non_spcx_cdp_events_ignored(self):
        _write_jsonl(self.cdp, [
            _cdp_event("vwap_reclaim", symbol="BTCUSD"),
            _cdp_event("orb_break_high", symbol="ETH"),
        ])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["data_source"]["cdp_events"], 0)

    def test_unknown_cdp_event_scores_zero(self):
        _write_jsonl(self.cdp, [_cdp_event("fvg_created")])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        self.assertEqual(result["score"], 0)

    def test_enrichment_from_flags(self):
        _write_jsonl(self.cdp, [
            _cdp_event("vwap_reclaim", vwap=164.74, orb_high=168.75, bias="bullish")
        ])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        self.assertAlmostEqual(result["levels"]["vwap"], 164.74)
        self.assertAlmostEqual(result["levels"]["orb_high"], 168.75)
        self.assertEqual(result["bias"], "bullish")

    def test_non_signal_event_v1_schema_skipped(self):
        row = _cdp_event("vwap_reclaim")
        row["_schema"] = "market_metrics.v1"
        _write_jsonl(self.cdp, [row])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        self.assertEqual(result["score"], 0)


# ---------------------------------------------------------------------------
# 3. SPACEX_WIRE from main events.jsonl
# ---------------------------------------------------------------------------

class TestWireEvents(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.cdp = self.tmp / "events_cdp.jsonl"
        self.ev = self.tmp / "events.jsonl"
        self.cdp.write_text("", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_spacex_wire_signal_scores_5(self):
        _write_jsonl(self.ev, [_wire_event("SPACEX_WIRE")])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        self.assertEqual(result["score"], 5)
        self.assertIn("SPACEX_WIRE", result["events"])
        self.assertEqual(result["data_source"]["wire_events"], 1)

    def test_non_spacex_wire_signals_ignored(self):
        _write_jsonl(self.ev, [_wire_event("BUY"), _wire_event("SELL")])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["data_source"]["wire_events"], 0)

    def test_non_spcx_wire_events_ignored(self):
        _write_jsonl(self.ev, [_wire_event("SPACEX_WIRE", symbol="BTCUSD")])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        self.assertEqual(result["score"], 0)


# ---------------------------------------------------------------------------
# 4. Combined sources -- acceptance scenario
# ---------------------------------------------------------------------------

class TestCombinedSources(unittest.TestCase):
    """3 signals (VWAP_RECLAIM+ORB_HIGH_BREAK+SPACEX_WIRE) -> score=55, grade=B, active."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.cdp = self.tmp / "events_cdp.jsonl"
        self.ev = self.tmp / "events.jsonl"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_full_scenario_score_80_grade_aplus_active(self):
        # VWAP_RECLAIM(25) + ORB_HIGH_BREAK(25) + SPACEX_WIRE(5) = 55
        # + vwap_acceptance(10) + momentum_continuation(10) + strong_continuation(5) = 80 -> A+
        _write_jsonl(self.cdp, [
            _cdp_event("vwap_reclaim",  price=173.77, vwap=164.74),
            _cdp_event("orb_break_high", price=173.77, vwap=164.74, orb_high=168.75),
        ])
        _write_jsonl(self.ev, [_wire_event("SPACEX_WIRE", price=173.77)])

        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)

        self.assertEqual(result["score"], 80)
        self.assertEqual(result["grade"], "A+")
        self.assertEqual(result["setup_state"], "active")
        self.assertIn("extended_above_vwap", result["risk_notes"])
        self.assertTrue(result["monitor_only"])
        self.assertEqual(result["data_source"]["cdp_events"], 2)
        self.assertEqual(result["data_source"]["wire_events"], 1)
        self.assertEqual(result["data_source"]["total_input_events"], 3)

    def test_cdp_and_wire_dedup_same_type(self):
        """Same event type from CDP twice + wire -> deduplicated per type."""
        _write_jsonl(self.cdp, [
            _cdp_event("vwap_reclaim"),
            _cdp_event("vwap_reclaim"),  # duplicate
        ])
        _write_jsonl(self.ev, [_wire_event("SPACEX_WIRE")])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        # VWAP_RECLAIM(25) + SPACEX_WIRE(5) = 30
        # + vwap_acceptance boost(10) = 40
        self.assertEqual(result["score"], 40)

    def test_mixed_symbols_only_spcx_counted(self):
        _write_jsonl(self.cdp, [
            _cdp_event("vwap_reclaim", symbol="SPCX"),
            _cdp_event("orb_break_high", symbol="NVDA"),
        ])
        _write_jsonl(self.ev, [
            _wire_event("SPACEX_WIRE", symbol="SPCX"),
            _wire_event("SPACEX_WIRE", symbol="TSLA"),
        ])
        result = read_spcx_score(cdp_path=self.cdp, events_path=self.ev)
        # Only SPCX: VWAP_RECLAIM(25) + SPACEX_WIRE(5) = 30
        # + vwap_acceptance boost(10) = 40
        self.assertEqual(result["score"], 40)


# ---------------------------------------------------------------------------
# 5. data_source metadata
# ---------------------------------------------------------------------------

class TestDataSourceMetadata(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_data_source_keys_present(self):
        result = read_spcx_score(
            cdp_path=self.tmp / "a.jsonl",
            events_path=self.tmp / "b.jsonl",
        )
        ds = result["data_source"]
        self.assertIn("cdp_events", ds)
        self.assertIn("wire_events", ds)
        self.assertIn("total_input_events", ds)

    def test_total_is_sum_of_parts(self):
        cdp = self.tmp / "events_cdp.jsonl"
        ev = self.tmp / "events.jsonl"
        _write_jsonl(cdp, [_cdp_event("vwap_reclaim")])
        _write_jsonl(ev, [_wire_event("SPACEX_WIRE")])
        result = read_spcx_score(cdp_path=cdp, events_path=ev)
        ds = result["data_source"]
        self.assertEqual(ds["total_input_events"], ds["cdp_events"] + ds["wire_events"])


if __name__ == "__main__":
    unittest.main()
