"""Tests for registry_index_builder.py"""

import pytest
import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from modules.data_center import registry_index_builder as rib
from modules.data_center import registry_validation as rv

COMPILED_DIR = REPO_ROOT / "data" / "data_center" / "_registry" / "compiled"


class TestBuildByContractClass:
    def test_returns_dict(self):
        inv = rv.load_inventory()
        cand = rv.load_source_candidates()
        result = rib.build_by_contract_class(inv, cand)
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_market_metrics_present(self):
        inv = rv.load_inventory()
        cand = rv.load_source_candidates()
        result = rib.build_by_contract_class(inv, cand)
        assert "market_metrics.v1" in result
        mm = result["market_metrics.v1"]
        assert "futures_open_interest" in mm["data_keys"]
        assert "funding_rate" in mm["data_keys"]
        assert len(mm["producers"]) >= 2


class TestBuildByDataKey:
    def test_returns_dict(self):
        inv = rv.load_inventory()
        cand = rv.load_source_candidates()
        result = rib.build_by_data_key(inv, cand)
        assert isinstance(result, dict)
        assert "futures_open_interest" in result

    def test_futures_open_interest_has_producers(self):
        inv = rv.load_inventory()
        cand = rv.load_source_candidates()
        result = rib.build_by_data_key(inv, cand)
        oi = result["futures_open_interest"]
        assert len(oi["producers"]) >= 2

    def test_data_key_count_matches_inventory(self):
        inv = rv.load_inventory()
        cand = rv.load_source_candidates()
        result = rib.build_by_data_key(inv, cand)
        actual = sum(len(item["fields"]) for item in inv["data_items"])
        assert len(result) <= actual  # some keys may not have contract_class


class TestBuildBySource:
    def test_returns_dict(self):
        prod = rv.load_producers()
        inv = rv.load_inventory()
        cand = rv.load_source_candidates()
        result = rib.build_by_source(prod, inv, cand)
        assert isinstance(result, dict)
        assert len(result) == 7


class TestBuildByPriority:
    def test_returns_dict(self):
        inv = rv.load_inventory()
        result = rib.build_by_priority(inv)
        assert len(result) == 22
        assert "P0" in result
        assert "P21" in result


class TestRebuildAll:
    def test_creates_compiled_files(self):
        v = rib.rebuild_all()
        assert len(v) == 12 or len(v) == 64  # short hash or full SHA256
        assert (COMPILED_DIR / "_compiled.json").exists()
        assert (COMPILED_DIR / "by_contract_class.json").exists()
        assert (COMPILED_DIR / "by_data_key.json").exists()
        assert (COMPILED_DIR / "by_source.json").exists()
        assert (COMPILED_DIR / "by_priority.json").exists()
        assert (COMPILED_DIR / "by_symbol.json").exists()

    def test_compiled_valid_json(self):
        rib.rebuild_all()
        for f in COMPILED_DIR.glob("*.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            assert isinstance(data, (dict, list))
