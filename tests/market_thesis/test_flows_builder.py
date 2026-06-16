"""
Tests for builders/flows_builder.py — PR3.

Covers:
- Full build with market metrics + coinglass vision
- Partial build with only market metrics
- Empty build (no data)
- Coinglass detection supplementation
- ETF flow derivation
"""

from __future__ import annotations

import unittest

from modules.market_thesis.builders.flows_builder import build_flows
from modules.market_thesis.context_aggregator import MarketContextInput
from modules.market_thesis.models import FlowSection
from modules.market_thesis.source_readers import NormalizedMetrics, NormalizedVision


class TestBuildFlows(unittest.TestCase):
    def test_full_build_from_metrics(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.flow_inputs = NormalizedMetrics(
            source="market_metrics",
            symbol="BTC",
            open_interest=28_500_000_000,
            funding_rate=0.0045,
            volume_24h=52_000_000_000,
            long_short_ratio=1.75,
            liquidations_long=35_000_000,
            liquidations_short=12_000_000,
            price_change_24h_pct=2.1,
        )

        result = build_flows(ctx)
        self.assertEqual(result.open_interest, 28_500_000_000)
        self.assertEqual(result.funding_rate, 0.0045)
        self.assertEqual(result.long_short_ratio, 1.75)
        self.assertEqual(result.liquidations_long, 35_000_000)
        self.assertEqual(result.liquidations_short, 12_000_000)
        self.assertEqual(result.oi_change_24h_pct, 2.1)
        self.assertIn("OI", result.narrative)

    def test_coinglass_supplements_missing_metrics(self):
        ctx = MarketContextInput(symbol="ETH")
        ctx.flow_inputs = NormalizedMetrics(
            source="market_metrics",
            symbol="ETH",
            open_interest=None,
            long_short_ratio=None,
            liquidations_long=None,
            liquidations_short=None,
        )
        ctx.vision_inputs = [
            NormalizedVision(
                source="vision_coinglass",
                symbol="ETH",
                coinglass_detections=[
                    {"detected_metric_type": "open_interest", "extracted_value": 15_000_000_000, "confidence": 0.75},
                    {"detected_metric_type": "long_short_ratio", "extracted_value": 0.44, "confidence": 0.68},
                    {"detected_metric_type": "liquidations_long", "extracted_value": 10_000_000, "confidence": 0.70},
                    {"detected_metric_type": "liquidations_short", "extracted_value": 5_000_000, "confidence": 0.65},
                ],
            )
        ]

        result = build_flows(ctx)
        self.assertEqual(result.open_interest, 15_000_000_000)
        self.assertEqual(result.long_short_ratio, 0.44)
        self.assertEqual(result.liquidations_long, 10_000_000)
        self.assertEqual(result.liquidations_short, 5_000_000)

    def test_coinglass_does_not_overwrite_existing(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.flow_inputs = NormalizedMetrics(
            source="market_metrics",
            symbol="BTC",
            open_interest=28_000_000_000,
        )
        ctx.vision_inputs = [
            NormalizedVision(
                source="vision_coinglass",
                symbol="BTC",
                coinglass_detections=[
                    {"detected_metric_type": "open_interest", "extracted_value": 99_000_000_000, "confidence": 0.50},
                ],
            )
        ]

        result = build_flows(ctx)
        # Should keep the market_metrics value (primary), not coinglass
        self.assertEqual(result.open_interest, 28_000_000_000)

    def test_etf_flow_from_macro_context(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {"macro_context": {"etf_flow_bias": "inflow"}}

        result = build_flows(ctx)
        self.assertEqual(result.etf_flow, "inflow")

    def test_etf_flow_from_price_trend(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.flow_inputs = NormalizedMetrics(
            source="market_metrics",
            symbol="BTC",
            price_change_24h_pct=3.5,
        )

        result = build_flows(ctx)
        self.assertEqual(result.etf_flow, "inflow")

    def test_etf_flow_from_negative_price(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.flow_inputs = NormalizedMetrics(
            source="market_metrics",
            symbol="BTC",
            price_change_24h_pct=-3.5,
        )

        result = build_flows(ctx)
        self.assertEqual(result.etf_flow, "outflow")

    def test_empty_flow(self):
        ctx = MarketContextInput(symbol="XRP")
        result = build_flows(ctx)
        self.assertIsNone(result.open_interest)
        self.assertIsNone(result.funding_rate)
        self.assertIn("insuffisantes", result.narrative.lower())

    def test_narrative_never_empty(self):
        ctx = MarketContextInput(symbol="MU")
        result = build_flows(ctx)
        self.assertIsInstance(result.narrative, str)
        self.assertTrue(len(result.narrative) > 0)

    def test_oi_change_from_orderflow(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.flow_inputs = NormalizedMetrics(source="mm", symbol="BTC", price_change_24h_pct=None)
        ctx.multitf_raw = {"orderflow": {"open_interest_change_pct": 5.5}}

        result = build_flows(ctx)
        self.assertEqual(result.oi_change_24h_pct, 5.5)

    def test_returns_flowsection_type(self):
        ctx = MarketContextInput(symbol="BTC")
        result = build_flows(ctx)
        self.assertIsInstance(result, FlowSection)


if __name__ == "__main__":
    unittest.main()
