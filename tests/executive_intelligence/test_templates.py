"""
Tests for Presentation Templates Engine — PR8.5.
"""

from __future__ import annotations

import unittest

from modules.executive_intelligence.templates.asset_analysis import render_asset_analysis

SAMPLE_THESIS = {
    "symbol": "BTC", "confidence": 68,
    "action": {"direction": "bullish", "readiness": "monitor_only", "voice_one_liner": "BTC haussier modéré.", "narrative": "Biais haussier. Attendre confirmation.", "key_levels": ["Support: 65000", "Invalidation: 63000"]},
    "context": {"macro_regime": "risk_on", "dxy_trend": "bearish", "vix_state": "low", "market_phase": "markup", "narrative": "Contexte macro favorable. DXY en baisse, VIX bas, SPY haussier."},
    "technical": {"htf_bias": "bullish", "ltf_bias": "bearish", "alignment": "divergent", "key_support": [65000, 62000], "key_resistance": [72000], "vwap": 66450, "active_setups": ["btc_vwap_reclaim"]},
    "flow": {"open_interest": 28500000000, "funding_rate": 0.0045, "long_short_ratio": 1.8, "liquidations_long": 45000000, "liquidations_short": 12000000, "narrative": "OI en hausse. Funding positif."},
    "news": {"sentiment": "positive", "narrative": "Sentiment news positif.", "key_drivers": ["ETF inflows"]},
    "probabilities": {"bull": 55, "range": 30, "bear": 15},
    "risks": [{"category": "concentration", "severity": "high", "description": "Crowding long élevé."}, {"category": "technical", "severity": "moderate", "description": "Divergence HTF/LTF."}],
    "sources": [{"name": "Binance", "contract": "mm.v1", "status": "used", "age_minutes": 3}],
    "freshness": {"overall": "fresh", "max_age_minutes": 5, "source_count": 10, "fresh_count": 8},
}

SAMPLE_EXEC = {"market_regime": "risk_on", "regime_confidence": 72, "leaders": ["NVDA", "BTC", "SPCX"], "laggards": ["MU", "XRP"]}
SAMPLE_RELIABILITY = {"score": 82, "grade": "excellent", "sample_size": 200}


class TestAssetAnalysisTemplate(unittest.TestCase):
    def setUp(self):
        self.data = {
            "symbol": "BTC",
            "thesis": SAMPLE_THESIS,
            "executive": SAMPLE_EXEC,
            "reliability": SAMPLE_RELIABILITY,
        }

    def test_renders_spoken(self):
        result = render_asset_analysis("BTC", self.data)
        self.assertIn("spoken_text", result)
        self.assertGreater(len(result["spoken_text"]), 20)

    def test_renders_display(self):
        result = render_asset_analysis("BTC", self.data)
        self.assertIn("display_text", result)
        self.assertGreater(len(result["display_text"]), 200)

    def test_renders_cards(self):
        result = render_asset_analysis("BTC", self.data)
        self.assertGreater(len(result["cards"]), 3)

    def test_no_json_in_spoken(self):
        result = render_asset_analysis("BTC", self.data)
        self.assertNotIn("{", result["spoken_text"])
        self.assertNotIn("}", result["spoken_text"])

    def test_no_underscores_in_display(self):
        result = render_asset_analysis("BTC", self.data)
        self.assertNotIn("risk_on", result["display_text"])
        self.assertNotIn("monitor_only", result["display_text"])

    def test_display_has_sections(self):
        result = render_asset_analysis("BTC", self.data)
        display = result["display_text"]
        for section in ["Résumé exécutif", "Situation actuelle", "Ce qui soutient", "Ce qui menace", "Scénarios", "Action"]:
            self.assertIn(section, display, f"Missing: {section}")

    def test_display_has_table(self):
        result = render_asset_analysis("BTC", self.data)
        display = result["display_text"]
        self.assertIn("Biais", display)
        self.assertIn("Confiance", display)

    def test_french_not_english(self):
        result = render_asset_analysis("BTC", self.data)
        self.assertNotIn("bullish", result["display_text"].lower())

    def test_monitor_only_in_display(self):
        result = render_asset_analysis("BTC", self.data)
        self.assertIn("Surveillance", result["display_text"])

    def test_missing_data(self):
        result = render_asset_analysis("XRP", {"thesis": None, "executive": None, "reliability": None})
        self.assertIn("pas", result["spoken_text"].lower())
        self.assertIn("Non disponible", result["display_text"])

    def test_spcx_name(self):
        data = dict(self.data)
        data["symbol"] = "SPCX"
        result = render_asset_analysis("SPCX", data)
        self.assertIn("SpaceX", result["spoken_text"])
        self.assertIn("SpaceX", result["display_text"])

    def test_xau_name(self):
        data = dict(self.data)
        data["symbol"] = "XAU"
        result = render_asset_analysis("XAU", data)
        self.assertIn("l'or", result["spoken_text"].lower())

    def test_spoken_under_400(self):
        result = render_asset_analysis("BTC", self.data)
        self.assertLess(len(result["spoken_text"]), 400)


if __name__ == "__main__":
    unittest.main()
