from __future__ import annotations

"""Unit tests for opening session metrics computation.

Tests compute_opening_metrics() and its integration with score_spcx().
"""

import unittest

from modules.data_center.opening_session_metrics import compute_opening_metrics
from modules.data_center.spcx_composite_score import score_spcx


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _event(event: str, price: float = 173.77, **extra) -> dict:
    flags = dict(extra)
    result = {
        "source": "tradingview",
        "symbol": "SPCX",
        "event": event,
        "price": price,
        "flags": flags,
        "timeframe": "15m",
    }
    v = flags.get("vwap")
    if v is not None:
        result["vwap"] = v
    return result


# ---------------------------------------------------------------------------
# 1. Opening gap computation
# ---------------------------------------------------------------------------

class TestOpeningGap(unittest.TestCase):
    def test_gap_up_from_prev_close(self):
        e = _event("GAP_OPEN_UP", price=164.0, prev_close=160.0, open_price=164.0)
        m = compute_opening_metrics([e])
        self.assertAlmostEqual(m["opening_gap_pct"], 2.5)
        self.assertEqual(m["opening_drive"], "up")

    def test_gap_down_from_prev_close(self):
        e = _event("GAP_OPEN_DOWN", price=155.0, prev_close=160.0, open_price=155.0)
        m = compute_opening_metrics([e])
        self.assertAlmostEqual(m["opening_gap_pct"], -3.125)
        self.assertEqual(m["opening_drive"], "down")

    def test_no_gap_when_no_prev_close(self):
        e = _event("VWAP_RECLAIM", price=170.0)
        m = compute_opening_metrics([e])
        self.assertIsNone(m["opening_gap_pct"])
        self.assertIsNone(m["opening_drive"])

    def test_flat_gap(self):
        e = _event("VWAP_RECLAIM", price=160.0, prev_close=160.0)
        m = compute_opening_metrics([e])
        self.assertAlmostEqual(m["opening_gap_pct"], 0.0)
        self.assertEqual(m["opening_drive"], "flat")


# ---------------------------------------------------------------------------
# 2. Distance metrics
# ---------------------------------------------------------------------------

class TestDistances(unittest.TestCase):
    def test_distance_vwap_pct(self):
        e = _event("VWAP_RECLAIM", price=173.77, vwap=164.74)
        m = compute_opening_metrics([e])
        self.assertAlmostEqual(m["distance_vwap_pct"], 5.4833, places=2)

    def test_distance_vwap_none_when_no_vwap(self):
        e = _event("SPACEX_WIRE", price=173.77)
        m = compute_opening_metrics([e])
        self.assertIsNone(m["distance_vwap_pct"])

    def test_distance_orb_high_pct(self):
        e = _event("ORB_HIGH_BREAK", price=173.77, vwap=164.74,
                   orb_high=168.75)
        m = compute_opening_metrics([e])
        self.assertAlmostEqual(m["distance_orb_pct"], 2.9754, places=2)

    def test_distance_premarket_high_pct(self):
        e = _event("PREMARKET_HIGH_BREAK", price=173.77, vwap=164.74,
                   premarket_high=170.0)
        m = compute_opening_metrics([e])
        self.assertAlmostEqual(m["distance_premarket_high_pct"], 2.2176, places=2)


# ---------------------------------------------------------------------------
# 3. Risk score
# ---------------------------------------------------------------------------

class TestRiskScore(unittest.TestCase):
    def test_high_risk_from_extension(self):
        e = _event("VWAP_RECLAIM", price=180.0, vwap=164.74)
        m = compute_opening_metrics([e])
        self.assertGreaterEqual(m["risk_score"], 40)

    def test_low_risk_no_signals(self):
        m = compute_opening_metrics([])
        self.assertEqual(m["risk_score"], 0)

    def test_exhaustion_adds_risk(self):
        e = _event("OPENING_EXHAUSTION")
        m = compute_opening_metrics([e])
        self.assertGreaterEqual(m["risk_score"], 30)


# ---------------------------------------------------------------------------
# 4. Continuation score
# ---------------------------------------------------------------------------

class TestContinuationScore(unittest.TestCase):
    def test_vwap_and_orb_high_continuation(self):
        events = [
            _event("VWAP_RECLAIM"),
            _event("ORB_HIGH_BREAK"),
        ]
        m = compute_opening_metrics(events)
        self.assertGreaterEqual(m["continuation_score"], 50)

    def test_no_signals_zero_continuation(self):
        m = compute_opening_metrics([])
        self.assertEqual(m["continuation_score"], 0)

    def test_premarket_break_adds_continuation(self):
        e = _event("PREMARKET_HIGH_BREAK")
        m = compute_opening_metrics([e])
        self.assertGreaterEqual(m["continuation_score"], 20)


# ---------------------------------------------------------------------------
# 5. Exhaustion score
# ---------------------------------------------------------------------------

class TestExhaustionScore(unittest.TestCase):
    def test_opening_exhaustion_max(self):
        e = _event("OPENING_EXHAUSTION")
        m = compute_opening_metrics([e])
        self.assertGreaterEqual(m["exhaustion_score"], 40)

    def test_gap_fill_adds_exhaustion(self):
        events = [
            _event("GAP_FILL_COMPLETED"),
            _event("PREMARKET_HIGH_REJECT"),
        ]
        m = compute_opening_metrics(events)
        self.assertGreaterEqual(m["exhaustion_score"], 40)

    def test_no_exhaustion_signals(self):
        e = _event("VWAP_RECLAIM", price=165.0, vwap=164.0)
        m = compute_opening_metrics([e])
        self.assertEqual(m["exhaustion_score"], 0)


# ---------------------------------------------------------------------------
# 6. Premarket range
# ---------------------------------------------------------------------------

class TestPremarketRange(unittest.TestCase):
    def test_range_computed(self):
        e = _event("PREMARKET_HIGH_BREAK", price=170.0,
                   premarket_high=170.0, premarket_low=168.0)
        m = compute_opening_metrics([e])
        self.assertAlmostEqual(m["premarket_range"], 2.0)
        self.assertAlmostEqual(m["premarket_high"], 170.0)
        self.assertAlmostEqual(m["premarket_low"], 168.0)


# ---------------------------------------------------------------------------
# 7. Relative volume
# ---------------------------------------------------------------------------

class TestRelativeVolume(unittest.TestCase):
    def test_rvol_from_flags(self):
        e = _event("VOLUME_SURGE", price=170.0,
                   rvol_1m=2.5, rvol_5m=1.8, rvol_15m=1.5)
        m = compute_opening_metrics([e])
        self.assertAlmostEqual(m["relative_volume_1m"], 2.5)
        self.assertAlmostEqual(m["relative_volume_5m"], 1.8)
        self.assertAlmostEqual(m["relative_volume_15m"], 1.5)

    def test_rvol_none_when_absent(self):
        e = _event("VWAP_RECLAIM")
        m = compute_opening_metrics([e])
        self.assertIsNone(m["relative_volume_1m"])


# ---------------------------------------------------------------------------
# 8. Integration with score_spcx
# ---------------------------------------------------------------------------

class TestScoreIntegration(unittest.TestCase):
    def test_score_with_opening_metrics_has_enrichment(self):
        events = [
            _event("VWAP_RECLAIM", price=173.77, vwap=164.74),
            _event("ORB_HIGH_BREAK", price=173.77, orb_high=168.75),
            _event("GAP_OPEN_UP", prev_close=160.0, open_price=164.0),
        ]
        metrics = compute_opening_metrics(events)
        result = score_spcx(events, opening_metrics=metrics)
        self.assertIn("opening_metrics", result)
        self.assertIn("opening_components", result)
        self.assertIn("dynamic_boost", result["opening_components"])
        self.assertGreaterEqual(result["opening_components"]["dynamic_boost"], 20)

    def test_score_without_opening_metrics_no_enrichment(self):
        events = [
            _event("VWAP_RECLAIM", price=173.77, vwap=164.74),
        ]
        result = score_spcx(events)
        self.assertNotIn("opening_metrics", result)
        self.assertNotIn("opening_components", result)

    def test_dynamic_boost_capped_at_120(self):
        events = [
            _event("VWAP_RECLAIM", price=173.77, vwap=164.74),
            _event("ORB_HIGH_BREAK", price=173.77, orb_high=168.75),
            _event("PREMARKET_HIGH_BREAK", price=173.77,
                   flags={"premarket_high": 170.0}),
            _event("GAP_OPEN_UP", prev_close=160.0, open_price=164.0),
            _event("VOLUME_SURGE", price=1000000,
                   flags={"rvol_15m": 3.0}),
        ]
        metrics = compute_opening_metrics(events)
        result = score_spcx(events, opening_metrics=metrics)
        self.assertLessEqual(result["score"], 120)


if __name__ == "__main__":
    unittest.main()
