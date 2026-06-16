"""
Tests for builders/action_builder.py — PR5.
"""

from __future__ import annotations

import unittest

from modules.market_thesis.builders.action_builder import build_action
from modules.market_thesis.context_aggregator import MarketContextInput
from modules.market_thesis.source_readers import NormalizedSetup, NormalizedVision


class TestBuildAction(unittest.TestCase):
    def test_bullish_aligned(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.priority_inputs = [
            NormalizedSetup(source="mtf", symbol="BTC", setup_id="s1", direction="long",
                           setup_type="breakout", grade="A", entry_zone=[66000, 66500],
                           invalidation=65000, targets=[68000]),
        ]
        action = build_action(ctx, htf_bias="bullish", ltf_bias="bullish",
                             alignment="aligned_bullish", probability_bull=70, probability_bear=15,
                             has_setups=True)
        self.assertEqual(action.direction, "bullish")
        self.assertEqual(action.readiness, "monitor_only")

    def test_bearish_aligned(self):
        ctx = MarketContextInput(symbol="ETH")
        action = build_action(ctx, htf_bias="bearish", ltf_bias="bearish",
                             alignment="aligned_bearish", probability_bull=15, probability_bear=65,
                             has_setups=True)
        self.assertEqual(action.direction, "bearish")

    def test_wait_divergent(self):
        ctx = MarketContextInput(symbol="SOL")
        action = build_action(ctx, htf_bias="bullish", ltf_bias="bearish",
                             alignment="divergent", probability_bull=45, probability_bear=40,
                             has_setups=False)
        self.assertIn(action.direction, ("wait", "neutral"))

    def test_readiness_always_monitor_only(self):
        ctx = MarketContextInput(symbol="BTC")
        action = build_action(ctx, htf_bias="bullish", ltf_bias="bullish",
                             alignment="aligned_bullish", probability_bull=90, probability_bear=5,
                             has_setups=True)
        self.assertEqual(action.readiness, "monitor_only")

    def test_key_levels_from_setups(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.priority_inputs = [
            NormalizedSetup(source="mtf", symbol="BTC", setup_id="btc_long", direction="long",
                           setup_type="vwap", grade="A", entry_zone=[66000, 66500],
                           invalidation=65000, targets=[68000, 70000]),
        ]
        action = build_action(ctx, has_setups=True)
        self.assertGreater(len(action.key_levels), 0)
        self.assertTrue(any("btc_long" in lv for lv in action.key_levels))

    def test_key_levels_from_vision(self):
        ctx = MarketContextInput(symbol="XAU")
        ctx.vision_inputs = [
            NormalizedVision(source="vision", symbol="XAU",
                           support_levels=[5000], resistance_levels=[5100]),
        ]
        action = build_action(ctx)
        self.assertTrue(any("Support" in lv for lv in action.key_levels))
        self.assertTrue(any("Resistance" in lv for lv in action.key_levels))

    def test_key_levels_from_vwap(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {"levels": {"vwap": 66450}}
        action = build_action(ctx)
        self.assertTrue(any("VWAP" in lv for lv in action.key_levels))

    def test_narrative_not_empty(self):
        ctx = MarketContextInput(symbol="MU")
        action = build_action(ctx)
        self.assertTrue(len(action.narrative) > 0)

    def test_voice_one_liner_not_empty(self):
        ctx = MarketContextInput(symbol="AVGO")
        action = build_action(ctx)
        self.assertTrue(len(action.voice_one_liner) > 0)

    def test_voice_one_liner_under_200_chars(self):
        ctx = MarketContextInput(symbol="BTC")
        action = build_action(ctx, htf_bias="bullish", ltf_bias="bearish",
                             alignment="divergent", probability_bull=45, probability_bear=35)
        self.assertLessEqual(len(action.voice_one_liner), 200)

    def test_high_risk_warning_in_narrative(self):
        ctx = MarketContextInput(symbol="BTC")
        action = build_action(ctx, has_high_risk=True, has_setups=True)
        self.assertIn("risque", action.narrative.lower())

    def test_no_setups_warning_in_narrative(self):
        ctx = MarketContextInput(symbol="XRP")
        action = build_action(ctx, has_setups=False)
        self.assertIn("setup", action.narrative.lower())


if __name__ == "__main__":
    unittest.main()
