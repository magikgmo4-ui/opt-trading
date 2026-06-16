"""
Tests for narrative_memory.py — PR4.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from modules.executive_intelligence.narrative_memory import (
    detect_changes,
    detect_and_save,
    load_last_snapshot,
    save_snapshot,
    summarize_changes,
)
from modules.executive_intelligence.models import DetectedChange


class TestSnapshotSaveLoad(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        import modules.executive_intelligence.narrative_memory as nm
        self._orig = nm.MEMORY_ROOT
        nm.MEMORY_ROOT = self.tmpdir

    def tearDown(self):
        import modules.executive_intelligence.narrative_memory as nm
        nm.MEMORY_ROOT = self._orig
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_save_and_load(self):
        snap = {"regime": "risk_on", "confidence": 75, "assets": []}
        path = save_snapshot(snap)
        self.assertTrue(path.exists())

        loaded = load_last_snapshot()
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["regime"], "risk_on")

    def test_load_empty(self):
        loaded = load_last_snapshot()
        self.assertIsNone(loaded)


class TestDetectChanges(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        import modules.executive_intelligence.narrative_memory as nm
        self._orig = nm.MEMORY_ROOT
        nm.MEMORY_ROOT = self.tmpdir

    def tearDown(self):
        import modules.executive_intelligence.narrative_memory as nm
        nm.MEMORY_ROOT = self._orig
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    @staticmethod
    def _mock_board():
        """Return a mock leaderboard list of dicts."""
        return [
            {"symbol": "BTC", "direction": "bullish", "confidence": 80, "reliability": 82, "momentum_score": 70, "rank": 1, "is_leader": True},
            {"symbol": "ETH", "direction": "bullish", "confidence": 70, "reliability": 70, "momentum_score": 60, "rank": 2, "is_leader": True},
            {"symbol": "SOL", "direction": "bullish", "confidence": 65, "reliability": 65, "momentum_score": 55, "rank": 3, "is_leader": True},
            {"symbol": "XRP", "direction": "bearish", "confidence": 40, "reliability": 50, "momentum_score": 25, "rank": 7, "is_leader": False},
            {"symbol": "XAU", "direction": "neutral", "confidence": 55, "reliability": 72, "momentum_score": 40, "rank": 4, "is_leader": False},
            {"symbol": "SPCX", "direction": "bullish", "confidence": 60, "reliability": 60, "momentum_score": 55, "rank": 5, "is_leader": False},
            {"symbol": "NVDA", "direction": "bullish", "confidence": 85, "reliability": 78, "momentum_score": 80, "rank": 1, "is_leader": True},
            {"symbol": "AVGO", "direction": "neutral", "confidence": 50, "reliability": 55, "momentum_score": 35, "rank": 6, "is_leader": False},
            {"symbol": "MU", "direction": "bearish", "confidence": 35, "reliability": 48, "momentum_score": 20, "rank": 8, "is_leader": False},
        ]

    @staticmethod
    def _mock_regime():
        class MockRegime:
            regime = "risk_on"
            confidence = 75
            risk_score = 35
        return MockRegime()

    def _patch_engines(self):
        import modules.executive_intelligence.narrative_memory as nm
        self._board_patch = unittest.mock.patch.object(nm, "build_leaderboard", return_value=self._make_leaderboard())
        self._regime_patch = unittest.mock.patch.object(nm, "detect_regime", return_value=self._mock_regime())
        self._board_patch.start()
        self._regime_patch.start()

    def _unpatch_engines(self):
        self._board_patch.stop()
        self._regime_patch.stop()

    def _make_leaderboard(self):
        from modules.executive_intelligence.models import LeaderBoardEntry
        data = self._mock_board()
        return [LeaderBoardEntry(**d) for d in data]

    def test_first_capture_initialization(self):
        self._patch_engines()
        try:
            changes = detect_changes()
            self.assertEqual(len(changes), 1)
            self.assertEqual(changes[0].field, "initialization")
            self.assertEqual(changes[0].magnitude, "major")
        finally:
            self._unpatch_engines()

    def test_regime_change_detected(self):
        # First save a snapshot with different regime
        prev = {
            "captured_at": "2026-06-15T10:00:00",
            "regime": "compression",
            "regime_confidence": 50,
            "risk_score": 45,
            "assets": self._mock_board(),
            "bullish_count": 4,
            "bearish_count": 3,
        }
        save_snapshot(prev)

        self._patch_engines()
        try:
            changes = detect_changes()
            regime_changes = [c for c in changes if c.field == "regime"]
            self.assertGreater(len(regime_changes), 0)
            self.assertEqual(regime_changes[0].previous, "compression")
            self.assertEqual(regime_changes[0].magnitude, "major")
        finally:
            self._unpatch_engines()

    def test_direction_change_detected(self):
        # Previous: XRP bullish, current: XRP bearish
        prev_assets = self._mock_board()
        for a in prev_assets:
            if a["symbol"] == "XRP":
                a["direction"] = "bullish"

        prev = {
            "captured_at": "2026-06-15T10:00:00",
            "regime": "risk_on",
            "regime_confidence": 75,
            "risk_score": 35,
            "assets": prev_assets,
            "bullish_count": 5,
            "bearish_count": 2,
        }
        save_snapshot(prev)

        self._patch_engines()
        try:
            changes = detect_changes()
            dir_changes = [c for c in changes if c.field == "direction" and c.symbol == "XRP"]
            self.assertGreater(len(dir_changes), 0)
            self.assertEqual(dir_changes[0].previous, "bullish")
            self.assertEqual(dir_changes[0].current, "bearish")
        finally:
            self._unpatch_engines()

    def test_no_changes_when_same(self):
        # Save identical snapshot
        prev = {
            "captured_at": "2026-06-15T10:00:00",
            "regime": "risk_on",
            "regime_confidence": 75,
            "risk_score": 35,
            "assets": self._mock_board(),
            "bullish_count": 5,
            "bearish_count": 2,
        }
        save_snapshot(prev)

        self._patch_engines()
        try:
            changes = detect_changes()
            # Should have no or few minor changes
            non_init = [c for c in changes if c.field != "initialization"]
            # Direction/regime should be unchanged
            regime_changes = [c for c in non_init if c.field == "regime"]
            self.assertEqual(len(regime_changes), 0)
        finally:
            self._unpatch_engines()

    def test_summarize_changes(self):
        changes = [
            DetectedChange(symbol="market", field="regime", previous="compression", current="risk_on", magnitude="major", description="Régime passé à risk_on."),
            DetectedChange(symbol="BTC", field="direction", previous="neutral", current="bullish", magnitude="moderate", description="BTC passe haussier."),
            DetectedChange(symbol="XRP", field="confidence", previous="40", current="55", magnitude="minor", description="Confiance XRP augmentée."),
        ]
        summary = summarize_changes(changes)
        self.assertIn("majeur", summary.lower())
        self.assertIn("risk_on", summary.lower())

    def test_detect_and_save(self):
        self._patch_engines()
        try:
            changes, summary = detect_and_save()
            self.assertIsInstance(changes, list)
            self.assertIsInstance(summary, str)
            self.assertTrue(len(summary) > 0)
        finally:
            self._unpatch_engines()


if __name__ == "__main__":
    unittest.main()
