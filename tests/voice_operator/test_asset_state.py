"""
Tests for asset_state_formatter — PR8 extension.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from modules.voice_operator.formatters.asset_state_formatter import (
    format_asset_state_display,
    format_asset_state_spoken,
    _gather_asset_state,
)

SAMPLE_THESIS = {
    "symbol": "BTC",
    "confidence": 68,
    "action": {
        "direction": "bullish",
        "readiness": "monitor_only",
        "voice_one_liner": "BTC haussier modéré.",
        "narrative": "Biais haussier modéré. Attendre confirmation.",
        "key_levels": ["Support: 65000", "Invalidation: 63000", "Target: 72000"],
    },
    "context": {
        "macro_regime": "risk_on",
        "dxy_trend": "bearish",
        "vix_state": "low",
        "market_phase": "markup",
        "narrative": "Contexte macro favorable. DXY en baisse, VIX bas.",
    },
    "technical": {
        "htf_bias": "bullish",
        "ltf_bias": "bearish",
        "alignment": "divergent",
        "key_support": [65000, 62000],
        "key_resistance": [72000],
        "narrative": "Structure D1 haussière mais H4 bearish. Divergence HTF/LTF.",
    },
    "flow": {"narrative": "OI en hausse. Funding positif. ETF inflows."},
    "news": {"sentiment": "positive", "narrative": "Sentiment positif. Drivers: ETF, CPI.", "key_drivers": ["ETF inflows", "CPI bas"]},
    "probabilities": {"bull": 55, "range": 30, "bear": 15},
    "risks": [
        {"category": "concentration", "severity": "high", "description": "Crowding long élevé. Risque de cascade si support cassé."},
        {"category": "technical", "severity": "moderate", "description": "Divergence HTF/LTF."},
    ],
    "sources": [
        {"name": "Binance spot", "contract": "mm.v1", "status": "used", "age_minutes": 3.0},
        {"name": "Multi-TF", "contract": "mtf.v1", "status": "used", "age_minutes": 8.0},
    ],
    "freshness": {"overall": "fresh", "max_age_minutes": 8.0, "source_count": 10, "fresh_count": 8},
    "metadata": {"thesis_id": "t1", "generated_at": "2026-06-15T12:00:00Z"},
}

SAMPLE_EXEC = {
    "market_regime": "risk_on",
    "regime_confidence": 72,
    "leaders": ["NVDA", "BTC", "SPCX"],
    "laggards": ["MU", "XRP"],
}

SAMPLE_RELIABILITY = {"score": 82, "grade": "excellent", "sample_size": 200}


class TestAssetStateFormatter(unittest.TestCase):
    def test_spoken_no_json(self):
        spoken = format_asset_state_spoken("BTC", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertNotIn("{", spoken)

    def test_spoken_no_underscores(self):
        spoken = format_asset_state_spoken("BTC", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertNotIn("risk_on", spoken.lower())
        self.assertNotIn("monitor_only", spoken)

    def test_spoken_surveillance_uniquement(self):
        spoken = format_asset_state_spoken("BTC", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertIn("surveillance uniquement", spoken.lower())

    def test_spoken_french(self):
        spoken = format_asset_state_spoken("BTC", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertIn("haussier", spoken.lower())

    def test_spoken_under_400(self):
        spoken = format_asset_state_spoken("BTC", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertLess(len(spoken), 400)

    def test_spoken_missing(self):
        spoken = format_asset_state_spoken("XRP", {"thesis": None, "executive": None, "reliability": None})
        self.assertIn("pas", spoken.lower())

    def test_xau_spoken_uses_or(self):
        spoken = format_asset_state_spoken("XAU", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertIn("l'or", spoken.lower())

    def test_spcx_spoken_uses_spacex(self):
        spoken = format_asset_state_spoken("SPCX", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertIn("SpaceX", spoken)

    def test_display_sections_present(self):
        text = format_asset_state_display("BTC", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        for section in ["Résumé exécutif", "Situation actuelle", "Ce qui soutient", "Ce qui menace", "Scénarios", "Action"]:
            self.assertIn(section, text, f"Missing section: {section}")

    def test_display_no_json(self):
        text = format_asset_state_display("BTC", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertNotIn("{", text)

    def test_display_no_underscores(self):
        text = format_asset_state_display("BTC", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertNotIn("risk_on", text)
        self.assertNotIn("monitor_only", text)

    def test_display_has_reliability(self):
        text = format_asset_state_display("BTC", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertIn("82%", text)
        self.assertIn("Excellent", text)

    def test_display_missing(self):
        text = format_asset_state_display("XRP", {"thesis": None, "executive": None, "reliability": None})
        self.assertIn("non disponible", text.lower())

    def test_display_has_leader_position(self):
        text = format_asset_state_display("BTC", {"thesis": SAMPLE_THESIS, "executive": SAMPLE_EXEC, "reliability": SAMPLE_RELIABILITY})
        self.assertIn("Leader", text)

    def test_stale_spoken(self):
        stale_thesis = dict(SAMPLE_THESIS)
        stale_thesis["freshness"] = {"overall": "stale", "max_age_minutes": 180}
        spoken = format_asset_state_spoken("BTC", {"thesis": stale_thesis, "executive": None, "reliability": None})
        self.assertIn("validée", spoken.lower())


if __name__ == "__main__":
    unittest.main()
