"""
Tests for Voice Executive Operator — PR8.
"""

from __future__ import annotations

import unittest

from modules.voice_operator.formatters.executive_voice_formatter import (
    format_briefing_spoken,
    format_leaders_spoken,
    format_regime_spoken,
    format_risks_spoken,
)
from modules.voice_operator.formatters.executive_text_formatter import (
    format_briefing_text,
)

SAMPLE_BRIEFING = {
    "market_regime": "risk_on",
    "regime_confidence": 72,
    "overall_confidence": 68,
    "leaders": ["NVDA", "BTC", "SPCX"],
    "laggards": ["MU", "XRP"],
    "summary": "Le marché reste en régime Risk-On. Leaders NVDA et BTC.",
    "what_changed": "Régime passé de compression à risk_on.",
    "what_to_watch": "Surveiller le dollar et la concentration du momentum.",
    "top_risks": ["Crowding haussier sur 4 actifs", "Rebond du dollar"],
    "top_opportunities": ["Continuation BTC", "Momentum IA via NVDA"],
    "voice_one_liner": "Marché Risk-On.",
}

SAMPLE_REGIME = {
    "regime": "risk_on", "confidence": 72, "risk_score": 35,
    "narrative": "Régime Risk-On confirmé. DXY baissier, VIX bas.",
}

SAMPLE_RISKS = {
    "top_risks": ["Crowding haussier", "Dollar fort", "Volatilité SPCX"],
    "regime_risk": 35,
}

SAMPLE_LEADERS = {
    "leaders": [{"symbol": "NVDA", "rank": 1}, {"symbol": "BTC", "rank": 2}],
    "laggards": [{"symbol": "MU", "rank": 9}],
}


class TestExecutiveVoiceFormatter(unittest.TestCase):
    def test_briefing_spoken_no_json(self):
        spoken = format_briefing_spoken(SAMPLE_BRIEFING)
        self.assertNotIn("{", spoken)
        self.assertNotIn("}", spoken)

    def test_briefing_spoken_no_underscores(self):
        spoken = format_briefing_spoken(SAMPLE_BRIEFING)
        self.assertNotIn("risk_on", spoken.lower())
        self.assertNotIn("monitor_only", spoken)
        self.assertNotIn("voice_one_liner", spoken)

    def test_briefing_spoken_french(self):
        spoken = format_briefing_spoken(SAMPLE_BRIEFING)
        self.assertIn("Risk-On", spoken)
        self.assertIn("surveillance uniquement", spoken.lower())

    def test_briefing_spoken_under_400(self):
        spoken = format_briefing_spoken(SAMPLE_BRIEFING)
        self.assertLess(len(spoken), 400)

    def test_briefing_missing(self):
        spoken = format_briefing_spoken(None)
        self.assertIn("pas", spoken.lower())

    def test_regime_spoken(self):
        spoken = format_regime_spoken(SAMPLE_REGIME)
        self.assertIn("Risk-On", spoken)
        self.assertIn("surveillance", spoken.lower())

    def test_regime_missing(self):
        spoken = format_regime_spoken(None)
        self.assertIn("pas", spoken.lower())

    def test_risks_spoken(self):
        spoken = format_risks_spoken(SAMPLE_RISKS)
        self.assertIn("risque", spoken.lower())
        self.assertNotIn("{", spoken)

    def test_risks_empty(self):
        spoken = format_risks_spoken({"top_risks": []})
        self.assertIn("Aucun risque", spoken)

    def test_leaders_spoken(self):
        spoken = format_leaders_spoken(SAMPLE_LEADERS)
        self.assertIn("NVDA", spoken)
        self.assertIn("MU", spoken)

    def test_leaders_missing(self):
        spoken = format_leaders_spoken(None)
        self.assertIn("pas", spoken.lower())


class TestExecutiveTextFormatter(unittest.TestCase):
    def test_briefing_text_sections(self):
        text = format_briefing_text(SAMPLE_BRIEFING)
        for section in ["Résumé", "Leaders", "Risques", "Opportunités", "Ce qui a changé", "À surveiller"]:
            self.assertIn(section, text)

    def test_briefing_text_no_json(self):
        text = format_briefing_text(SAMPLE_BRIEFING)
        self.assertNotIn("{", text)
        self.assertNotIn("}", text)

    def test_briefing_text_french(self):
        text = format_briefing_text(SAMPLE_BRIEFING)
        self.assertNotIn("risk_on", text)
        self.assertIn("Risk-On", text)

    def test_briefing_text_monitor_only(self):
        text = format_briefing_text(SAMPLE_BRIEFING)
        self.assertIn("Surveillance uniquement", text)

    def test_briefing_text_missing(self):
        text = format_briefing_text(None)
        self.assertIn("non disponible", text.lower())


if __name__ == "__main__":
    unittest.main()
