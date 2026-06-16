"""Tests for morning_briefing template — PR10."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from modules.executive_intelligence.models import LeaderBoardEntry, DetectedChange


class TestMorningBriefing(unittest.TestCase):
    def setUp(self):
        self.patches = [
            patch("modules.desk_pro.service.executive_reader.get_executive", return_value={
                "market_regime": "risk_on", "regime_confidence": 72,
                "leaders": ["NVDA", "BTC", "SPCX"], "laggards": ["MU"],
                "top_risks": ["Crowding haussier", "Dollar fort"],
                "top_opportunities": ["BTC momentum", "NVDA IA"],
            }),
            patch("modules.desk_pro.service.executive_reader.get_executive_regime", return_value={
                "regime": "risk_on", "confidence": 72, "risk_score": 35,
            }),
            patch("modules.desk_pro.service.executive_reader.get_executive_leaders", return_value={
                "leaders": [{"symbol": "NVDA"}], "laggards": [{"symbol": "MU"}],
            }),
            patch("modules.desk_pro.service.executive_reader.get_executive_risks", return_value={
                "top_risks": ["Crowding"],
            }),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()

    def _make_board(self):
        return [
            LeaderBoardEntry(symbol="BTC", rank=1, direction="bullish", confidence=75, reliability=82, momentum_score=70, is_leader=True),
            LeaderBoardEntry(symbol="NVDA", rank=2, direction="bullish", confidence=80, reliability=78, momentum_score=85, is_leader=True),
            LeaderBoardEntry(symbol="ETH", rank=3, direction="bullish", confidence=68, reliability=70, momentum_score=60),
            LeaderBoardEntry(symbol="SOL", rank=4, direction="bullish", confidence=62, reliability=65, momentum_score=55),
            LeaderBoardEntry(symbol="SPCX", rank=5, direction="bullish", confidence=65, reliability=60, momentum_score=55, is_leader=True),
            LeaderBoardEntry(symbol="XAU", rank=6, direction="neutral", confidence=55, reliability=72, momentum_score=40),
            LeaderBoardEntry(symbol="XRP", rank=7, direction="bearish", confidence=40, reliability=50, momentum_score=25),
            LeaderBoardEntry(symbol="MU", rank=8, direction="bearish", confidence=35, reliability=48, momentum_score=20, is_laggard=True),
        ]

    def _make_setups(self):
        return {
            "cards": [
                {"symbol": "SPCX", "setup": "VWAP Reclaim", "grade": "A", "probability": 64, "bias": "Long", "entry_zone": "170-173", "stop_loss": 168},
                {"symbol": "BTC", "setup": "Pullback VWAP", "grade": "A-", "probability": 60, "bias": "Long", "entry_zone": "65.8k-66.1k", "stop_loss": 65250},
            ],
            "market_summary": {"active_setups": 2},
        }

    @patch("modules.executive_intelligence.cross_asset_engine.build_leaderboard")
    @patch("modules.executive_intelligence.narrative_memory.detect_changes")
    @patch("modules.executive_intelligence.templates.setup_card.render_setup_cards")
    def test_render_briefing(self, mock_setups, mock_changes, mock_board):
        from modules.executive_intelligence.templates.morning_briefing import render_morning_briefing

        mock_setups.return_value = self._make_setups()
        mock_changes.return_value = [
            DetectedChange(field="regime", previous="compression", current="risk_on", magnitude="major", description="Régime passé à risk_on."),
        ]
        mock_board.return_value = self._make_board()

        result = render_morning_briefing()
        self.assertIn("spoken_text", result)
        self.assertIn("display_text", result)
        self.assertIn("cards", result)

    @patch("modules.executive_intelligence.cross_asset_engine.build_leaderboard")
    @patch("modules.executive_intelligence.narrative_memory.detect_changes")
    @patch("modules.executive_intelligence.templates.setup_card.render_setup_cards")
    def test_spoken_no_json(self, mock_setups, mock_changes, mock_board):
        from modules.executive_intelligence.templates.morning_briefing import render_morning_briefing

        mock_setups.return_value = {"cards": [], "market_summary": {}}
        mock_changes.return_value = []
        mock_board.return_value = self._make_board()

        result = render_morning_briefing()
        self.assertNotIn("{", result["spoken_text"])
        self.assertNotIn("}", result["spoken_text"])

    @patch("modules.executive_intelligence.cross_asset_engine.build_leaderboard")
    @patch("modules.executive_intelligence.narrative_memory.detect_changes")
    @patch("modules.executive_intelligence.templates.setup_card.render_setup_cards")
    def test_display_has_sections(self, mock_setups, mock_changes, mock_board):
        from modules.executive_intelligence.templates.morning_briefing import render_morning_briefing

        mock_setups.return_value = {"cards": [], "market_summary": {}}
        mock_changes.return_value = []
        mock_board.return_value = self._make_board()

        result = render_morning_briefing()
        display = result["display_text"]
        for section in ["État du marché", "Setups actifs", "Risques principaux", "Ce qui a changé"]:
            self.assertIn(section, display, f"Missing: {section}")

    @patch("modules.executive_intelligence.cross_asset_engine.build_leaderboard")
    @patch("modules.executive_intelligence.narrative_memory.detect_changes")
    @patch("modules.executive_intelligence.templates.setup_card.render_setup_cards")
    def test_monitor_only(self, mock_setups, mock_changes, mock_board):
        from modules.executive_intelligence.templates.morning_briefing import render_morning_briefing

        mock_setups.return_value = {"cards": [], "market_summary": {}}
        mock_changes.return_value = []
        mock_board.return_value = self._make_board()

        result = render_morning_briefing()
        self.assertIn("Surveillance uniquement", result["spoken_text"])
        self.assertIn("Aucun ordre automatique", result["spoken_text"])

    @patch("modules.executive_intelligence.cross_asset_engine.build_leaderboard")
    @patch("modules.executive_intelligence.narrative_memory.detect_changes")
    @patch("modules.executive_intelligence.templates.setup_card.render_setup_cards")
    def test_cards_have_key_fields(self, mock_setups, mock_changes, mock_board):
        from modules.executive_intelligence.templates.morning_briefing import render_morning_briefing

        mock_setups.return_value = {"cards": [], "market_summary": {}}
        mock_changes.return_value = []
        mock_board.return_value = self._make_board()

        result = render_morning_briefing()
        card_labels = {c["label"] for c in result["cards"]}
        for label in ["Régime", "Confiance", "Risque", "Setups actifs", "Mode"]:
            self.assertIn(label, card_labels)


if __name__ == "__main__":
    unittest.main()
