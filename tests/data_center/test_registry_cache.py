"""Tests for registry_cache.py"""

import pytest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from modules.data_center import registry_cache as rc


class TestGetCache:
    def test_get_cache_returns_dict(self):
        cache = rc.get_cache()
        assert isinstance(cache, dict)
        assert "by_contract_class" in cache
        assert "by_data_key" in cache
        assert "by_source" in cache
        assert "by_priority" in cache
        assert "by_symbol" in cache

    def test_cache_not_none(self):
        rc.invalidate_cache()
        cache = rc.get_cache()
        assert cache is not None


class TestGetByContractClass:
    def test_market_metrics_exists(self):
        info = rc.get_by_contract_class("market_metrics.v1")
        assert info is not None
        assert "funding_rate" in info["data_keys"]

    def test_nonexistent_returns_none(self):
        assert rc.get_by_contract_class("nonexistent.v42") is None


class TestGetByDataKey:
    def test_futures_open_interest(self):
        info = rc.get_by_data_key("futures_open_interest")
        assert info is not None
        assert info["contract_class"] == "market_metrics.v1"
        assert len(info["producers"]) >= 2

    def test_funding_rate(self):
        info = rc.get_by_data_key("funding_rate")
        assert info is not None

    def test_nonexistent_returns_none(self):
        assert rc.get_by_data_key("nonexistent_key_xyz") is None


class TestGetCandidates:
    def test_market_metrics_oi(self):
        result = rc.get_candidates("market_metrics.v1", "futures_open_interest")
        assert len(result["producers"]) >= 2
        assert result["criticality"] <= 10

    def test_wrong_contract_class_returns_empty_producers(self):
        result = rc.get_candidates("wrong.v1", "futures_open_interest")
        assert result["producers"] == []

    def test_unknown_data_key(self):
        result = rc.get_candidates("market_metrics.v1", "unknown_key_xyz")
        assert result["producers"] == []


class TestGetBySource:
    def test_bitget_exists(self):
        info = rc.get_by_source("derivatives_collector__bitget")
        assert info is not None
        assert info["family"] == "derivatives"

    def test_binance_exists(self):
        info = rc.get_by_source("derivatives_collector__binance")
        assert info is not None


class TestGetByPriority:
    def test_p0_exists(self):
        info = rc.get_by_priority("P0")
        assert info is not None
        assert info["criticality"] == 1

    def test_p21_exists(self):
        info = rc.get_by_priority("P21")
        assert info is not None


class TestCacheInvalidation:
    def test_invalidate_reloads(self):
        rc.invalidate_cache()
        cache1 = rc.get_cache()
        rc.invalidate_cache()
        cache2 = rc.get_cache()
        assert cache1 is not cache2  # new object after invalidate


class TestRebuildCache:
    def test_rebuild_returns_dict(self):
        cache = rc.rebuild_cache()
        assert isinstance(cache, dict)
        assert "by_data_key" in cache
