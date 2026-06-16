"""
Tests for regime_engine.py — PR3.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from modules.executive_intelligence.models import LeaderBoardEntry
from modules.executive_intelligence.regime_engine import (
    _classify_regime,
    _compute_risk_score,
    _gather_evidence,
    detect_regime,
)


def _make_board(bullish_count: int, bearish_count: int,
                leader_conf: int = 70, leader_momentum: int = 60) -> list:
    """Build a mock leaderboard."""
    board = []
    for i in range(bullish_count):
        board.append(LeaderBoardEntry(
            symbol=f"BULL{i}", rank=i + 1, direction="bullish",
            confidence=leader_conf, reliability=70, momentum_score=leader_momentum,
            is_leader=(i < 3),
        ))
    for i in range(bearish_count):
        board.append(LeaderBoardEntry(
            symbol=f"BEAR{i}", rank=bullish_count + i + 1, direction="bearish",
            confidence=50 - i * 5, reliability=50, momentum_score=40 - i * 5,
            is_laggard=(bearish_count - i <= 3),
        ))
    return board


class TestRegimeClassification(unittest.TestCase):
    def test_risk_on(self):
        board = _make_board(7, 1, leader_conf=75, leader_momentum=65)
        evidence = _gather_evidence(board, [])
        regime, conf = _classify_regime(board, evidence)
        self.assertEqual(regime, "risk_on")
        self.assertGreater(conf, 60)

    def test_risk_off(self):
        board = _make_board(1, 6, leader_conf=40, leader_momentum=20)
        evidence = _gather_evidence(board, [])
        regime, conf = _classify_regime(board, evidence)
        self.assertEqual(regime, "risk_off")

    def test_panic(self):
        board = _make_board(0, 8, leader_conf=20, leader_momentum=10)
        evidence = _gather_evidence(board, [])
        regime, conf = _classify_regime(board, evidence)
        self.assertEqual(regime, "panic")
        self.assertGreater(conf, 70)

    def test_recovery(self):
        board = _make_board(5, 1, leader_conf=60, leader_momentum=50)
        evidence = _gather_evidence(board, [])
        regime, conf = _classify_regime(board, evidence)
        self.assertIn(regime, ("recovery", "expansion", "risk_on"))

    def test_expansion(self):
        board = _make_board(6, 2, leader_conf=70, leader_momentum=65)
        evidence = _gather_evidence(board, [])
        regime, conf = _classify_regime(board, evidence)
        self.assertIn(regime, ("expansion", "risk_on"))

    def test_compression(self):
        board = _make_board(4, 4, leader_conf=55, leader_momentum=35)
        evidence = _gather_evidence(board, [])
        regime, conf = _classify_regime(board, evidence)
        self.assertIn(regime, ("compression", "distribution", "accumulation"))

    def test_unknown_empty(self):
        board = []
        evidence = RegimeEvidence = type("E", (), {})()  # empty
        from modules.executive_intelligence.models import RegimeEvidence
        evidence = RegimeEvidence()
        regime, conf = _classify_regime(board, evidence)
        self.assertEqual(regime, "unknown")
        self.assertEqual(conf, 0)

    def test_risk_score_panic_high(self):
        board = _make_board(0, 8, leader_conf=20, leader_momentum=10)
        evidence = _gather_evidence(board, [])
        score = _compute_risk_score(board, evidence, "panic")
        self.assertGreater(score, 60)

    def test_risk_score_risk_on_low(self):
        board = _make_board(7, 1, leader_conf=75, leader_momentum=65)
        evidence = _gather_evidence(board, [])
        score = _compute_risk_score(board, evidence, "risk_on")
        self.assertLess(score, 50)

    def test_risk_score_bounded(self):
        board = _make_board(5, 3)
        evidence = _gather_evidence(board, [])
        for regime in ["risk_on", "risk_off", "panic", "expansion"]:
            score = _compute_risk_score(board, evidence, regime)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)


class TestDetectRegimeIntegration(unittest.TestCase):
    @patch("modules.executive_intelligence.regime_engine.build_leaderboard")
    @patch("modules.executive_intelligence.regime_engine.compute_influences")
    def test_detect_regime_returns_valid(self, mock_inf, mock_board):
        mock_board.return_value = _make_board(7, 1, leader_conf=75, leader_momentum=65)
        mock_inf.return_value = []

        regime = detect_regime()
        from modules.executive_intelligence.models import MarketRegime
        self.assertIsInstance(regime, MarketRegime)
        self.assertIn(regime.regime, ("risk_on", "expansion"))
        self.assertGreaterEqual(regime.confidence, 0)
        self.assertLessEqual(regime.confidence, 100)
        self.assertGreater(len(regime.narrative), 0)

    @patch("modules.executive_intelligence.regime_engine.build_leaderboard")
    @patch("modules.executive_intelligence.regime_engine.compute_influences")
    def test_detect_regime_panic(self, mock_inf, mock_board):
        mock_board.return_value = _make_board(0, 9, leader_conf=15, leader_momentum=5)
        mock_inf.return_value = []

        regime = detect_regime()
        self.assertEqual(regime.regime, "panic")

    @patch("modules.executive_intelligence.regime_engine.build_leaderboard")
    @patch("modules.executive_intelligence.regime_engine.compute_influences")
    def test_detect_regime_compression(self, mock_inf, mock_board):
        mock_board.return_value = _make_board(4, 3, leader_conf=50, leader_momentum=35)
        mock_inf.return_value = []

        regime = detect_regime()
        self.assertIn(regime.regime, ("compression", "distribution", "accumulation"))

    def test_narrative_french(self):
        board = _make_board(7, 1, leader_conf=75, leader_momentum=65)
        evidence = _gather_evidence(board, [])
        from modules.executive_intelligence.regime_engine import _build_narrative
        narrative = _build_narrative("risk_on", 75, evidence, board)
        self.assertIn("Risk-On", narrative)
        self.assertIn("haussier", narrative.lower())

    def test_transition_prediction(self):
        from modules.executive_intelligence.regime_engine import _predict_transition
        board = _make_board(5, 2)
        evidence = _gather_evidence(board, [])
        next_r, prob = _predict_transition("risk_on", board, evidence)
        self.assertIsNotNone(next_r)
        self.assertGreaterEqual(prob, 0)
        self.assertLessEqual(prob, 100)


if __name__ == "__main__":
    unittest.main()
