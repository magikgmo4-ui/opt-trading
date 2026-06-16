"""
Tests for builders/news_builder.py — PR4.
"""

from __future__ import annotations

import unittest

from modules.market_thesis.builders.news_builder import build_news
from modules.market_thesis.context_aggregator import MarketContextInput
from modules.market_thesis.source_readers import NormalizedEvent, NormalizedSetup, NormalizedVision


class TestBuildNews(unittest.TestCase):
    def test_positive_from_telegram(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.telegram_inputs = [
            NormalizedEvent(source="telegram", symbol="BTC", event_type="trade", direction="LONG"),
            NormalizedEvent(source="telegram", symbol="BTC", event_type="trade", direction="LONG"),
            NormalizedEvent(source="telegram", symbol="BTC", event_type="trade", direction="LONG"),
            NormalizedEvent(source="telegram", symbol="BTC", event_type="trade", direction="SHORT"),
        ]

        result = build_news(ctx)
        self.assertIn(result.sentiment, ("positive", "neutral"))
        self.assertGreater(result.sentiment_score, 0)

    def test_negative_from_signals(self):
        ctx = MarketContextInput(symbol="ETH")
        ctx.telegram_inputs = [
            NormalizedEvent(source="telegram", symbol="ETH", event_type="trade", direction="SHORT"),
            NormalizedEvent(source="telegram", symbol="ETH", event_type="trade", direction="SHORT"),
        ]

        result = build_news(ctx)
        self.assertLess(result.sentiment_score, 0)

    def test_cdp_events_influence(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.news_inputs = [
            NormalizedEvent(source="cdp", symbol="BTC", event_type="VWAP_RECLAIM", direction="MONITOR_ONLY"),
            NormalizedEvent(source="cdp", symbol="BTC", event_type="ORB_HIGH_BREAK", direction="MONITOR_ONLY"),
        ]

        result = build_news(ctx)
        self.assertIn(result.sentiment, ("positive", "neutral"))

    def test_cdp_bearish_events(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.news_inputs = [
            NormalizedEvent(source="cdp", symbol="BTC", event_type="VWAP_LOSS", direction="MONITOR_ONLY"),
            NormalizedEvent(source="cdp", symbol="BTC", event_type="BOS_BEAR", direction="MONITOR_ONLY"),
        ]

        result = build_news(ctx)
        self.assertIn(result.sentiment, ("negative", "neutral"))

    def test_vision_analysis_influence(self):
        ctx = MarketContextInput(symbol="XAU")
        ctx.vision_inputs = [
            NormalizedVision(
                source="vision_analysis",
                symbol="XAU",
                analysis_summary="Bullish trend confirmed on D1. Strong momentum.",
            ),
        ]

        result = build_news(ctx)
        self.assertIn(result.sentiment, ("positive", "neutral"))

    def test_key_drivers_collected(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.raw_events = [
            NormalizedEvent(source="webhook", symbol="BTC", event_type="SELL", direction="SELL",
                           raw_reason="Bearish structure break H4"),
        ]
        ctx.priority_inputs = [
            NormalizedSetup(source="mtf", symbol="BTC", setup_id="btc_vwap", direction="long",
                           setup_type="breakout", grade="B", reasons=["VWAP reclaim setup"]),
        ]

        result = build_news(ctx)
        self.assertGreater(len(result.key_drivers), 0)

    def test_empty_defaults(self):
        ctx = MarketContextInput(symbol="MU")
        result = build_news(ctx)
        self.assertEqual(result.sentiment, "neutral")
        self.assertEqual(result.sentiment_score, 0.0)
        self.assertEqual(result.key_drivers, [])

    def test_narrative_never_empty(self):
        ctx = MarketContextInput(symbol="AVGO")
        result = build_news(ctx)
        self.assertTrue(len(result.narrative) > 0)

    def test_webhook_buy_influence(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.raw_events = [
            NormalizedEvent(source="webhook", symbol="BTC", event_type="BUY", direction="BUY", raw_reason="VWAP reclaim"),
            NormalizedEvent(source="webhook", symbol="BTC", event_type="BUY", direction="BUY", raw_reason="Support hold"),
        ]

        result = build_news(ctx)
        self.assertIn(result.sentiment, ("positive", "neutral"))


if __name__ == "__main__":
    unittest.main()
