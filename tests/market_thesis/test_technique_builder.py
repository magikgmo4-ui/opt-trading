"""
Tests for builders/technique_builder.py — PR3.

Covers:
- Full build with multi-TF + vision + setups data
- Bias extraction from various sources
- Level extraction from vision + multi-TF
- Alignment computation
- Empty/partial data fallbacks
"""

from __future__ import annotations

import unittest

from modules.market_thesis.builders.technique_builder import build_technique
from modules.market_thesis.context_aggregator import MarketContextInput
from modules.market_thesis.source_readers import NormalizedEvent, NormalizedSetup, NormalizedVision


class TestBuildTechnique(unittest.TestCase):
    def test_full_build(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {
            "bias": {"htf": "bullish", "ltf": "bearish"},
            "levels": {
                "support_levels": [65000, 62000],
                "resistance_levels": [72000],
                "vwap": 66450,
            },
            "price": 66300,
        }
        ctx.vision_inputs = [
            NormalizedVision(
                source="vision_analysis",
                symbol="BTC",
                support_levels=[65000, 63000],
                resistance_levels=[68500, 70000],
            )
        ]
        ctx.priority_inputs = [
            NormalizedSetup(
                source="multitf_scores",
                symbol="BTC",
                setup_id="btc_vwap_reclaim",
                direction="long",
                setup_type="vwap_reclaim",
                grade="B",
                score=62,
                invalidation=65000,
                targets=[68000],
            )
        ]

        result = build_technique(ctx)
        self.assertEqual(result.htf_bias, "bullish")
        self.assertEqual(result.ltf_bias, "bearish")
        self.assertEqual(result.alignment, "divergent")
        self.assertGreater(len(result.key_support), 0)
        self.assertGreater(len(result.key_resistance), 0)
        self.assertEqual(result.vwap, 66450)
        self.assertIn("btc_vwap_reclaim", result.active_setups)

    def test_aligned_bullish(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {"bias": {"htf": "bullish", "ltf": "bullish"}}

        result = build_technique(ctx)
        self.assertEqual(result.alignment, "aligned_bullish")

    def test_aligned_bearish(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {"bias": {"htf": "bearish", "ltf": "bearish"}}

        result = build_technique(ctx)
        self.assertEqual(result.alignment, "aligned_bearish")

    def test_bias_from_timeframes(self):
        ctx = MarketContextInput(symbol="ETH")
        ctx.multitf_raw = {
            "timeframes": {
                "H4": {"indicators": {"trend": "bearish"}},
                "H1": {"indicators": {"trend": "bearish"}},
            }
        }

        result = build_technique(ctx)
        self.assertEqual(result.htf_bias, "bearish")  # H4 first try
        self.assertEqual(result.ltf_bias, "bearish")  # H1 first try

    def test_bias_from_vision_summary(self):
        ctx = MarketContextInput(symbol="XAU")
        ctx.vision_inputs = [
            NormalizedVision(
                source="vision_analysis",
                symbol="XAU",
                analysis_summary="Gold trend bullish on D1, resistance at 5100",
            )
        ]

        result = build_technique(ctx)
        self.assertEqual(result.htf_bias, "bullish")

    def test_bias_from_vision_bearish(self):
        ctx = MarketContextInput(symbol="XAU")
        ctx.vision_inputs = [
            NormalizedVision(
                source="vision_analysis",
                symbol="XAU",
                analysis_summary="Bearish structure. Bearish momentum increasing.",
            )
        ]

        result = build_technique(ctx)
        self.assertEqual(result.htf_bias, "bearish")

    def test_bias_from_cdp_signals(self):
        ctx = MarketContextInput(symbol="SOL")
        ctx.raw_events = [
            NormalizedEvent(source="cdp", symbol="SOL", event_type="VWAP_RECLAIM", direction="MONITOR_ONLY"),
            NormalizedEvent(source="cdp", symbol="SOL", event_type="ORB_HIGH_BREAK", direction="MONITOR_ONLY"),
            NormalizedEvent(source="cdp", symbol="SOL", event_type="VWAP_LOSS", direction="MONITOR_ONLY"),
        ]

        result = build_technique(ctx)
        # CDP signals are monitor_only — they don't have BUY/SELL direction,
        # so the LTF bias derivation should not be triggered by them
        self.assertEqual(result.htf_bias, "neutral")

    def test_bias_defaults_neutral(self):
        ctx = MarketContextInput(symbol="XRP")
        result = build_technique(ctx)
        self.assertEqual(result.htf_bias, "neutral")
        self.assertEqual(result.ltf_bias, "neutral")
        self.assertEqual(result.alignment, "neutral")

    def test_no_reject_setups_in_active(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.priority_inputs = [
            NormalizedSetup(source="mtf", symbol="BTC", setup_id="bad", grade="REJECT", direction="monitor_only", setup_type="none"),
            NormalizedSetup(source="mtf", symbol="BTC", setup_id="good", grade="B", direction="long", setup_type="breakout"),
        ]

        result = build_technique(ctx)
        self.assertNotIn("bad", result.active_setups)
        self.assertIn("good", result.active_setups)

    def test_narrative_never_empty(self):
        ctx = MarketContextInput(symbol="MU")
        result = build_technique(ctx)
        self.assertIsInstance(result.narrative, str)
        self.assertTrue(len(result.narrative) > 0)

    def test_vwap_extraction(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {"levels": {"vwap": 50000}}
        result = build_technique(ctx)
        self.assertEqual(result.vwap, 50000)


if __name__ == "__main__":
    unittest.main()
