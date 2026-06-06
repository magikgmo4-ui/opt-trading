"""Tests for source_selector.py"""

import pytest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from modules.data_center import source_selector as ss
from modules.data_center import registry_cache as rc


class TestResolveBestCandidate:
    def test_market_metrics_oi(self):
        result = ss.resolve("market_metrics.v1", "BTCUSDT", "futures_open_interest", mode="best_candidate")
        assert "resolver_decision" in result
        assert "canonical_value" in result
        rd = result["resolver_decision"]
        assert rd["schema_version"] == "resolver_decision.v1"
        assert rd["contract_class"] == "market_metrics.v1"
        assert rd["data_key"] == "futures_open_interest"
        assert len(rd["candidates"]) >= 0
        assert "selection_rule" in rd

    def test_unknown_contract_returns_stale(self):
        result = ss.resolve("nonexistent.v1", "BTCUSDT", "futures_open_interest", mode="best_candidate")
        assert result["canonical_value"]["stale"] is True
        assert result["resolver_decision"]["selection_rule"] == "stale_fallback"

    def test_unknown_data_key_returns_stale(self):
        result = ss.resolve("market_metrics.v1", "BTCUSDT", "unknown_key_xyz", mode="best_candidate")
        assert result["canonical_value"]["stale"] is True


class TestResolveAllCandidates:
    def test_returns_all_candidates(self):
        result = ss.resolve("market_metrics.v1", "BTCUSDT", "futures_open_interest", mode="all_candidates")
        assert "all_candidates" in result
        assert "resolver_decision" in result


class TestResolveConsensus:
    def test_consensus_stale_if_no_candidates(self):
        result = ss.resolve("nonexistent.v1", "BTCUSDT", "futures_open_interest", mode="consensus")
        assert result["canonical_value"]["stale"] is True


class TestResolveFallback:
    def test_fallback_mode_returns_result(self):
        result = ss.resolve("market_metrics.v1", "BTCUSDT", "futures_open_interest", mode="fallback_only")
        assert "resolver_decision" in result


class TestResolverDecision:
    def test_decision_has_decision_id(self):
        result = ss.resolve("market_metrics.v1", "BTCUSDT", "futures_open_interest")
        rd = result["resolver_decision"]
        assert len(rd["decision_id"]) == 36

    def test_canonical_value_refs_decision(self):
        result = ss.resolve("market_metrics.v1", "BTCUSDT", "futures_open_interest")
        rd = result["resolver_decision"]
        cv = result["canonical_value"]
        assert cv["resolver_decision_ref"] == rd["decision_id"]

    def test_canonical_value_has_stale_flag(self):
        result = ss.resolve("market_metrics.v1", "BTCUSDT", "futures_open_interest")
        cv = result["canonical_value"]
        assert "stale" in cv

    def test_selection_rule_present(self):
        result = ss.resolve("market_metrics.v1", "BTCUSDT", "futures_open_interest")
        assert result["resolver_decision"]["selection_rule"] in (
            "highest_score", "only_eligible", "stale_fallback",
            "consensus", "fallback_only", "fallback_only__secondary",
            "no_candidates", "no_eligible_candidates",
        )


class TestDataCenterDoesNotDecideTrades:
    def test_no_trading_signal_in_output(self):
        result = ss.resolve("market_metrics.v1", "BTCUSDT", "futures_open_interest")
        rd = result["resolver_decision"]
        assert "direction" not in rd
        assert "trade" not in rd
        assert "order" not in rd

    def test_only_source_selection_info(self):
        result = ss.resolve("market_metrics.v1", "BTCUSDT", "futures_open_interest")
        rd = result["resolver_decision"]
        allowed_keys = {
            "schema_version", "decision_id", "contract_class", "symbol",
            "data_key", "decided_at", "candidates", "selected_producer_id",
            "selected_score", "selection_reason", "selection_rule",
            "min_score_threshold", "resolver_version",
        }
        assert set(rd.keys()).issubset(allowed_keys)
