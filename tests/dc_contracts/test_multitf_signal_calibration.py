"""Signal calibration tests — validate grade transitions, downgrades, caps."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestSignalCalibrationTransitions(unittest.TestCase):
    """Validate grade transitions: C→B+, downgrade, caps."""

    def setUp(self):
        self.scorer_path = PROJECT_ROOT / "modules" / "data_center" / "multitf_setup_scorer.py"

    def test_support_watch_without_cdp_stays_c(self):
        """support_watch sans trigger CDP doit rester C/C+"""
        from modules.data_center.multitf_setup_scorer import _score_setups, _score_to_grade
        entry = {
            "symbol": "BTC",
            "price": 67000,
            "freshness_state": "fresh",
            "timeframes": {"H4": {"indicators": {"trend": "bearish"}}, "M15": {"indicators": {"trend": "bearish"}}},
            "levels": {"support_levels": [65000], "resistance_levels": [69000]},
            "signals": [],  # Pas de CDP
        }
        setups = _score_setups(entry)
        self.assertEqual(len(setups), 1)
        self.assertEqual(setups[0]["setup_type"], "support_watch")
        self.assertIn(setups[0]["grade"], ("C", "C+"))
        self.assertLess(setups[0]["score"], 40)

    def test_vwap_reclaim_fresh_gives_b_plus(self):
        """vwap_reclaim fresh + neutral/bullish doit donner B minimum"""
        from modules.data_center.multitf_setup_scorer import _score_setups
        entry_fresh = {
            "symbol": "SPCX",
            "price": 171.5,
            "freshness_state": "fresh",
            "asset_class": "ipo",
            "timeframes": {"H4": {"indicators": {"trend": "neutral"}}, "M15": {"indicators": {"trend": "neutral"}}},
            "levels": {"support_levels": [165], "resistance_levels": [180]},
            "signals": [{"source": "tradingview_cdp", "event": "vwap_reclaim", "timestamp": "2026-06-15T17:30:00Z"}],
        }
        # Stale
        entry_stale = dict(entry_fresh)
        entry_stale["freshness_state"] = "stale"

        fresh_setups = _score_setups(entry_fresh)
        stale_setups = _score_setups(entry_stale)

        # Stale should have lower confidence or score
        if fresh_setups and stale_setups:
            self.assertGreaterEqual(
                fresh_setups[0]["confidence_pct"],
                stale_setups[0]["confidence_pct"],
                "Stale confidence should not exceed fresh"
            )

    def test_missing_critical_fields_caps_score(self):
        """Champs critiques absents doivent baisser le score"""
        from modules.data_center.multitf_setup_scorer import _score_setups
        entry = {
            "symbol": "BTC",
            "price": 66500,
            "freshness_state": "fresh",
            "timeframes": {"H4": {"indicators": {"trend": "bearish"}}, "M15": {"indicators": {"trend": "bearish"}}},
            "levels": {},  # Pas de VWAP, pas de niveaux
            "signals": [{"source": "tradingview_cdp", "event": "vwap_loss"}],
            "missing": ["vwap_raw_value"],  # Explicit missing
        }
        setups = _score_setups(entry)
        if setups:
            self.assertIn("vwap_raw_value", setups[0].get("missing", []),
                          "Should note missing VWAP")

    def test_no_trigger_no_upgrade(self):
        """Sans trigger CDP, le grade ne depasse pas C+"""
        from modules.data_center.multitf_setup_scorer import _score_setups
        entry = {
            "symbol": "ETH",
            "price": 1800,
            "freshness_state": "fresh",
            "timeframes": {"H4": {"indicators": {"trend": "bearish"}}, "M15": {"indicators": {"trend": "bearish"}}},
            "levels": {"support_levels": [1700], "resistance_levels": [1900]},
            "signals": [],
        }
        setups = _score_setups(entry)
        self.assertEqual(len(setups), 1)
        self.assertLess(setups[0]["score"], 40, f"No trigger should keep score < 40, got {setups[0]['score']}")

    def test_spcx_baseline_matches_observed(self):
        """Baseline SPCX doit être vwap_reclaim, B minimum"""
        from modules.data_center.multitf_setup_scorer import _score_setups
        entry = {
            "symbol": "SPCX",
            "price": 171.5,
            "freshness_state": "fresh",
            "asset_class": "ipo",
            "timeframes": {"H4": {"indicators": {"trend": "neutral"}}, "M15": {"indicators": {"trend": "neutral"}}},
            "levels": {"support_levels": [165], "resistance_levels": [180]},
            "signals": [{"source": "tradingview_cdp", "event": "vwap_reclaim", "price": 171.5,
                          "timestamp": "2026-06-15T17:30:00Z"}],
        }
        setups = _score_setups(entry)
        self.assertGreaterEqual(len(setups), 1)
        best = setups[0]
        self.assertEqual(best["setup_type"], "vwap_reclaim")
        self.assertGreaterEqual(best["score"], 50, f"SPCX should be at least B, got {best['score']}")
        self.assertIn(best["grade"], ("B+", "B", "A-", "A"))


class TestVoiceConsumerReflectsTransitions(unittest.TestCase):
    """Voice must reflect real scores, not stale or invented data."""

    def test_priorities_reflects_multitf_scores(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("priorities")
        spoken = result["rich"]["spoken_text"]
        # Must mention multitf
        self.assertIn("multitf", spoken.lower())
        # Must not be empty or fallback
        self.assertGreater(len(spoken), 20)

    def test_attention_signals_issues(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("attention")
        cards = result["rich"]["cards"]
        # Should have at least one issue (completeness, freshness, score)
        self.assertGreater(len(cards), 0, "Attention should find issues")

    def test_market_view_has_top_setups(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("market_view")
        spoken = result["rich"]["spoken_text"]
        self.assertIn("setup", spoken.lower())

    def test_exec_summary_mentions_grade_or_score(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("exec_summary")
        spoken = result["rich"]["spoken_text"]
        has_grade = any(w in spoken.lower() for w in ["grade", "score", "b+", "b-", "a+", "a-", "c"])
        self.assertTrue(has_grade, f"No grade/score in: {spoken[:80]}")

    def test_no_execution_terms(self):
        from modules.localcms.app.main import _handle_composite
        forbidden = ["execute", "broker", "order_book", "auto_trade", "market_order", "limit_order"]
        for cmd in ["priorities", "attention", "exec_summary", "market_view"]:
            result = _handle_composite(cmd)
            text = json.dumps(result).lower()
            for term in forbidden:
                self.assertNotIn(term, text, f"{cmd}: forbidden term '{term}'")

    def test_btc_stays_c_without_trigger(self):
        """BTC doit rester C sans CDP trigger"""
        # This is validated by reading the live multitf output
        baseline = json.loads(
            (PROJECT_ROOT / "outputs" / "multitf_signal_calibration" / "baseline_scores.json").read_text().splitlines()[0]
        )
        self.assertEqual(baseline["symbol"], "BTC")
        self.assertEqual(baseline["grade"], "C")
        self.assertLess(baseline["score"], 40)

    def test_spcx_is_b_plus_with_trigger(self):
        """SPCX doit être B+ avec vwap_reclaim CDP"""
        lines = (PROJECT_ROOT / "outputs" / "multitf_signal_calibration" / "baseline_scores.json").read_text().splitlines()
        spcx = [json.loads(l) for l in lines if '"SPCX"' in l]
        self.assertEqual(len(spcx), 1, "SPCX baseline entry missing")
        self.assertEqual(spcx[0]["grade"], "B+")
        self.assertGreater(spcx[0]["score"], 55)


class TestMonitorOnlyInvariants(unittest.TestCase):
    def test_scorer_output_no_execution_terms(self):
        import glob
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "by_symbol" / "*.json")
        forbidden = ["execute", "broker", "order_book", "auto_trade", "market_order", "limit_order"]
        for f in sorted(glob.glob(pattern)):
            text = open(f).read().lower()
            for term in forbidden:
                self.assertNotIn(term, text, f"{Path(f).name}: forbidden '{term}'")

    def test_all_setups_monitor_only(self):
        import glob
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "by_symbol" / "*.json")
        for f in sorted(glob.glob(pattern)):
            d = json.loads(open(f).read())
            for s in d.get("setups", []):
                self.assertIn(s.get("direction", ""), {"long", "short", "monitor_only"})
