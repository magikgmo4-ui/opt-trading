"""
Tests for Voice Operator Market Thesis — PR9.
Covers: reader, voice formatter, text formatter, endpoints, anti-robot rules.
"""

from __future__ import annotations

import unittest

from modules.voice_operator.formatters.market_thesis_voice_formatter import (
    format_spoken,
    format_summary_spoken,
)
from modules.voice_operator.formatters.market_thesis_text_formatter import (
    format_display,
    format_summary_display,
)


class TestVoiceFormatterAntiRobot(unittest.TestCase):
    """Anti-robot speech rules."""

    def setUp(self):
        self.thesis = {
            "symbol": "BTC",
            "confidence": 68,
            "action": {"direction": "bullish", "readiness": "monitor_only", "voice_one_liner": "BTC biais haussier.", "key_levels": ["Support: 65000"]},
            "context": {"macro_regime": "risk_on", "dxy_trend": "bearish", "vix_state": "low", "market_phase": "markup", "narrative": "Contexte macro favorable. DXY en baisse, VIX bas."},
            "technical": {"htf_bias": "bullish", "ltf_bias": "bearish", "alignment": "divergent", "narrative": "Structure D1 haussière mais H4 bearish."},
            "flow": {"narrative": "OI en hausse. Funding positif."},
            "news": {"sentiment": "positive", "narrative": "Sentiment positif."},
            "probabilities": {"bull": 50, "range": 30, "bear": 20},
            "risks": [{"category": "concentration", "severity": "high", "description": "Crowding long élevé. Risque de cascade si support cassé."}],
            "sources": [{"name": "Binance", "contract": "mm.v1", "status": "used", "age_minutes": 3.0}],
            "freshness": {"overall": "fresh", "max_age_minutes": 5, "source_count": 10, "fresh_count": 8},
            "metadata": {"thesis_id": "t1", "generated_at": "2026-06-15T12:00:00Z"},
            "probabilities": {"bull": 55, "range": 30, "bear": 15},
        }

    def test_no_json_in_spoken(self):
        spoken = format_spoken("BTC", self.thesis)
        self.assertNotIn("{", spoken)
        self.assertNotIn("}", spoken)
        self.assertNotIn('"', spoken)

    def test_no_underscores_in_spoken(self):
        spoken = format_spoken("BTC", self.thesis)
        self.assertNotIn("monitor_only", spoken)
        self.assertNotIn("risk_on", spoken)
        self.assertNotIn("voice_one_liner", spoken)
        self.assertNotIn("macro_regime", spoken)

    def test_monitor_only_explicit(self):
        spoken = format_spoken("BTC", self.thesis)
        self.assertIn("surveillance uniquement", spoken.lower())

    def test_french_not_english(self):
        spoken = format_spoken("BTC", self.thesis)
        self.assertNotIn("bullish", spoken.lower())
        self.assertNotIn("bearish", spoken.lower())
        self.assertIn("haussier", spoken.lower())

    def test_spoken_under_4_sentences_approx(self):
        spoken = format_spoken("BTC", self.thesis)
        sentences = [s.strip() for s in spoken.split(".") if s.strip()]
        self.assertLessEqual(len(sentences), 6)

    def test_spoken_under_400_chars(self):
        spoken = format_spoken("BTC", self.thesis)
        self.assertLess(len(spoken), 400)

    def test_missing_thesis(self):
        spoken = format_spoken("BTC", None)
        self.assertIn("pas", spoken.lower())
        self.assertNotIn("{", spoken)


class TestTextFormatter(unittest.TestCase):
    def setUp(self):
        self.thesis = {
            "symbol": "BTC",
            "confidence": 55,
            "action": {"direction": "bearish", "readiness": "monitor_only", "voice_one_liner": "BTC baissier.", "narrative": "Attendre confirmation.", "key_levels": ["Support: 65000", "Invalidation: 63000"]},
            "context": {"macro_regime": "risk_off", "dxy_trend": "bullish", "vix_state": "elevated", "market_phase": "markdown", "narrative": "Contexte défavorable."},
            "technical": {"htf_bias": "bearish", "ltf_bias": "bearish", "alignment": "aligned_bearish", "narrative": "Structure bearish."},
            "flow": {"narrative": "OI en baisse."},
            "news": {"sentiment": "negative", "narrative": "Sentiment négatif."},
            "probabilities": {"bull": 20, "range": 30, "bear": 50},
            "risks": [{"category": "technical", "severity": "moderate", "description": "Divergence HTF/LTF."}],
            "sources": [{"name": "Binance", "contract": "mm.v1", "status": "used", "age_minutes": 5.0}],
            "freshness": {"overall": "stale", "max_age_minutes": 60, "source_count": 10, "fresh_count": 3},
            "metadata": {"thesis_id": "t1", "generated_at": "2026-06-15T12:00:00Z"},
        }

    def test_sections_present(self):
        display = format_display("BTC", self.thesis)
        self.assertIn("Contexte", display)
        self.assertIn("Analyse technique", display)
        self.assertIn("Flux", display)
        self.assertIn("Actualité", display)
        self.assertIn("Risques", display)
        self.assertIn("Probabilités", display)
        self.assertIn("Recommandation", display)
        self.assertIn("Sources", display)
        self.assertIn("Fraîcheur", display)

    def test_no_json_in_display(self):
        display = format_display("BTC", self.thesis)
        self.assertNotIn("{", display)
        self.assertNotIn("}", display)

    def test_no_raw_field_names(self):
        display = format_display("BTC", self.thesis)
        self.assertNotIn("voice_one_liner", display)
        self.assertNotIn("monitor_only", display)
        self.assertNotIn("macro_regime", display)
        self.assertNotIn("readiness", display)

    def test_french_terms(self):
        display = format_display("BTC", self.thesis)
        self.assertIn("Haussier", display)  # in probabilities
        self.assertNotIn("bullish", display.lower())

    def test_missing_thesis_display(self):
        display = format_display("BTC", None)
        self.assertIn("non disponible", display.lower())

    def test_xau_display_name(self):
        display = format_display("XAU", self.thesis)
        self.assertIn("Or (XAU)", display)

    def test_spcx_display_name(self):
        display = format_display("SPCX", self.thesis)
        self.assertIn("SpaceX (SPCX)", display)


class TestVoiceFormatterStaleFallback(unittest.TestCase):
    def test_stale_warning(self):
        thesis = {
            "action": {"direction": "neutral"},
            "confidence": 50,
            "context": {"narrative": "Contexte."},
            "technical": {"htf_bias": "neutral", "ltf_bias": "neutral", "alignment": "neutral", "narrative": "Structure."},
            "flow": {"narrative": "Flux."},
            "news": {"sentiment": "neutral", "narrative": "News."},
            "probabilities": {"bull": 33, "range": 34, "bear": 33},
            "risks": [],
            "sources": [],
            "freshness": {"overall": "stale", "max_age_minutes": 120, "source_count": 1, "fresh_count": 0},
            "metadata": {"thesis_id": "t1"},
        }
        spoken = format_spoken("BTC", thesis)
        self.assertIn("validée", spoken.lower())

    def test_expired_warning(self):
        thesis = {
            "action": {"direction": "neutral"},
            "confidence": 50,
            "context": {"narrative": "Contexte."},
            "technical": {"htf_bias": "neutral", "ltf_bias": "neutral", "alignment": "neutral", "narrative": "Structure."},
            "flow": {"narrative": "Flux."},
            "news": {"sentiment": "neutral", "narrative": "News."},
            "probabilities": {"bull": 33, "range": 34, "bear": 33},
            "risks": [],
            "sources": [],
            "freshness": {"overall": "expired", "max_age_minutes": 300, "source_count": 1, "fresh_count": 0},
            "metadata": {"thesis_id": "t1"},
        }
        spoken = format_spoken("BTC", thesis)
        self.assertIn("validée", spoken.lower())


class TestSummaryFormatters(unittest.TestCase):
    def setUp(self):
        self.summaries = [
            {"symbol": "BTC", "direction": "bullish", "confidence": 68, "one_liner": "BTC haussier.", "freshness": "fresh"},
            {"symbol": "ETH", "direction": "bearish", "confidence": 40, "one_liner": "ETH baissier.", "freshness": "warm"},
            {"symbol": "XAU", "direction": "bullish", "confidence": 72, "one_liner": "Gold haussier.", "freshness": "fresh"},
        ]

    def test_summary_spoken(self):
        spoken = format_summary_spoken(self.summaries)
        self.assertIn("actifs", spoken.lower())
        self.assertNotIn("{", spoken)

    def test_summary_display(self):
        display = format_summary_display(self.summaries)
        self.assertIn("BTC", display)
        self.assertIn("ETH", display)
        self.assertIn("XAU", display)

    def test_empty_summary(self):
        self.assertIn("Aucune", format_summary_spoken([]))
        self.assertIn("Aucune", format_summary_display([]))


class TestXAUAndSPCXNames(unittest.TestCase):
    def setUp(self):
        self.thesis = {
            "symbol": "XAU",
            "confidence": 70,
            "action": {"direction": "bullish", "readiness": "monitor_only", "voice_one_liner": "Gold haussier.", "key_levels": ["Support: 5000"]},
            "context": {"macro_regime": "risk_on", "narrative": "Contexte favorable."},
            "technical": {"htf_bias": "bullish", "ltf_bias": "bullish", "alignment": "aligned_bullish", "narrative": "Structure haussière."},
            "flow": {"narrative": "Flux normaux."},
            "news": {"sentiment": "positive", "narrative": "Positif."},
            "probabilities": {"bull": 60, "range": 25, "bear": 15},
            "risks": [],
            "sources": [],
            "freshness": {"overall": "fresh", "max_age_minutes": 5, "source_count": 5, "fresh_count": 5},
            "metadata": {"thesis_id": "t1"},
        }

    def test_xau_spoken_uses_or(self):
        spoken = format_spoken("XAU", self.thesis)
        self.assertIn("l'or", spoken.lower())

    def test_spcx_spoken_uses_spacex(self):
        thesis_spcx = dict(self.thesis)
        thesis_spcx["symbol"] = "SPCX"
        spoken = format_spoken("SPCX", thesis_spcx)
        self.assertIn("SpaceX", spoken)


if __name__ == "__main__":
    unittest.main()
