"""
Tests for narrative.py — PR3.

Covers all narrative generators: context, technique, flows.
All must return non-empty French strings, never crash.
"""

from __future__ import annotations

import unittest

from modules.market_thesis.narrative import (
    context_narrative,
    flows_narrative,
    technique_narrative,
)


class TestContextNarrative(unittest.TestCase):
    def test_full_context(self):
        result = context_narrative(
            macro_regime="risk_on",
            dxy_trend="bearish",
            vix_state="low",
            spy_trend="bullish",
            market_phase="markup",
            fear_greed=72,
        )
        self.assertIn("risk-on", result.lower())
        self.assertIn("dxy", result.lower())
        self.assertIn("vix", result.lower())
        self.assertIn("spy", result.lower())
        self.assertIn("greed", result.lower())

    def test_partial_context(self):
        result = context_narrative(macro_regime="risk_off", dxy_trend="bullish")
        self.assertIn("risk-off", result.lower())
        self.assertIn("dxy", result.lower())

    def test_empty_context(self):
        result = context_narrative()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn("insuffisant", result.lower())

    def test_all_unknown(self):
        result = context_narrative(
            macro_regime="unknown",
            dxy_trend="unknown",
            vix_state="unknown",
            spy_trend="unknown",
            market_phase="unknown",
        )
        self.assertIn("insuffisant", result.lower())

    def test_fear_greed_extreme_fear(self):
        result = context_narrative(fear_greed=15)
        self.assertIn("peur extrême", result.lower())

    def test_fear_greed_extreme_greed(self):
        result = context_narrative(fear_greed=85)
        self.assertIn("greed extrême", result.lower())

    def test_french_language(self):
        """All narratives must contain French, not English boilerplate."""
        result = context_narrative(macro_regime="risk_on")
        self.assertNotIn("TODO", result)
        self.assertNotIn("placeholder", result.lower())
        self.assertNotIn("lorem ipsum", result.lower())


class TestTechniqueNarrative(unittest.TestCase):
    def test_full(self):
        result = technique_narrative(
            htf_bias="bullish",
            ltf_bias="bearish",
            alignment="divergent",
            supports=[65000, 62000],
            resistances=[72000],
            vwap=66450,
            price=66300,
            active_setups=["btc_vwap_reclaim"],
        )
        self.assertIn("haussier", result.lower())
        self.assertIn("baissier", result.lower())
        self.assertIn("divergent", result.lower())
        self.assertIn("65000", result)
        self.assertIn("VWAP", result)
        self.assertIn("btc_vwap_reclaim", result)

    def test_minimal(self):
        result = technique_narrative()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn("biais", result.lower())

    def test_no_levels(self):
        result = technique_narrative(htf_bias="bearish", ltf_bias="bearish", alignment="aligned_bearish")
        self.assertIn("baissier", result.lower())

    def test_price_above_vwap(self):
        result = technique_narrative(vwap=65000, price=67000)
        self.assertIn("au-dessus", result.lower())

    def test_price_below_vwap(self):
        result = technique_narrative(vwap=67000, price=65000)
        self.assertIn("sous", result.lower())

    def test_french_no_english(self):
        result = technique_narrative()
        self.assertNotIn("TODO", result)
        self.assertNotIn("placeholder", result.lower())


class TestFlowsNarrative(unittest.TestCase):
    def test_full(self):
        result = flows_narrative(
            open_interest=28_500_000_000,
            oi_change_pct=2.1,
            funding_rate=0.0045,
            long_short_ratio=1.8,
            liquidations_long=45_000_000,
            liquidations_short=12_000_000,
            etf_flow="inflow",
        )
        self.assertIn("OI", result)
        self.assertIn("28.5B", result)
        self.assertIn("Funding", result)
        self.assertIn("L/S", result)
        self.assertIn("ETF", result)

    def test_high_funding(self):
        result = flows_narrative(funding_rate=0.02)
        self.assertIn("élevé", result.lower())

    def test_negative_funding(self):
        result = flows_narrative(funding_rate=-0.005)
        self.assertIn("négatif", result.lower())

    def test_crowding_long(self):
        result = flows_narrative(long_short_ratio=2.5)
        self.assertIn("crowding long", result.lower())

    def test_crowding_short(self):
        result = flows_narrative(long_short_ratio=0.3)
        self.assertIn("crowding short", result.lower())

    def test_liquidations_long_dominant(self):
        result = flows_narrative(liquidations_long=100, liquidations_short=10)
        self.assertIn("longs dominantes", result.lower())

    def test_liquidations_short_dominant(self):
        result = flows_narrative(liquidations_long=10, liquidations_short=100)
        self.assertIn("shorts dominantes", result.lower())

    def test_empty(self):
        result = flows_narrative()
        self.assertIn("insuffisantes", result.lower())

    def test_etf_outflow(self):
        result = flows_narrative(etf_flow="outflow")
        self.assertIn("outflow", result.lower())

    def test_french_no_english(self):
        result = flows_narrative(open_interest=1e9)
        self.assertNotIn("TODO", result)
        self.assertNotIn("placeholder", result.lower())


if __name__ == "__main__":
    unittest.main()
