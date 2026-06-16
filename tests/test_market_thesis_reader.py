"""
Tests for market_thesis_reader.py — PR8.
"""

from __future__ import annotations

import unittest

from modules.desk_pro.service.market_thesis_reader import (
    get_market_thesis,
    get_market_thesis_or_build,
    get_market_thesis_summary,
)


class TestMarketThesisReader(unittest.TestCase):
    def test_summary_returns_nine(self):
        items = get_market_thesis_summary()
        self.assertEqual(len(items), 9)

    def test_summary_has_required_fields(self):
        items = get_market_thesis_summary()
        for item in items:
            for field in ["symbol", "direction", "confidence", "prob_bull", "prob_bear", "one_liner"]:
                self.assertIn(field, item, f"Missing {field} in {item['symbol']}")

    def test_get_thesis_btc(self):
        thesis = get_market_thesis_or_build("BTC")
        self.assertIsNotNone(thesis)
        self.assertEqual(thesis["symbol"], "BTC")
        self.assertIn("context", thesis)
        self.assertIn("technical", thesis)
        self.assertIn("probabilities", thesis)

    def test_get_thesis_missing_returns_none(self):
        # Build then read
        get_market_thesis_or_build("ETH")
        thesis = get_market_thesis("ETH")
        self.assertIsNotNone(thesis)

    def test_summary_directions_valid(self):
        items = get_market_thesis_summary()
        valid = {"bullish", "bearish", "neutral", "wait", "unknown"}
        for item in items:
            self.assertIn(item["direction"], valid)

    def test_summary_confidence_range(self):
        items = get_market_thesis_summary()
        for item in items:
            conf = item["confidence"]
            self.assertGreaterEqual(conf, 0)
            self.assertLessEqual(conf, 100)

    def test_all_nine_symbols_buildable(self):
        for sym in ["BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU"]:
            thesis = get_market_thesis_or_build(sym)
            self.assertIsNotNone(thesis, f"Failed to build thesis for {sym}")
            self.assertEqual(thesis["symbol"], sym)
            self.assertEqual(thesis["action"]["readiness"], "monitor_only")


if __name__ == "__main__":
    unittest.main()
