from __future__ import annotations

"""Unit tests for the SPCX composite score scorer.

Fixtures mirror real TradingView CDP alerts captured 2026-06-12:
    - VWAP_RECLAIM  at price 173.77, vwap 164.74
    - ORB_HIGH_BREAK at price 173.77, orb_high 168.75
    - SPACEX_WIRE

Weights (updated 2026-06-15): VWAP_RECLAIM=25, ORB_HIGH_BREAK=25, BREAK_174=20,
    VOLUME_SURGE=15, PREMARKET_GAP=10, SPACEX_WIRE=5, BOT_VISION_CONF=5.
Three baseline alerts -> score=55, grade=B, setup_state=active.
"""

import unittest

from modules.data_center.spcx_composite_score import score_spcx

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_VWAP_RECLAIM = {
    "source": "tradingview",
    "symbol": "SPCX",
    "event": "VWAP_RECLAIM",
    "bias": "bullish",
    "price": "173.77",
    "vwap": "164.74",
    "timeframe": "15m",
}

_ORB_HIGH_BREAK = {
    "source": "tradingview",
    "symbol": "SPCX",
    "event": "ORB_HIGH_BREAK",
    "bias": "bullish",
    "price": "173.77",
    "vwap": "164.74",
    "orb_high": "168.75",
    "timeframe": "15m",
}

_SPACEX_WIRE = {
    "source": "tradingview",
    "symbol": "SPCX",
    "event": "SPACEX_WIRE",
    "timeframe": "15m",
}


# ---------------------------------------------------------------------------
# 1. Core acceptance tests (real alert fixtures)
# ---------------------------------------------------------------------------

class TestAcceptanceCriteria(unittest.TestCase):
    """Three baseline signals: VWAP_RECLAIM + ORB_HIGH_BREAK + SPACEX_WIRE = 55, grade B."""

    def setUp(self):
        self.result = score_spcx([_VWAP_RECLAIM, _ORB_HIGH_BREAK, _SPACEX_WIRE])

    def test_score_is_55(self):
        # VWAP_RECLAIM(25) + ORB_HIGH_BREAK(25) + SPACEX_WIRE(5) = 55
        self.assertEqual(self.result["score"], 55)

    def test_grade_is_B(self):
        self.assertEqual(self.result["grade"], "B")

    def test_setup_state_is_active(self):
        self.assertEqual(self.result["setup_state"], "active")

    def test_risk_note_extended_above_vwap(self):
        self.assertIn("extended_above_vwap", self.result["risk_notes"])

    def test_monitor_only_is_true(self):
        self.assertTrue(self.result["monitor_only"])

    def test_symbol_is_SPCX(self):
        self.assertEqual(self.result["symbol"], "SPCX")

    def test_bias_is_bullish(self):
        self.assertEqual(self.result["bias"], "bullish")

    def test_events_contains_three_triggers(self):
        self.assertIn("VWAP_RECLAIM", self.result["events"])
        self.assertIn("ORB_HIGH_BREAK", self.result["events"])
        self.assertIn("SPACEX_WIRE", self.result["events"])


# ---------------------------------------------------------------------------
# 2. Grade boundary tests
# ---------------------------------------------------------------------------

class TestGradeBoundaries(unittest.TestCase):
    def test_score_0_grade_C(self):
        self.assertEqual(score_spcx([])["grade"], "C")

    def test_score_30_grade_C(self):
        # VWAP_RECLAIM(25) + SPACEX_WIRE(5) = 30 -> C
        result = score_spcx([_VWAP_RECLAIM, _SPACEX_WIRE])
        self.assertEqual(result["score"], 30)
        self.assertEqual(result["grade"], "C")

    def test_score_25_grade_C(self):
        result = score_spcx([_VWAP_RECLAIM])
        self.assertEqual(result["score"], 25)
        self.assertEqual(result["grade"], "C")

    def test_score_50_grade_B(self):
        # VWAP_RECLAIM(25) + ORB_HIGH_BREAK(25) = 50 -> B
        result = score_spcx([_VWAP_RECLAIM, _ORB_HIGH_BREAK])
        self.assertEqual(result["score"], 50)
        self.assertEqual(result["grade"], "B")

    def test_score_55_grade_B(self):
        # VWAP_RECLAIM(25) + ORB_HIGH_BREAK(25) + SPACEX_WIRE(5) = 55 -> B
        result = score_spcx([_VWAP_RECLAIM, _ORB_HIGH_BREAK, _SPACEX_WIRE])
        self.assertEqual(result["score"], 55)
        self.assertEqual(result["grade"], "B")

    def test_all_events_grade_Aplus(self):
        # All bullish weights: 25+25+20+15+10+5+5 = 105 -> A+
        all_events = [
            {**_VWAP_RECLAIM, "event": "VWAP_RECLAIM"},
            {**_ORB_HIGH_BREAK, "event": "ORB_HIGH_BREAK"},
            {"symbol": "SPCX", "event": "BREAK_174"},
            {"symbol": "SPCX", "event": "VOLUME_SURGE"},
            {"symbol": "SPCX", "event": "PREMARKET_GAP"},
            {"symbol": "SPCX", "event": "SPACEX_WIRE"},
            {"symbol": "SPCX", "event": "BOT_VISION_CONF"},
        ]
        result = score_spcx(all_events)
        self.assertEqual(result["score"], 105)
        self.assertEqual(result["grade"], "A+")


# ---------------------------------------------------------------------------
# 3. Setup state tests
# ---------------------------------------------------------------------------

class TestSetupState(unittest.TestCase):
    def test_active_when_price_above_orb_and_vwap(self):
        result = score_spcx([_VWAP_RECLAIM, _ORB_HIGH_BREAK])
        self.assertEqual(result["setup_state"], "active")

    def test_invalidated_when_price_below_vwap_after_reclaim(self):
        below_vwap = {**_VWAP_RECLAIM, "price": "160.00"}
        result = score_spcx([below_vwap])
        self.assertEqual(result["setup_state"], "invalidated")

    def test_watch_when_only_spacex_wire(self):
        result = score_spcx([_SPACEX_WIRE])
        self.assertEqual(result["setup_state"], "watch")

    def test_watch_when_no_events(self):
        result = score_spcx([])
        self.assertEqual(result["setup_state"], "watch")

    def test_watch_when_orb_break_without_vwap_reclaim(self):
        result = score_spcx([_ORB_HIGH_BREAK])
        # ORB_HIGH_BREAK alone -> no VWAP_RECLAIM -> can't reach "active", falls back to watch
        self.assertEqual(result["setup_state"], "watch")

    def test_invalidation_overrides_when_price_dips_below_vwap(self):
        """Even with ORB_HIGH_BREAK, if price < vwap -> invalidated."""
        below = {**_ORB_HIGH_BREAK, "price": "160.00"}
        reclaim = {**_VWAP_RECLAIM, "price": "160.00"}
        result = score_spcx([reclaim, below])
        self.assertEqual(result["setup_state"], "invalidated")


# ---------------------------------------------------------------------------
# 4. Filtering and deduplication
# ---------------------------------------------------------------------------

class TestFilteringAndDedup(unittest.TestCase):
    def test_non_spcx_events_ignored(self):
        btc = {**_VWAP_RECLAIM, "symbol": "BTCUSDT"}
        result = score_spcx([btc, _SPACEX_WIRE])
        # Only SPACEX_WIRE counted (weight=5)
        self.assertEqual(result["score"], 5)

    def test_duplicate_event_type_counted_once(self):
        result = score_spcx([_VWAP_RECLAIM, dict(_VWAP_RECLAIM)])
        self.assertEqual(result["score"], 25)

    def test_empty_event_field_skipped(self):
        result = score_spcx([{"symbol": "SPCX", "event": ""}])
        self.assertEqual(result["score"], 0)

    def test_missing_symbol_skipped(self):
        result = score_spcx([{"event": "VWAP_RECLAIM"}])
        self.assertEqual(result["score"], 0)

    def test_lowercase_event_type_matches(self):
        lower = {**_VWAP_RECLAIM, "event": "vwap_reclaim"}
        result = score_spcx([lower])
        self.assertEqual(result["score"], 25)

    def test_lowercase_symbol_matches(self):
        lower = {**_VWAP_RECLAIM, "symbol": "spcx"}
        result = score_spcx([lower])
        self.assertEqual(result["score"], 25)


# ---------------------------------------------------------------------------
# 5. Levels extraction
# ---------------------------------------------------------------------------

class TestLevels(unittest.TestCase):
    def test_levels_extracted_from_orb_event(self):
        result = score_spcx([_ORB_HIGH_BREAK])
        lvl = result["levels"]
        self.assertAlmostEqual(lvl["price"], 173.77)
        self.assertAlmostEqual(lvl["vwap"], 164.74)
        self.assertAlmostEqual(lvl["orb_high"], 168.75)

    def test_levels_none_when_absent(self):
        result = score_spcx([_SPACEX_WIRE])
        lvl = result["levels"]
        self.assertIsNone(lvl["price"])
        self.assertIsNone(lvl["vwap"])
        self.assertIsNone(lvl["orb_high"])
        self.assertIsNone(lvl["orb_low"])

    def test_numeric_price_accepted(self):
        e = {**_VWAP_RECLAIM, "price": 173.77}
        result = score_spcx([e])
        self.assertAlmostEqual(result["levels"]["price"], 173.77)


# ---------------------------------------------------------------------------
# 6. Risk notes
# ---------------------------------------------------------------------------

class TestRiskNotes(unittest.TestCase):
    def test_extended_above_vwap_when_5pct_above(self):
        # 173.77 vs 164.74 -> +5.48%
        result = score_spcx([_VWAP_RECLAIM])
        self.assertIn("extended_above_vwap", result["risk_notes"])

    def test_no_risk_note_when_close_to_vwap(self):
        at_vwap = {**_VWAP_RECLAIM, "price": "165.00", "vwap": "164.74"}
        result = score_spcx([at_vwap])
        self.assertNotIn("extended_above_vwap", result["risk_notes"])

    def test_extended_below_vwap_when_5pct_below(self):
        below = {**_VWAP_RECLAIM, "price": "155.00", "vwap": "164.74"}
        result = score_spcx([below])
        self.assertIn("extended_below_vwap", result["risk_notes"])

    def test_no_risk_note_when_no_price(self):
        result = score_spcx([_SPACEX_WIRE])
        self.assertEqual(result["risk_notes"], [])


# ---------------------------------------------------------------------------
# 7. Invalidation dict
# ---------------------------------------------------------------------------

class TestInvalidation(unittest.TestCase):
    def test_vwap_loss_level_set_when_reclaim_triggered(self):
        result = score_spcx([_VWAP_RECLAIM])
        self.assertIn("vwap_loss", result["invalidation"])
        self.assertAlmostEqual(result["invalidation"]["vwap_loss"]["level"], 164.74)

    def test_orb_loss_level_set_when_orb_break_triggered(self):
        result = score_spcx([_ORB_HIGH_BREAK])
        self.assertIn("orb_loss", result["invalidation"])
        self.assertAlmostEqual(result["invalidation"]["orb_loss"]["level"], 168.75)

    def test_invalidation_empty_when_no_signals(self):
        result = score_spcx([])
        self.assertEqual(result["invalidation"], {})

    def test_invalidation_empty_when_only_spacex_wire(self):
        result = score_spcx([_SPACEX_WIRE])
        self.assertEqual(result["invalidation"], {})


# ---------------------------------------------------------------------------
# 8. Bias
# ---------------------------------------------------------------------------

class TestBias(unittest.TestCase):
    def test_bullish_when_all_events_bullish(self):
        result = score_spcx([_VWAP_RECLAIM, _ORB_HIGH_BREAK])
        self.assertEqual(result["bias"], "bullish")

    def test_neutral_when_no_bias_field(self):
        result = score_spcx([_SPACEX_WIRE])
        self.assertEqual(result["bias"], "neutral")

    def test_mixed_when_conflicting_bias(self):
        bullish = {**_VWAP_RECLAIM, "event": "VWAP_RECLAIM", "bias": "bullish"}
        bearish = {**_SPACEX_WIRE, "event": "SPACEX_WIRE", "bias": "bearish"}
        result = score_spcx([bullish, bearish])
        self.assertEqual(result["bias"], "mixed")


# ---------------------------------------------------------------------------
# 9. Output structure contract
# ---------------------------------------------------------------------------

class TestOutputStructure(unittest.TestCase):
    _REQUIRED_KEYS = {
        "symbol", "score", "grade", "events", "bias",
        "setup_state", "levels", "risk_notes", "invalidation", "monitor_only",
    }
    _REQUIRED_LEVEL_KEYS = {"price", "vwap", "orb_high", "orb_low"}

    def _check(self, result: dict) -> None:
        self.assertEqual(result.keys(), self._REQUIRED_KEYS)
        self.assertEqual(set(result["levels"].keys()), self._REQUIRED_LEVEL_KEYS)
        self.assertIsInstance(result["score"], int)
        self.assertIsInstance(result["events"], list)
        self.assertIsInstance(result["risk_notes"], list)
        self.assertIsInstance(result["invalidation"], dict)
        self.assertTrue(result["monitor_only"])

    def test_structure_empty_input(self):
        self._check(score_spcx([]))

    def test_structure_single_event(self):
        self._check(score_spcx([_VWAP_RECLAIM]))

    def test_structure_full_fixture(self):
        self._check(score_spcx([_VWAP_RECLAIM, _ORB_HIGH_BREAK, _SPACEX_WIRE]))


if __name__ == "__main__":
    unittest.main()
