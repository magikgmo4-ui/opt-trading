"""
Tests for cross_asset_engine.py — PR2.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from modules.executive_intelligence.cross_asset_engine import (
    DEPENDENCY_MAP,
    INVERSE_PAIRS,
    SECTORS,
    build_leaderboard,
    compute_all,
    compute_influences,
    detect_laggards,
    detect_leaders,
)


def _mock_thesis(symbol: str, direction: str = "neutral", confidence: int = 50,
                 prob_bull: int = 33, prob_bear: int = 33, oi_change: float = 0.0) -> dict:
    return {
        "symbol": symbol,
        "confidence": confidence,
        "action": {"direction": direction},
        "probabilities": {"bull": prob_bull, "range": 100 - prob_bull - prob_bear, "bear": prob_bear},
        "flow": {"oi_change_24h_pct": oi_change},
    }


def _mock_reliability(symbol: str) -> dict:
    """Mock reliability: premium assets get high scores."""
    scores = {"BTC": 82, "ETH": 70, "SOL": 65, "XRP": 50, "XAU": 72, "SPCX": 60, "NVDA": 78, "AVGO": 55, "MU": 48}
    return {"reliability": scores.get(symbol, 50), "sample_size": 100}


class TestCrossAssetEngine(unittest.TestCase):
    def setUp(self):
        self._patches = [
            patch("modules.executive_intelligence.cross_asset_engine._load_thesis", side_effect=self._load_thesis),
            patch("modules.executive_intelligence.cross_asset_engine._load_reliability", side_effect=_mock_reliability),
        ]
        for p in self._patches:
            p.start()

    def tearDown(self):
        for p in self._patches:
            p.stop()

    def _load_thesis(self, symbol: str) -> dict:
        """Simulate realistic thesis directions."""
        configs = {
            "BTC": ("bullish", 75, 60, 20),
            "ETH": ("bullish", 68, 55, 25),
            "SOL": ("bullish", 62, 50, 30),
            "XRP": ("bearish", 45, 30, 45),
            "XAU": ("bullish", 72, 58, 22),
            "SPCX": ("bullish", 65, 55, 25),
            "NVDA": ("bullish", 80, 65, 15),
            "AVGO": ("neutral", 50, 35, 35),
            "MU": ("bearish", 38, 25, 50),
        }
        c = configs.get(symbol, ("neutral", 50, 33, 33))
        return _mock_thesis(symbol, direction=c[0], confidence=c[1], prob_bull=c[2], prob_bear=c[3])

    def test_dependency_graph_structure(self):
        self.assertIn("BTC", DEPENDENCY_MAP)
        self.assertIn("ETH", DEPENDENCY_MAP["BTC"])
        self.assertIn("SOL", DEPENDENCY_MAP["BTC"])
        self.assertIn("XRP", DEPENDENCY_MAP["BTC"])
        self.assertIn("DXY", DEPENDENCY_MAP)
        self.assertIn("XAU", DEPENDENCY_MAP["DXY"])

    def test_inverse_pairs(self):
        self.assertIn(("DXY", "XAU"), INVERSE_PAIRS)

    def test_sectors(self):
        self.assertEqual(SECTORS["BTC"], "crypto")
        self.assertEqual(SECTORS["NVDA"], "semiconductor")
        self.assertEqual(SECTORS["XAU"], "commodity")

    def test_compute_influences(self):
        influences = compute_influences()
        self.assertGreater(len(influences), 0)
        for inf in influences:
            self.assertIsInstance(inf.source, str)
            self.assertIsInstance(inf.target, str)
            self.assertGreaterEqual(inf.influence_score, 0)
            self.assertLessEqual(inf.influence_score, 100)
            self.assertGreaterEqual(inf.correlation, -1.0)
            self.assertLessEqual(inf.correlation, 1.0)

    def test_btc_crypto_influence(self):
        influences = compute_influences()
        btc_inf = [i for i in influences if i.source == "BTC"]
        self.assertGreater(len(btc_inf), 0)

    def test_dxy_gold_inverse(self):
        influences = compute_influences()
        dxy_gold = [i for i in influences if i.source == "DXY" and i.target == "XAU"]
        if dxy_gold:
            self.assertEqual(dxy_gold[0].direction, "opposite")

    def test_build_leaderboard(self):
        board = build_leaderboard()
        self.assertGreaterEqual(len(board), 9)
        ranks = [e.rank for e in board]
        self.assertEqual(ranks, sorted(ranks))

    def test_leaderboard_sorted(self):
        board = build_leaderboard()
        scores = [e.confidence + e.reliability + e.momentum_score for e in board]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_detect_leaders(self):
        leaders = detect_leaders()
        self.assertGreater(len(leaders), 0)
        for l in leaders:
            self.assertTrue(l.is_leader)

    def test_detect_laggards(self):
        laggards = detect_laggards()
        for l in laggards:
            self.assertTrue(l.is_laggard)

    def test_compute_all(self):
        result = compute_all()
        self.assertIn("influences", result)
        self.assertIn("leaders", result)
        self.assertGreater(result["total_assets"], 0)

    def test_leaderboard_has_nvda_high(self):
        board = build_leaderboard()
        nvda = next((e for e in board if e.symbol == "NVDA"), None)
        self.assertIsNotNone(nvda)
        # NVDA has bullish + 80 conf + 78 reliability
        self.assertGreaterEqual(nvda.confidence, 70)

    def test_momentum_score_bounded(self):
        board = build_leaderboard()
        for e in board:
            self.assertGreaterEqual(e.momentum_score, 0)
            self.assertLessEqual(e.momentum_score, 100)

    def test_all_symbols_present(self):
        board = build_leaderboard()
        symbols = {e.symbol for e in board}
        self.assertTrue(symbols.issuperset({"BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU"}))

    def test_rank_increments(self):
        board = build_leaderboard()
        for i, e in enumerate(board):
            self.assertEqual(e.rank, i + 1)


if __name__ == "__main__":
    unittest.main()
