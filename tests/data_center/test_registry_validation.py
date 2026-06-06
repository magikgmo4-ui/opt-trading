"""Tests for registry_validation.py"""

import pytest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from modules.data_center import registry_validation as rv


class TestLoadInventory:
    def test_load_inventory_exists(self):
        inv = rv.load_inventory()
        assert "data_items" in inv
        assert len(inv["data_items"]) == 22

    def test_load_source_candidates_exists(self):
        cand = rv.load_source_candidates()
        assert "source_candidates" in cand
        assert len(cand["source_candidates"]) == 22

    def test_load_producers_exists(self):
        prod = rv.load_producers()
        assert "producers" in prod
        assert len(prod["producers"]) == 7


class TestValidateInventorySummary:
    def test_summary_matches_actual(self):
        inv = rv.load_inventory()
        errors = rv.validate_inventory_summary(inv)
        assert errors == [], f"Summary mismatch: {errors}"

    def test_total_fields_is_671(self):
        inv = rv.load_inventory()
        assert inv["summary"]["total_fields"] == 671


class TestValidateUniqueDataKeys:
    def test_no_duplicates(self):
        inv = rv.load_inventory()
        errors = rv.validate_unique_data_keys(inv)
        assert errors == [], f"Duplicate keys: {errors}"

    def test_known_key_exists(self):
        inv = rv.load_inventory()
        keys = set()
        for item in inv["data_items"]:
            for f in item["fields"]:
                keys.add(f["data_key"])
        assert "futures_open_interest" in keys
        assert "funding_rate" in keys
        assert "last_price" in keys


class TestValidateSourceCandidates:
    def test_all_coverage_keys_exist_in_inventory(self):
        inv = rv.load_inventory()
        cand = rv.load_source_candidates()
        errors = rv.validate_source_candidates(cand, inv)
        assert errors == [], f"Coverage key errors: {errors}"

    def test_score_zero_policy_is_unevaluated(self):
        cand = rv.load_source_candidates()
        errors = rv.validate_score_zero_policy(cand)
        assert errors == [], f"Score zero policy errors: {errors}"

    def test_candidate_data_keys_exist(self):
        inv = rv.load_inventory()
        cand = rv.load_source_candidates()
        errors = rv.validate_candidate_data_keys_exist(cand, inv)
        assert errors == [], f"Data key existence errors: {errors[:5]}"


class TestProducerConsistency:
    def test_active_registry_in_producers(self):
        cand = rv.load_source_candidates()
        prod = rv.load_producers()
        errors = rv.validate_producer_registry_consistency(cand, prod)
        assert errors == [], f"Producer consistency errors: {errors}"


class TestSourceSelectability:
    def test_score_zero_candidate_not_selectable(self):
        src = {"source_id": "test", "score": 0, "status": "candidate"}
        assert rv.is_source_selectable(src) is False

    def test_active_registry_selectable(self):
        src = {"source_id": "test", "score": 0, "status": "active_registry"}
        assert rv.is_source_selectable(src) is True

    def test_evaluated_selectable(self):
        src = {"source_id": "test", "score": 0.85, "status": "evaluated"}
        assert rv.is_source_selectable(src) is True

    def test_candidate_with_score_not_selectable(self):
        src = {"source_id": "test", "score": 0.5, "status": "candidate"}
        assert rv.is_source_selectable(src) is False  # status=candidate blocks
