"""
Tests for context_builder.py — PR3.

Covers:
- Full build from MarketContextInput with multi-TF data
- Partial build with missing data (defaults)
- Empty build (no data at all)
- Derivation from technique when macro missing
"""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from modules.market_thesis.context_aggregator import MarketContextInput
from modules.market_thesis.context_builder import build_context
from modules.market_thesis.source_readers import NormalizedMetrics, NormalizedSetup, NormalizedVision


class TestBuildContext(unittest.TestCase):
    def test_build_from_multitf_macro(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {
            "macro_context": {
                "risk_regime": "risk_on",
                "dxy_trend": "bearish",
                "vix_state": "low",
                "spy_trend": "bullish",
            },
            "bias": {"htf": "bullish", "ltf": "bearish"},
        }

        result = build_context(ctx)
        self.assertEqual(result.macro_regime, "risk_on")
        self.assertEqual(result.dxy_trend, "bearish")
        self.assertEqual(result.vix_state, "low")
        self.assertEqual(result.spy_trend, "bullish")
        self.assertIn("risk-on", result.narrative.lower())

    def test_derive_macro_regime_from_htf(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {"bias": {"htf": "bullish", "ltf": "bullish"}}

        result = build_context(ctx)
        self.assertEqual(result.macro_regime, "risk_on")
        self.assertEqual(result.market_phase, "markup")

    def test_bearish_regime_from_htf(self):
        ctx = MarketContextInput(symbol="ETH")
        ctx.multitf_raw = {"bias": {"htf": "bearish", "ltf": "bearish"}}

        result = build_context(ctx)
        self.assertEqual(result.macro_regime, "risk_off")
        self.assertEqual(result.market_phase, "markdown")

    def test_accumulation_phase(self):
        ctx = MarketContextInput(symbol="SOL")
        ctx.multitf_raw = {"bias": {"htf": "bearish", "ltf": "bullish"}}

        result = build_context(ctx)
        self.assertEqual(result.market_phase, "accumulation")

    def test_distribution_phase(self):
        ctx = MarketContextInput(symbol="SOL")
        ctx.multitf_raw = {"bias": {"htf": "bullish", "ltf": "bearish"}}

        result = build_context(ctx)
        self.assertEqual(result.market_phase, "distribution")

    def test_empty_context_fallback(self):
        ctx = MarketContextInput(symbol="XRP")
        # No data at all

        result = build_context(ctx)
        self.assertEqual(result.macro_regime, "unknown")
        self.assertEqual(result.market_phase, "unknown")
        self.assertIn("insuffisant", result.narrative.lower())

    def test_narrative_never_empty(self):
        ctx = MarketContextInput(symbol="MU")
        result = build_context(ctx)
        self.assertIsInstance(result.narrative, str)
        self.assertTrue(len(result.narrative) > 0)

    def test_extracts_from_timeframes(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {
            "timeframes": {
                "H4": {"indicators": {"trend": "bearish"}},
                "H1": {"indicators": {"trend": "bullish"}},
            }
        }

        result = build_context(ctx)
        self.assertEqual(result.macro_regime, "risk_off")  # H4 bearish → risk_off
        self.assertEqual(result.market_phase, "accumulation")  # HTF bear + LTF bull


if __name__ == "__main__":
    unittest.main()
