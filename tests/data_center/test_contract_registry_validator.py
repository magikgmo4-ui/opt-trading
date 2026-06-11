"""Tests for contract_registry_validator.py"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from modules.data_center.contract_registry_validator import validate, load_contracts


class TestContractRegistry:

    def test_contracts_json_exists(self):
        data = load_contracts()
        assert "contracts" in data
        assert len(data["contracts"]) > 0

    def test_all_28_contracts_present(self):
        data = load_contracts()
        contracts = data["contracts"]
        assert len(contracts) == 28, f"Expected 28, got {len(contracts)}"

    def test_7_domains_registered(self):
        data = load_contracts()
        domains = data.get("domains", {})
        assert len(domains) == 7

    def test_no_duplicate_contract_ids(self):
        data = load_contracts()
        ids = list(data["contracts"].keys())
        assert len(ids) == len(set(ids))

    def test_all_required_fields(self):
        data = load_contracts()
        required = ["domain", "provider_id", "schedule", "status"]
        for cid, c in data["contracts"].items():
            for field in required:
                assert field in c, f"{cid}: missing {field}"

    def test_proven_contracts_have_score(self):
        data = load_contracts()
        for cid, c in data["contracts"].items():
            if c["status"] == "PROVEN" and not c.get("on_demand"):
                assert c.get("score") is not None, f"{cid}: PROVEN but no score"

    def test_all_have_data_keys(self):
        data = load_contracts()
        for cid, c in data["contracts"].items():
            keys = c.get("data_keys", [])
            assert len(keys) > 0, f"{cid}: no data_keys"

    def test_summary_matches(self):
        data = load_contracts()
        s = data.get("summary", {})
        contracts = data["contracts"]
        assert s["total_contracts"] == len(contracts)
        assert s["proven"] == sum(1 for c in contracts.values() if c["status"] == "PROVEN")
        assert s["partial"] == sum(1 for c in contracts.values() if c["status"] == "PARTIAL")

    def test_domain_contracts_consistent(self):
        data = load_contracts()
        domains = data["domains"]
        for dom_id, dom in domains.items():
            listed = set(dom["contracts"])
            actual = {cid for cid, c in data["contracts"].items() if c["domain"] == dom_id}
            assert listed == actual, f"domain {dom_id}: mismatch {sorted(listed ^ actual)}"
