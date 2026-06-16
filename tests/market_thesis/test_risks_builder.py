"""
Tests for builders/risks_builder.py — PR4.
"""

from __future__ import annotations

import unittest

from modules.market_thesis.builders.risks_builder import build_risks
from modules.market_thesis.context_aggregator import MarketContextInput
from modules.market_thesis.source_readers import NormalizedMetrics, NormalizedSetup


class TestBuildRisks(unittest.TestCase):
    def test_crowding_long_high(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.flow_inputs = NormalizedMetrics(
            source="mm", symbol="BTC", long_short_ratio=2.5,
        )

        risks = build_risks(ctx)
        concentration = [r for r in risks if r.category == "concentration" and r.severity == "high"]
        self.assertGreater(len(concentration), 0)

    def test_crowding_short_high(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.flow_inputs = NormalizedMetrics(
            source="mm", symbol="BTC", long_short_ratio=0.3,
        )

        risks = build_risks(ctx)
        concentration = [r for r in risks if r.category == "concentration" and "short" in r.description.lower()]
        self.assertGreater(len(concentration), 0)

    def test_extreme_funding(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.flow_inputs = NormalizedMetrics(
            source="mm", symbol="BTC", funding_rate=0.12,
        )

        risks = build_risks(ctx)
        funding_risks = [r for r in risks if "Funding" in r.description]
        self.assertGreater(len(funding_risks), 0)

    def test_no_setups_risk(self):
        ctx = MarketContextInput(symbol="XRP")
        # No setups

        risks = build_risks(ctx)
        tech_risks = [r for r in risks if r.category == "technical"]
        self.assertGreater(len(tech_risks), 0)

    def test_divergence_risk(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {"bias": {"htf": "bullish", "ltf": "bearish"}}

        risks = build_risks(ctx)
        div_risks = [r for r in risks if "divergence" in r.description.lower()]
        self.assertGreater(len(div_risks), 0)

    def test_liquidation_imbalance_long(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.flow_inputs = NormalizedMetrics(
            source="mm", symbol="BTC",
            liquidations_long=90_000_000,
            liquidations_short=10_000_000,
        )

        risks = build_risks(ctx)
        liq_risks = [r for r in risks if "capitulation" in r.description.lower()]
        self.assertGreater(len(liq_risks), 0)

    def test_liquidation_imbalance_short(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.flow_inputs = NormalizedMetrics(
            source="mm", symbol="BTC",
            liquidations_long=10_000_000,
            liquidations_short=90_000_000,
        )

        risks = build_risks(ctx)
        liq_risks = [r for r in risks if "short squeeze" in r.description.lower()]
        self.assertGreater(len(liq_risks), 0)

    def test_macro_event_risk(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.multitf_raw = {"macro_context": {"macro_high_impact_soon": True}}

        risks = build_risks(ctx)
        event_risks = [r for r in risks if r.category == "event"]
        self.assertGreater(len(event_risks), 0)

    def test_stale_sources_risk(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.stale_sources = ["Market Metrics", "Telegram Signals"]

        risks = build_risks(ctx)
        stale_risks = [r for r in risks if "stale" in r.description.lower()]
        self.assertGreater(len(stale_risks), 0)

    def test_empty_returns_list(self):
        ctx = MarketContextInput(symbol="MU")
        risks = build_risks(ctx)
        self.assertIsInstance(risks, list)

    def test_low_grade_setups_risk(self):
        ctx = MarketContextInput(symbol="BTC")
        ctx.priority_inputs = [
            NormalizedSetup(source="mtf", symbol="BTC", setup_id="bad", grade="C", direction="monitor_only", setup_type="none"),
        ]

        risks = build_risks(ctx)
        low_risks = [r for r in risks if "faible" in r.description.lower()]
        self.assertGreater(len(low_risks), 0)


if __name__ == "__main__":
    unittest.main()
