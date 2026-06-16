"""
Tests for briefing_engine.py — PR5.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from modules.executive_intelligence.models import ExecutiveBriefing


def _mock_board():
    from modules.executive_intelligence.models import LeaderBoardEntry
    return [
        LeaderBoardEntry(symbol="NVDA", rank=1, direction="bullish", confidence=85, reliability=78, momentum_score=80, is_leader=True),
        LeaderBoardEntry(symbol="BTC", rank=2, direction="bullish", confidence=75, reliability=82, momentum_score=70, is_leader=True),
        LeaderBoardEntry(symbol="ETH", rank=3, direction="bullish", confidence=70, reliability=70, momentum_score=60, is_leader=True),
        LeaderBoardEntry(symbol="SPCX", rank=4, direction="bullish", confidence=75, reliability=60, momentum_score=55),
        LeaderBoardEntry(symbol="SOL", rank=5, direction="bullish", confidence=78, reliability=65, momentum_score=55),
        LeaderBoardEntry(symbol="XAU", rank=6, direction="neutral", confidence=55, reliability=72, momentum_score=40),
        LeaderBoardEntry(symbol="AVGO", rank=7, direction="neutral", confidence=50, reliability=55, momentum_score=35, is_laggard=True),
        LeaderBoardEntry(symbol="XRP", rank=8, direction="bearish", confidence=40, reliability=50, momentum_score=25, is_laggard=True),
        LeaderBoardEntry(symbol="MU", rank=9, direction="bearish", confidence=35, reliability=48, momentum_score=20, is_laggard=True),
    ]


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


def _mock_changes():
    from modules.executive_intelligence.models import DetectedChange
    return [
        DetectedChange(symbol="market", field="regime", previous="compression", current="risk_on", magnitude="major", description="Régime passé à risk_on."),
        DetectedChange(symbol="SPCX", field="direction", previous="neutral", current="bullish", magnitude="moderate", description="SPCX passe haussier."),
    ]


class TestBuildBriefing(unittest.TestCase):
    def setUp(self):
        self.patches = [
            patch("modules.executive_intelligence.briefing_engine.build_leaderboard", return_value=_mock_board()),
            patch("modules.executive_intelligence.briefing_engine.detect_regime", return_value=_mock_regime()),
            patch("modules.executive_intelligence.briefing_engine.compute_influences", return_value=[]),
            patch("modules.executive_intelligence.briefing_engine.detect_changes", return_value=_mock_changes()),
            patch("modules.executive_intelligence.briefing_engine.detect_leaders", return_value=[e for e in _mock_board() if e.is_leader]),
            patch("modules.executive_intelligence.briefing_engine.detect_laggards", return_value=[e for e in _mock_board() if e.is_laggard]),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()

    def test_build_briefing(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertIsInstance(brief, ExecutiveBriefing)
        self.assertEqual(brief.market_regime, "risk_on")
        self.assertEqual(brief.regime_confidence, 75)

    def test_leaders_populated(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertIn("NVDA", brief.leaders)
        self.assertIn("BTC", brief.leaders)

    def test_laggards_populated(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertIn("MU", brief.laggards)

    def test_summary_not_empty(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertGreater(len(brief.summary), 20)
        self.assertIn("Risk-On", brief.summary)

    def test_what_changed_not_empty(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertGreater(len(brief.what_changed), 10)

    def test_what_to_watch_not_empty(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertGreater(len(brief.what_to_watch), 10)

    def test_voice_one_liner_under_300(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertLessEqual(len(brief.voice_one_liner), 300)

    def test_voice_briefing_under_600(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertLessEqual(len(brief.voice_briefing), 600)

    def test_top_risks_populated(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertGreater(len(brief.top_risks), 0)

    def test_top_opportunities_populated(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertGreater(len(brief.top_opportunities), 0)

    def test_french_language(self):
        from modules.executive_intelligence.briefing_engine import build_briefing
        brief = build_briefing()
        self.assertNotIn("bullish", brief.summary.lower())
        self.assertNotIn("bearish", brief.summary.lower())
        self.assertNotIn("monitor_only", brief.summary.lower())


if __name__ == "__main__":
    unittest.main()
