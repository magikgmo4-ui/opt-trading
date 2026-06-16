"""
Tests for executive API — PR6.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from modules.executive_intelligence.api import app, _cache

client = TestClient(app)


def _mock_brief():
    from modules.executive_intelligence.models import ExecutiveBriefing
    from datetime import datetime, timezone
    return ExecutiveBriefing(
        briefing_id="b1",
        generated_at=datetime.now(timezone.utc),
        market_regime="risk_on",
        regime_confidence=75,
        overall_confidence=72,
        leaders=["BTC", "NVDA", "SPCX"],
        laggards=["MU", "XRP"],
        summary="Régime Risk-On. Leaders BTC, NVDA.",
        what_changed="Régime passé à risk_on.",
        what_to_watch="Surveiller le dollar.",
        top_risks=["Crowding haussier", "Dollar fort"],
        top_opportunities=["BTC momentum", "NVDA IA"],
        voice_one_liner="Marché Risk-On.",
        voice_briefing="Régime Risk-On avec 75% de confiance.",
    )


def _mock_regime():
    from modules.executive_intelligence.models import MarketRegime, RegimeEvidence
    return MarketRegime(
        regime="risk_on",
        confidence=75,
        risk_score=35,
        evidence=RegimeEvidence(
            dxy_trend="bearish", vix_level="low", spy_trend="bullish",
            asset_count_bullish=6, asset_count_bearish=2,
        ),
        narrative="Régime Risk-On.",
    )


def _mock_board():
    from modules.executive_intelligence.models import LeaderBoardEntry
    return [
        LeaderBoardEntry(symbol="NVDA", rank=1, direction="bullish", confidence=85, reliability=78, momentum_score=80, is_leader=True),
        LeaderBoardEntry(symbol="BTC", rank=2, direction="bullish", confidence=75, reliability=82, momentum_score=70, is_leader=True),
        LeaderBoardEntry(symbol="SPCX", rank=3, direction="bullish", confidence=65, reliability=60, momentum_score=55, is_leader=True),
        LeaderBoardEntry(symbol="MU", rank=9, direction="bearish", confidence=30, reliability=48, momentum_score=20, is_laggard=True),
    ]


class TestExecutiveAPI(unittest.TestCase):
    def setUp(self):
        _cache.clear()
        self._patches = [
            patch("modules.executive_intelligence.api._build_full", return_value={"ok": True, "summary": "test"}),
            patch("modules.executive_intelligence.api._build_briefing", return_value={"ok": True, "summary": "briefing test"}),
            patch("modules.executive_intelligence.api._build_regime", return_value={"ok": True, "regime": "risk_on"}),
            patch("modules.executive_intelligence.api._build_leaders", return_value={"ok": True, "leaders": []}),
            patch("modules.executive_intelligence.api._build_risks", return_value={"ok": True, "top_risks": []}),
        ]
        for p in self._patches:
            p.start()

    def tearDown(self):
        _cache.clear()
        for p in self._patches:
            p.stop()

    def test_health(self):
        r = client.get("/health")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["ok"])

    def test_executive_full(self):
        r = client.get("/read/executive")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["ok"])

    def test_executive_briefing(self):
        r = client.get("/read/executive/briefing")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["ok"])

    def test_executive_regime(self):
        r = client.get("/read/executive/regime")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["ok"])

    def test_executive_leaders(self):
        r = client.get("/read/executive/leaders")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["ok"])

    def test_executive_risks(self):
        r = client.get("/read/executive/risks")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["ok"])

    def test_build_true(self):
        r = client.get("/read/executive?build=true")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["source"], "build")

    def test_cache_hit(self):
        r1 = client.get("/read/executive")
        self.assertEqual(r1.json()["source"], "build")
        r2 = client.get("/read/executive")
        self.assertEqual(r2.json()["source"], "cache")

    def test_force_build_bypasses_cache(self):
        client.get("/read/executive/briefing")
        r = client.get("/read/executive/briefing?build=true")
        self.assertEqual(r.json()["source"], "build")

    def test_ttl_present(self):
        r = client.get("/read/executive/regime")
        self.assertIn("ttl_seconds", r.json())

    def test_missing_data_fallback(self):
        with patch("modules.executive_intelligence.api._build_full", side_effect=Exception("no data")):
            r = client.get("/read/executive?build=true")
            self.assertFalse(r.json()["ok"])
            self.assertIn("error", r.json())


if __name__ == "__main__":
    unittest.main()
