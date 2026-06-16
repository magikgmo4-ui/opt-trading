"""
Tests for setup_card template — PR8.5.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from modules.executive_intelligence.templates.setup_card import render_setup_cards

MOCK_BTC_THESIS = {
    "symbol": "BTC",
    "confidence": 72,
    "action": {"direction": "bullish", "voice_one_liner": "BTC haussier."},
    "technical": {
        "htf_bias": "bullish", "ltf_bias": "bearish", "alignment": "divergent",
        "key_support": [65800, 65250], "key_resistance": [67250, 68200],
        "vwap": 66050, "active_setups": ["btc_vwap_reclaim"],
    },
    "flow": {"narrative": "OI en hausse."},
    "news": {"sentiment": "positive"},
    "probabilities": {"bull": 60, "range": 25, "bear": 15},
    "risks": [{"severity": "high", "description": "Crowding long."}],
    "freshness": {"overall": "fresh"},
}

MOCK_SPCX_THESIS = {
    "symbol": "SPCX",
    "confidence": 78,
    "action": {"direction": "bullish"},
    "technical": {
        "htf_bias": "bullish", "ltf_bias": "bullish", "alignment": "aligned_bullish",
        "key_support": [168, 166.8], "key_resistance": [172.5, 176, 190],
        "vwap": 170.4, "active_setups": ["spcx_vwap_reclaim"],
    },
    "flow": {},
    "news": {},
    "probabilities": {"bull": 64, "range": 21, "bear": 15},
    "risks": [{"severity": "moderate", "description": "Fake breakout IPO."}],
    "freshness": {"overall": "fresh"},
}


class TestSetupCards(unittest.TestCase):
    @patch("modules.executive_intelligence.templates.setup_card._gather_all_setups")
    def test_renders_cards(self, mock_gather):
        mock_gather.return_value = [
            {
                "symbol": "SPCX", "asset": "SpaceX (SPCX)", "asset_type": "Equity / IPO momentum",
                "setup": "Vwap Reclaim", "timeframe": "M15 / H1", "status": "Prioritaire",
                "grade": "A", "score": 84, "probability": 64,
                "bias": "Long", "price": 171.2, "vwap": 170.4,
                "support": [168, 166.8], "resistance": [172.5, 176],
                "entry_trigger": "Clôture M15 > 172", "entry_zone": "170 — 173",
                "stop_loss": 166.8, "invalidation": 166.8,
                "tp1": 176, "tp2": 182, "tp3": 190,
                "risk_reward": 2.1, "confirmation": "Volume + maintien VWAP",
                "risk_flags": "Fake breakout IPO",
                "action": "Attendre breakout confirmé",
            },
            {
                "symbol": "BTC", "asset": "BTC", "asset_type": "Crypto perp",
                "setup": "Pullback Vwap", "timeframe": "M15 / H1", "status": "Watch",
                "grade": "A-", "score": 78, "probability": 60,
                "bias": "Long", "price": 66385, "vwap": 66050,
                "support": [65800, 65250], "resistance": [67250, 68200],
                "entry_trigger": "Reclaim M15 sur pullback", "entry_zone": "65800 — 66100",
                "stop_loss": 65250, "invalidation": 65250,
                "tp1": 66800, "tp2": 67250, "tp3": 68200,
                "risk_reward": 1.8, "confirmation": "Structure + volume + timeframe",
                "risk_flags": "Crowding long",
                "action": "Ne pas acheter au milieu du range",
            },
        ]

        result = render_setup_cards()
        self.assertIn("spoken_text", result)
        self.assertIn("display_text", result)
        self.assertIn("cards", result)
        self.assertEqual(len(result["cards"]), 2)

    @patch("modules.executive_intelligence.templates.setup_card._gather_all_setups")
    def test_spoken_no_json(self, mock_gather):
        mock_gather.return_value = [
            {"symbol": "BTC", "asset": "BTC", "asset_type": "Crypto", "setup": "Vwap", "timeframe": "H1",
             "status": "Prioritaire", "grade": "A", "score": 80, "probability": 65, "bias": "Long",
             "price": 66000, "vwap": 65900, "support": [65000], "resistance": [67000],
             "entry_trigger": "Reclaim", "entry_zone": "65-66k", "stop_loss": 64800,
             "invalidation": 64800, "tp1": 67000, "tp2": 68000, "tp3": 69000,
             "risk_reward": 2.0, "confirmation": "Volume", "risk_flags": "Aucun",
             "action": "Attendre"},
        ]
        result = render_setup_cards()
        self.assertNotIn("{", result["spoken_text"])

    @patch("modules.executive_intelligence.templates.setup_card._gather_all_setups")
    def test_spoken_has_monitor_only(self, mock_gather):
        mock_gather.return_value = [
            {"symbol": "BTC", "asset": "BTC", "asset_type": "Crypto", "setup": "Vwap", "timeframe": "H1",
             "status": "Watch", "grade": "B", "score": 60, "probability": 50, "bias": "Long",
             "price": 66000, "vwap": 65900, "support": [65000], "resistance": [67000],
             "entry_trigger": "Reclaim", "entry_zone": "65-66k", "stop_loss": 64800,
             "invalidation": 64800, "tp1": 67000, "tp2": 68000, "tp3": 69000,
             "risk_reward": 2.0, "confirmation": "Volume", "risk_flags": "Aucun",
             "action": "Attendre"},
        ]
        result = render_setup_cards()
        self.assertIn("Aucun trade automatique", result["spoken_text"])

    @patch("modules.executive_intelligence.templates.setup_card._gather_all_setups")
    def test_cards_have_canonical_fields(self, mock_gather):
        mock_gather.return_value = [
            {"symbol": "BTC", "asset": "BTC", "asset_type": "Crypto", "setup": "Vwap", "timeframe": "H1",
             "status": "Prioritaire", "grade": "A", "score": 80, "probability": 65, "bias": "Long",
             "price": 66000, "vwap": 65900, "support": [65000], "resistance": [67000],
             "entry_trigger": "Reclaim", "entry_zone": "65-66k", "stop_loss": 64800,
             "invalidation": 64800, "tp1": 67000, "tp2": 68000, "tp3": 69000,
             "risk_reward": 2.0, "confirmation": "Volume", "risk_flags": "Aucun",
             "action": "Attendre"},
        ]
        result = render_setup_cards()
        card = result["cards"][0]
        canonical = ["asset", "asset_type", "setup", "timeframe", "status", "grade", "score",
                     "probability", "bias", "price", "vwap", "support", "resistance",
                     "entry_trigger", "entry_zone", "stop_loss", "invalidation",
                     "tp1", "tp2", "tp3", "risk_reward", "confirmation", "risk_flags", "action"]
        for field in canonical:
            self.assertIn(field, card, f"Missing canonical field: {field}")

    @patch("modules.executive_intelligence.templates.setup_card._gather_all_setups")
    def test_empty_setups(self, mock_gather):
        mock_gather.return_value = []
        result = render_setup_cards()
        self.assertIn("Aucun setup", result["spoken_text"])

    @patch("modules.executive_intelligence.templates.setup_card._gather_all_setups")
    def test_display_compact_format(self, mock_gather):
        mock_gather.return_value = [
            {"symbol": "SPCX", "asset": "SpaceX", "asset_type": "Equity", "setup": "Vwap Reclaim",
             "timeframe": "M15/H1", "status": "Prioritaire", "grade": "A", "score": 84,
             "probability": 64, "bias": "Long", "price": 171.2, "vwap": 170.4,
             "support": [168], "resistance": [172.5, 176], "entry_trigger": ">172.5",
             "entry_zone": "170-172.5", "stop_loss": 168, "invalidation": 168,
             "tp1": 176, "tp2": 182, "tp3": 190, "risk_reward": 2.1,
             "confirmation": "Volume", "risk_flags": "Fake breakout",
             "action": "Attendre"},
        ]
        result = render_setup_cards()
        display = result["display_text"]
        self.assertIn("Résumé marché", display)
        self.assertIn("SPCX", display)
        self.assertIn("A", display)


if __name__ == "__main__":
    unittest.main()
