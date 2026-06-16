"""
Tests for live_data_binder — GO_SETUP_CARDS_LIVE_DATA_BINDING_01.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from modules.executive_intelligence.templates.live_data_binder import (
    bind_live_data,
    check_data_freshness,
    get_active_cdp_triggers,
    get_live_price,
    get_reliability_context,
)


class TestLivePrice(unittest.TestCase):
    @patch("modules.market_thesis.config.source_path_for_symbol")
    def test_price_from_market_metrics(self, mock_path):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"last_price": 66450.5, "metrics_ts": "2026-06-15T12:00:00Z"}')
            f.flush()
            mock_path.return_value = Path(f.name)

        price = get_live_price("BTC")
        self.assertEqual(price, 66450.5)
        Path(f.name).unlink(missing_ok=True)

    @patch("modules.market_thesis.config.source_path_for_symbol")
    def test_price_missing(self, mock_path):
        mock_path.return_value = None
        self.assertIsNone(get_live_price("ZZZ"))


class TestCDPTriggers(unittest.TestCase):
    @patch("modules.market_thesis.config.source_path_for_symbol")
    def test_triggers_from_signal_event(self, mock_path):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('[{"event": "vwap_reclaim", "source": "tradingview_cdp", "price": 172.5, "timestamp": "2026-06-15T12:00:00Z"}]')
            f.flush()
            mock_path.return_value = Path(f.name)

        triggers = get_active_cdp_triggers("SPCX")
        self.assertGreater(len(triggers), 0)
        self.assertEqual(triggers[0]["event"], "vwap_reclaim")
        Path(f.name).unlink(missing_ok=True)

    @patch("modules.market_thesis.config.source_path_for_symbol")
    def test_no_triggers(self, mock_path):
        mock_path.return_value = None
        self.assertEqual(get_active_cdp_triggers("ZZZ"), [])


class TestReliabilityContext(unittest.TestCase):
    @patch("modules.market_thesis.reliability_engine.evaluate_reliability")
    def test_reliability(self, mock_rel):
        from modules.market_thesis.reliability_engine import ReliabilityReport
        mock_rel.return_value = ReliabilityReport(
            symbol="BTC", reliability_score=82, grade="excellent", sample_size=200,
            sample_score=30, accuracy_score=32, calibration_score=15, probability_score=5,
        )
        ctx = get_reliability_context("BTC")
        self.assertEqual(ctx["score"], 82)
        self.assertEqual(ctx["grade"], "excellent")


class TestFreshnessCheck(unittest.TestCase):
    @patch("modules.market_thesis.config.source_path_for_symbol")
    def test_stale_detection(self, mock_path):
        mock_path.return_value = None  # All missing = stale
        result = check_data_freshness("BTC")
        self.assertTrue(result["is_stale"])
        self.assertGreater(len(result["stale_sources"]), 0)


class TestBindLiveData(unittest.TestCase):
    @patch("modules.executive_intelligence.templates.live_data_binder.get_live_metrics")
    @patch("modules.executive_intelligence.templates.live_data_binder.get_active_cdp_triggers")
    @patch("modules.executive_intelligence.templates.live_data_binder.get_reliability_context")
    @patch("modules.executive_intelligence.templates.live_data_binder.get_leaderboard_position")
    @patch("modules.executive_intelligence.templates.live_data_binder.check_data_freshness")
    def test_bind_all(self, mock_fresh, mock_lb, mock_rel, mock_cdp, mock_metrics):
        mock_metrics.return_value = {"price": 66500, "open_interest": 28e9}
        mock_cdp.return_value = [{"event": "vwap_reclaim", "active": True}]
        mock_rel.return_value = {"score": 82, "grade": "excellent", "sample_size": 200}
        mock_lb.return_value = {"rank": 2, "is_leader": True, "momentum_score": 70}
        mock_fresh.return_value = {"is_stale": False, "stale_sources": []}

        live = bind_live_data("BTC")
        self.assertEqual(live["price"], 66500)
        self.assertEqual(len(live["cdp_triggers"]), 1)
        self.assertEqual(live["reliability"]["score"], 82)
        self.assertTrue(live["leaderboard"]["is_leader"])
        self.assertTrue(live["has_data"])

    @patch("modules.executive_intelligence.templates.live_data_binder.get_live_metrics")
    @patch("modules.executive_intelligence.templates.live_data_binder.get_active_cdp_triggers")
    def test_no_data_flag(self, mock_cdp, mock_metrics):
        mock_metrics.return_value = {}
        mock_cdp.return_value = []
        with patch.object(
            __import__("modules.executive_intelligence.templates.live_data_binder", fromlist=["get_reliability_context"]),
            "get_reliability_context", return_value={},
        ), patch.object(
            __import__("modules.executive_intelligence.templates.live_data_binder", fromlist=["get_leaderboard_position"]),
            "get_leaderboard_position", return_value={},
        ), patch.object(
            __import__("modules.executive_intelligence.templates.live_data_binder", fromlist=["check_data_freshness"]),
            "check_data_freshness", return_value={"is_stale": True, "stale_sources": ["all"]},
        ):
            live = bind_live_data("ZZZ")
            self.assertFalse(live["has_data"])


if __name__ == "__main__":
    unittest.main()
