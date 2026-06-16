"""
Tests for thesis_engine.py — PR5.

Covers:
- build_thesis(symbol) produces valid MarketThesis
- All 9 symbols work
- Confidence in range 0-100
- Probabilities total 100
- Action is always monitor_only
- archive save/load roundtrip
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from modules.market_thesis.archive import save, save_latest, load_latest, ensure_dirs, ARCHIVE_ROOT
from modules.market_thesis.models import MarketThesis, CANONICAL_BTC_THESIS
from modules.market_thesis.thesis_engine import build_thesis, build_all


class TestBuildThesis(unittest.TestCase):
    def test_build_btc(self):
        thesis = build_thesis("BTC")
        self.assertEqual(thesis.symbol, "BTC")
        self.assertEqual(thesis.metadata.contract, "market_thesis.v1")
        self.assertEqual(thesis.action.readiness, "monitor_only")
        self.assertGreaterEqual(thesis.confidence, 0)
        self.assertLessEqual(thesis.confidence, 100)
        self.assertEqual(
            thesis.probabilities.bull + thesis.probabilities.range + thesis.probabilities.bear,
            100,
        )

    def test_build_all_symbols(self):
        for sym in ["BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU"]:
            thesis = build_thesis(sym)
            self.assertEqual(thesis.symbol, sym)
            self.assertEqual(thesis.action.readiness, "monitor_only")
            self.assertIsInstance(thesis.context.narrative, str)
            self.assertIsInstance(thesis.technical.narrative, str)
            self.assertIsInstance(thesis.flow.narrative, str)
            self.assertIsInstance(thesis.news.narrative, str)
            self.assertIsInstance(thesis.action.narrative, str)
            self.assertIsInstance(thesis.action.voice_one_liner, str)
            self.assertGreater(len(thesis.sources), 0)
            self.assertGreaterEqual(thesis.freshness.source_count, 0)

    def test_confidence_in_range(self):
        for sym in ["BTC", "ETH", "SOL"]:
            thesis = build_thesis(sym)
            self.assertGreaterEqual(thesis.confidence, 0)
            self.assertLessEqual(thesis.confidence, 100)

    def test_all_narratives_non_empty(self):
        thesis = build_thesis("BTC")
        for attr in ["context", "technical", "flow", "news", "action"]:
            section = getattr(thesis, attr)
            self.assertTrue(len(section.narrative) > 0, f"{attr}.narrative empty")

    def test_one_liner_under_200(self):
        for sym in ["BTC", "ETH", "SPCX"]:
            thesis = build_thesis(sym)
            self.assertLessEqual(len(thesis.action.voice_one_liner), 200)

    def test_probabilities_total_100(self):
        for sym in ["BTC", "ETH", "SOL", "XRP", "XAU"]:
            thesis = build_thesis(sym)
            p = thesis.probabilities
            self.assertEqual(p.bull + p.range + p.bear, 100)


class TestBuildAll(unittest.TestCase):
    def test_returns_nine(self):
        theses = build_all()
        self.assertEqual(len(theses), 9)
        symbols = {t.symbol for t in theses}
        self.assertEqual(symbols, {"BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU"})

    def test_all_valid(self):
        for thesis in build_all():
            self.assertEqual(thesis.probabilities.bull + thesis.probabilities.range + thesis.probabilities.bear, 100)
            self.assertEqual(thesis.action.readiness, "monitor_only")
            self.assertGreater(len(thesis.sources), 0)


class TestArchive(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        # Patch ARCHIVE_ROOT
        self._orig_root = ARCHIVE_ROOT
        # We need to patch the module-level constant
        import modules.market_thesis.archive as arch_mod
        self._orig_root_val = arch_mod.ARCHIVE_ROOT
        arch_mod.ARCHIVE_ROOT = self.tmpdir

    def tearDown(self):
        import modules.market_thesis.archive as arch_mod
        arch_mod.ARCHIVE_ROOT = self._orig_root_val
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_save_and_load_latest(self):
        thesis = CANONICAL_BTC_THESIS
        path = save_latest(thesis)
        self.assertTrue(path.exists())

        loaded = load_latest("BTC")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.symbol, "BTC")
        self.assertEqual(loaded.confidence, 55)

    def test_save_to_history(self):
        thesis = CANONICAL_BTC_THESIS
        path = save(thesis)
        self.assertTrue(path.exists())
        self.assertIn("thesis_BTC", str(path))

    def test_load_latest_missing(self):
        loaded = load_latest("NOSYMBOL")
        self.assertIsNone(loaded)

    def test_load_history(self):
        from modules.market_thesis.archive import load_history
        thesis = CANONICAL_BTC_THESIS
        save(thesis)
        history = load_history("BTC", limit=10)
        self.assertGreaterEqual(len(history), 1)

    def test_load_history_empty(self):
        from modules.market_thesis.archive import load_history
        history = load_history("NOSYMBOL")
        self.assertEqual(history, [])

    def test_ensure_dirs(self):
        import modules.market_thesis.archive as arch_mod
        arch_mod.ARCHIVE_ROOT = self.tmpdir
        ensure_dirs()
        self.assertTrue((self.tmpdir / "by_symbol").exists())
        self.assertTrue((self.tmpdir / "history").exists())


if __name__ == "__main__":
    unittest.main()
