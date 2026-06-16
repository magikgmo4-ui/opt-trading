"""
Tests for DeskPro executive reader + routes — PR7.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from modules.desk_pro.service.executive_reader import (
    get_executive,
    get_executive_leaders,
    get_executive_regime,
    get_executive_risks,
)

# Mock data
MOCK_BRIEF = {
    "briefing_id": "b1", "generated_at": "2026-06-15T12:00:00Z",
    "market_regime": "risk_on", "regime_confidence": 75, "overall_confidence": 72,
    "leaders": ["NVDA", "BTC", "SPCX"], "laggards": ["MU", "XRP"],
    "summary": "Régime Risk-On. Leaders NVDA, BTC.",
    "what_changed": "Régime passé à risk_on.", "what_to_watch": "Surveiller dollar.",
    "top_risks": ["Crowding haussier"], "top_opportunities": ["BTC momentum"],
    "voice_one_liner": "Marché Risk-On.", "voice_briefing": "Régime Risk-On.",
}

MOCK_REGIME = {
    "regime": "risk_on", "confidence": 75, "risk_score": 35,
    "narrative": "Régime Risk-On.", "dxy_trend": "bearish",
    "vix_level": "low", "spy_trend": "bullish", "fear_greed": 65,
    "bullish_count": 6, "bearish_count": 2,
}

MOCK_LEADERS = {
    "leaders": [{"symbol": "NVDA", "rank": 1, "direction": "bullish", "confidence": 85, "momentum": 80}],
    "laggards": [{"symbol": "MU", "rank": 9, "direction": "bearish", "confidence": 30, "momentum": 20}],
    "full_board": [],
    "cross_asset": ["BTC→ETH: same (80)"],
}

MOCK_RISKS = {
    "top_risks": ["Crowding haussier"],
    "regime_risk": 35,
    "regime_risk_label": "low",
}


class TestExecutiveReader(unittest.TestCase):
    @patch("modules.executive_intelligence.briefing_engine.build_briefing")
    def test_get_executive(self, mock_brief):
        from modules.executive_intelligence.models import ExecutiveBriefing
        from datetime import datetime, timezone
        mock_brief.return_value = ExecutiveBriefing(
            briefing_id="b1", generated_at=datetime.now(timezone.utc),
            market_regime="risk_on", regime_confidence=75, overall_confidence=72,
            leaders=["NVDA", "BTC"], laggards=["MU"],
            summary="Régime Risk-On.", what_changed="Changement.", what_to_watch="Surveiller.",
            top_risks=["Crowding"], top_opportunities=["BTC"],
            voice_one_liner="Marché.", voice_briefing="Briefing.",
        )
        data = get_executive()
        self.assertIsNotNone(data)
        self.assertEqual(data["market_regime"], "risk_on")

    @patch("modules.executive_intelligence.regime_engine.detect_regime")
    def test_get_regime(self, mock_r):
        from modules.executive_intelligence.models import MarketRegime, RegimeEvidence
        mock_r.return_value = MarketRegime(
            regime="risk_on", confidence=75, risk_score=35,
            evidence=RegimeEvidence(dxy_trend="bearish", vix_level="low", spy_trend="bullish",
                                     fear_greed=65, asset_count_bullish=6, asset_count_bearish=2),
            narrative="Régime Risk-On.",
        )
        data = get_executive_regime()
        self.assertIsNotNone(data)
        self.assertEqual(data["regime"], "risk_on")

    @patch("modules.executive_intelligence.cross_asset_engine.compute_influences")
    @patch("modules.executive_intelligence.cross_asset_engine.build_leaderboard")
    def test_get_leaders(self, mock_board, mock_inf):
        from modules.executive_intelligence.models import LeaderBoardEntry
        mock_board.return_value = [
            LeaderBoardEntry(symbol="NVDA", rank=1, direction="bullish", confidence=85, reliability=78, momentum_score=80, is_leader=True),
        ]
        mock_inf.return_value = []
        data = get_executive_leaders()
        self.assertIsNotNone(data)
        self.assertGreater(len(data["leaders"]), 0)

    @patch("modules.executive_intelligence.regime_engine.detect_regime")
    @patch("modules.executive_intelligence.briefing_engine.build_briefing")
    def test_get_risks(self, mock_brief, mock_r):
        from modules.executive_intelligence.models import ExecutiveBriefing, MarketRegime, RegimeEvidence
        from datetime import datetime, timezone
        mock_brief.return_value = ExecutiveBriefing(
            briefing_id="b1", generated_at=datetime.now(timezone.utc),
            market_regime="risk_on", regime_confidence=75, overall_confidence=72,
            leaders=[], laggards=[], summary=".", what_changed=".", what_to_watch=".",
            top_risks=["Crowding"], top_opportunities=[], voice_one_liner=".", voice_briefing=".",
        )
        mock_r.return_value = MarketRegime(
            regime="risk_on", confidence=75, risk_score=35,
            evidence=RegimeEvidence(asset_count_bullish=6, asset_count_bearish=2),
        )
        data = get_executive_risks()
        self.assertIsNotNone(data)
        self.assertIn("top_risks", data)

    @patch("modules.executive_intelligence.briefing_engine.build_briefing")
    def test_get_executive_error_fallback(self, mock_b):
        mock_b.side_effect = Exception("boom")
        self.assertIsNone(get_executive())


class TestExecutiveRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from modules.desk_pro.api.routes import router
        app = FastAPI()
        app.include_router(router)
        cls.client = TestClient(app)

    @patch("modules.desk_pro.api.routes.get_executive")
    def test_executive_json(self, mock):
        mock.return_value = MOCK_BRIEF
        r = self.client.get("/desk/executive")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["market_regime"], "risk_on")

    @patch("modules.desk_pro.api.routes.get_executive_regime")
    def test_executive_regime(self, mock):
        mock.return_value = MOCK_REGIME
        r = self.client.get("/desk/executive/regime")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["regime"], "risk_on")

    @patch("modules.desk_pro.api.routes.get_executive_leaders")
    def test_executive_leaders(self, mock):
        mock.return_value = MOCK_LEADERS
        r = self.client.get("/desk/executive/leaders")
        self.assertEqual(r.status_code, 200)

    @patch("modules.desk_pro.api.routes.get_executive_risks")
    def test_executive_risks(self, mock):
        mock.return_value = MOCK_RISKS
        r = self.client.get("/desk/executive/risks")
        self.assertEqual(r.status_code, 200)

    @patch("modules.desk_pro.api.routes.get_executive")
    def test_executive_ui(self, mock):
        mock.return_value = MOCK_BRIEF
        r = self.client.get("/desk/executive/ui")
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn("Executive Center", html)
        self.assertIn("risk_on", html.lower())

    @patch("modules.desk_pro.api.routes.get_executive")
    def test_ui_dark_mode(self, mock):
        mock.return_value = MOCK_BRIEF
        r = self.client.get("/desk/executive/ui")
        self.assertIn("background:#111", r.text)
        self.assertIn("color:#e0e0e0", r.text)

    @patch("modules.desk_pro.api.routes.get_executive")
    def test_ui_mobile_viewport(self, mock):
        mock.return_value = MOCK_BRIEF
        r = self.client.get("/desk/executive/ui")
        self.assertIn("viewport", r.text)
        self.assertIn("max-width:700px", r.text)

    @patch("modules.desk_pro.api.routes.get_executive")
    def test_ui_cards_present(self, mock):
        mock.return_value = MOCK_BRIEF
        r = self.client.get("/desk/executive/ui")
        html = r.text
        for card in ["Leaders", "Laggards", "Top Risks", "Top Opportunities", "What Changed", "What To Watch"]:
            self.assertIn(card, html, f"Missing card: {card}")

    @patch("modules.desk_pro.api.routes.get_executive")
    def test_executive_unavailable(self, mock):
        mock.return_value = None
        r = self.client.get("/desk/executive")
        self.assertEqual(r.status_code, 503)


if __name__ == "__main__":
    unittest.main()
