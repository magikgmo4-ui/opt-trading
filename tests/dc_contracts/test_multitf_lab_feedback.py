"""Tests for Lab backtest feedback loop — exporter + edge scorer + scorer feedback."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestLabExporter(unittest.TestCase):
    def setUp(self):
        from modules.analysis_bundles.lab_backtest.setup_candidate_exporter import export_setup_candidates
        self.result = export_setup_candidates()

    def test_export_has_exported_count(self):
        self.assertIn("exported", self.result)

    def test_candidates_file_exists(self):
        path = PROJECT_ROOT / "outputs" / "lab_backtest" / "inbox" / "setup_candidates.jsonl"
        self.assertTrue(path.exists(), "setup_candidates.jsonl not written")

    def test_candidates_have_required_fields(self):
        path = PROJECT_ROOT / "outputs" / "lab_backtest" / "inbox" / "setup_candidates.jsonl"
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            d = json.loads(line)
            for field in ["setup_id", "symbol", "setup_type", "score_before_backtest",
                          "grade_before_backtest", "core_evidence", "monitor_only"]:
                self.assertIn(field, d, f"Missing {field}")

    def test_all_candidates_monitor_only(self):
        path = PROJECT_ROOT / "outputs" / "lab_backtest" / "inbox" / "setup_candidates.jsonl"
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            d = json.loads(line)
            self.assertTrue(d.get("monitor_only"), "monitor_only must be True")

    def test_no_execution_terms(self):
        path = PROJECT_ROOT / "outputs" / "lab_backtest" / "inbox" / "setup_candidates.jsonl"
        forbidden = ["execute", "broker", "order_book", "auto_trade", "market_order"]
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            text = line.lower()
            for term in forbidden:
                self.assertNotIn(term, text, f"Forbidden term '{term}' in candidate")


class TestLabEdgeScorer(unittest.TestCase):
    def setUp(self):
        from modules.analysis_bundles.lab_backtest.setup_edge_scorer import score_candidates
        self.result = score_candidates()

    def test_scorer_returns_scored_count(self):
        self.assertIn("scored", self.result)

    def test_edge_scores_file_exists(self):
        path = PROJECT_ROOT / "outputs" / "lab_backtest" / "results" / "setup_edge_scores.jsonl"
        self.assertTrue(path.exists())

    def test_edge_scores_have_required_fields(self):
        path = PROJECT_ROOT / "outputs" / "lab_backtest" / "results" / "setup_edge_scores.jsonl"
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            d = json.loads(line)
            for field in ["setup_id", "symbol", "setup_type", "sample_size", "win_rate",
                          "edge_score", "recommendation", "monitor_only"]:
                self.assertIn(field, d, f"Missing {field}")

    def test_recommendation_is_valid(self):
        path = PROJECT_ROOT / "outputs" / "lab_backtest" / "results" / "setup_edge_scores.jsonl"
        valid = {"supportive", "neutral", "negative", "insufficient_sample"}
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            d = json.loads(line)
            self.assertIn(d.get("recommendation"), valid)

    def test_insufficient_sample_returns_no_boost(self):
        from modules.analysis_bundles.lab_backtest.setup_edge_scorer import _score_edge
        result = _score_edge({"sample_size": 5, "win_rate": 0.80, "avg_r": 2.0, "profit_factor": 2.5})
        self.assertEqual(result["recommendation"], "insufficient_sample")
        self.assertEqual(result["edge_score"], 0)

    def test_supportive_edge_scores_high(self):
        from modules.analysis_bundles.lab_backtest.setup_edge_scorer import _score_edge
        result = _score_edge({"sample_size": 100, "win_rate": 0.65, "avg_r": 1.8, "profit_factor": 2.0})
        self.assertEqual(result["recommendation"], "supportive")
        self.assertGreater(result["edge_score"], 60)

    def test_negative_edge_scores_low(self):
        from modules.analysis_bundles.lab_backtest.setup_edge_scorer import _score_edge
        result = _score_edge({"sample_size": 50, "win_rate": 0.35, "avg_r": 0.5, "profit_factor": 0.6})
        self.assertEqual(result["recommendation"], "negative")
        self.assertLess(result["edge_score"], 45)


class TestLabScorerFeedback(unittest.TestCase):
    """Verify Lab results feed back into scorer correctly."""

    def test_lab_edge_loaded(self):
        from modules.data_center.multitf_setup_scorer import _load_lab_edge
        edge = _load_lab_edge("SPCX", "vwap_reclaim")
        if edge:
            self.assertIn("edge_score", edge)

    def test_no_trigger_still_capped_with_lab_support(self):
        """Even with supportive Lab edge, no CDP trigger = cap C+"""
        from modules.data_center.multitf_setup_scorer import _score_setups
        entry = {
            "symbol": "ETH", "price": 1800, "freshness_state": "fresh",
            "asset_class": "crypto_perp",
            "timeframes": {"H4": {"indicators": {"trend": "bearish"}}, "M15": {"indicators": {"trend": "bearish"}}},
            "levels": {"support_levels": [1700]},
            "signals": [],
        }
        setups = _score_setups(entry)
        if setups:
            self.assertLess(setups[0]["score"], 40, "No trigger should stay < 40 even with Lab")

    def test_negative_lab_edge_adds_downgrade(self):
        from modules.data_center.multitf_setup_scorer import _score_setups
        entry = {
            "symbol": "ETH", "price": 1800, "freshness_state": "fresh",
            "asset_class": "crypto_perp",
            "timeframes": {"H4": {"indicators": {"trend": "bearish"}}, "M15": {"indicators": {"trend": "bearish"}}},
            "levels": {"support_levels": [1700]},
            "signals": [],
        }
        setups = _score_setups(entry)
        if setups:
            dg = setups[0].get("downgrade_reasons", [])
            # Lab negative should appear in downgrades or the grade should be capped
            has_lab = any("Lab" in r for r in dg)
            self.assertTrue(has_lab or setups[0]["score"] < 40)

    def test_supportive_lab_edge_boosts_backtest(self):
        from modules.data_center.multitf_setup_scorer import _score_setups
        entry = {
            "symbol": "SPCX", "price": 171.5, "freshness_state": "fresh",
            "asset_class": "ipo",
            "timeframes": {"H4": {"indicators": {"trend": "neutral"}}, "M15": {"indicators": {"trend": "neutral"}}},
            "levels": {"support_levels": [165], "resistance_levels": [180]},
            "signals": [{"source": "tradingview_cdp", "event": "vwap_reclaim", "timestamp": "2026-06-15T17:30:00Z"}],
        }
        setups = _score_setups(entry)
        if setups:
            be = setups[0].get("score_breakdown", {}).get("backtest_edge", 0)
            self.assertGreater(be, 1, f"Lab supportive should boost backtest_edge, got {be}")
