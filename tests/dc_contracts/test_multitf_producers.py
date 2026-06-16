"""Tests for multitf_analysis_producer and multitf_setup_scorer."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class TestMultiTFAnalysisProducer(unittest.TestCase):
    def test_producer_runs_without_crash(self):
        from modules.data_center.multitf_analysis_producer import produce_multitf_analysis_input
        result = produce_multitf_analysis_input()
        self.assertIn("symbols", result)
        self.assertGreaterEqual(result["symbols"], 0)

    def test_output_view_exists(self):
        from modules.data_center.multitf_analysis_producer import produce_multitf_analysis_input
        produce_multitf_analysis_input()
        latest = PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_analysis_input.v1" / "latest.json"
        self.assertTrue(latest.exists(), "latest.json not written")

    def test_output_has_correct_class(self):
        latest = PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_analysis_input.v1" / "latest.json"
        data = json.loads(latest.read_text())
        self.assertEqual(data["input_class"], "multitf_analysis_input.v1")
        self.assertEqual(data["provider_id"], "data_center_aggregator")

    def test_per_symbol_views_have_required_fields(self):
        import glob
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_analysis_input.v1" / "by_symbol" / "*.json")
        for f in sorted(glob.glob(pattern)):
            d = json.loads(open(f).read())
            self.assertEqual(d["input_class"], "multitf_analysis_input.v1")
            self.assertIn("symbol", d)
            self.assertIn("as_of", d)
            self.assertIn("freshness_state", d)
            self.assertIn("timeframes", d)
            self.assertIn("signals", d)
            self.assertIn("missing", d)
            self.assertIn("source_quality", d)
            self.assertIn("price", d)

    def test_symbols_have_asset_class(self):
        import glob
        valid = {"crypto_perp", "forex_cfd", "stock", "ipo", "index", "commodity", "unknown"}
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_analysis_input.v1" / "by_symbol" / "*.json")
        for f in sorted(glob.glob(pattern)):
            d = json.loads(open(f).read())
            self.assertIn(d.get("asset_class", ""), valid, f"{Path(f).name}: bad asset_class")

    def test_timeframes_have_required_tfs(self):
        import glob
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_analysis_input.v1" / "by_symbol" / "*.json")
        for f in sorted(glob.glob(pattern)):
            d = json.loads(open(f).read())
            tfs = d.get("timeframes", {})
            for tf in ["H4", "H1", "M15"]:
                self.assertIn(tf, tfs, f"{Path(f).name}: missing timeframe {tf}")

    def test_non_symbols_not_in_by_symbol_dir(self):
        """Only actual symbols should have per-symbol views."""
        by_sym = PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_analysis_input.v1" / "by_symbol"
        for f in by_sym.glob("*.json"):
            name = f.stem
            self.assertNotIn("latest", name.lower())
            self.assertNotIn("global", name.lower())


class TestMultiTFSetupScorer(unittest.TestCase):
    def test_scorer_runs_without_crash(self):
        from modules.data_center.multitf_setup_scorer import produce_multitf_setup_scores
        result = produce_multitf_setup_scores()
        self.assertIn("symbols", result)
        self.assertGreaterEqual(result["symbols"], 0)

    def test_output_view_exists(self):
        from modules.data_center.multitf_setup_scorer import produce_multitf_setup_scores
        produce_multitf_setup_scores()
        latest = PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "latest.json"
        self.assertTrue(latest.exists(), "latest.json not written")

    def test_output_has_correct_class(self):
        latest = PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "latest.json"
        if not latest.exists():
            from modules.data_center.multitf_setup_scorer import produce_multitf_setup_scores
            produce_multitf_setup_scores()
        data = json.loads(latest.read_text())
        self.assertEqual(data["output_class"], "multitf_setup_score.v1")

    def test_per_symbol_views_have_required_fields(self):
        import glob
        from modules.data_center.multitf_setup_scorer import produce_multitf_setup_scores
        produce_multitf_setup_scores()
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "by_symbol" / "*.json")
        files = sorted(glob.glob(pattern))
        self.assertGreater(len(files), 0, "No per-symbol score views written")
        for f in files:
            d = json.loads(open(f).read())
            self.assertEqual(d["output_class"], "multitf_setup_score.v1")
            self.assertIn("symbol", d)
            self.assertIn("bias", d)
            self.assertIn("setups", d)
            self.assertIn("top_setup", d)
            self.assertIn("next_action", d)
            self.assertIn("missing", d)
            self.assertIn("source_quality", d)

    def test_setup_structure(self):
        import glob
        from modules.data_center.multitf_setup_scorer import produce_multitf_setup_scores
        produce_multitf_setup_scores()
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "by_symbol" / "*.json")
        for f in sorted(glob.glob(pattern)):
            d = json.loads(open(f).read())
            for st in d.get("setups", []):
                self.assertIn("setup_id", st)
                self.assertIn("direction", st)
                self.assertIn("grade", st)
                self.assertIn("score", st)
                self.assertTrue(0 <= st["score"] <= 100, f"score out of range: {st['score']}")
                self.assertIn("probability_pct", st)
                self.assertIn("confidence_pct", st)
                self.assertIn("entry_zone", st)
                self.assertIn("invalidation", st)
                self.assertIn("targets", st)
                self.assertIn("score_breakdown", st)

    def test_setup_direction_monitor_only(self):
        import glob
        from modules.data_center.multitf_setup_scorer import produce_multitf_setup_scores
        produce_multitf_setup_scores()
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "by_symbol" / "*.json")
        for f in sorted(glob.glob(pattern)):
            d = json.loads(open(f).read())
            for st in d.get("setups", []):
                self.assertIn(st["direction"], {"long", "short", "monitor_only"})

    def test_bias_has_required_fields(self):
        import glob
        from modules.data_center.multitf_setup_scorer import produce_multitf_setup_scores
        produce_multitf_setup_scores()
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "by_symbol" / "*.json")
        for f in sorted(glob.glob(pattern)):
            d = json.loads(open(f).read())
            bias = d.get("bias", {})
            self.assertIn("htf", bias)
            self.assertIn("ltf", bias)
            self.assertIn("alignment", bias)
            self.assertIn("reason", bias)

    def test_source_quality_structure(self):
        import glob
        from modules.data_center.multitf_setup_scorer import produce_multitf_setup_scores
        produce_multitf_setup_scores()
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "by_symbol" / "*.json")
        for f in sorted(glob.glob(pattern)):
            d = json.loads(open(f).read())
            sq = d.get("source_quality", {})
            self.assertIn("input_freshness", sq)
            self.assertIn("completeness_pct", sq)
            self.assertIn("timeframes_with_data", sq)
            self.assertIn("timeframes_missing", sq)


class TestProducerMonitorOnlyInvariants(unittest.TestCase):
    def test_scorer_produces_no_execution_terms(self):
        import glob
        from modules.data_center.multitf_setup_scorer import produce_multitf_setup_scores
        produce_multitf_setup_scores()
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "by_symbol" / "*.json")
        forbidden = ["execute", "broker", "order_book", "auto_trade", "market_order", "limit_order"]
        for f in sorted(glob.glob(pattern)):
            text = open(f).read().lower()
            for term in forbidden:
                self.assertNotIn(term, text, f"{Path(f).name} contains forbidden: {term}")

    def test_analysis_producer_output_no_order_terms(self):
        import glob
        pattern = str(PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_analysis_input.v1" / "by_symbol" / "*.json")
        forbidden = ["execute", "broker", "order_book", "auto_trade", "market_order"]
        for f in sorted(glob.glob(pattern)):
            text = open(f).read().lower()
            for term in forbidden:
                self.assertNotIn(term, text, f"{Path(f).name} contains forbidden: {term}")
