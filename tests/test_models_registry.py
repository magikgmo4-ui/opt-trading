"""Tests for ai_models_registry (scripts/ai/workers/models.registry.json).

Validates structure, required fields, status consistency, and schema version.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "scripts" / "ai" / "workers" / "models.registry.json"

VALID_STATUSES = {
    "VERIFIED",
    "VERIFIED_FREE",
    "RETIRED_CURRENT_ENDPOINT",
    "ABSENT_CURRENT_ENDPOINT",
    "OBSOLETE_REPLACED",
    "DRAFT_ONLY",
}
VALID_AUTONOMY = {"A0", "A1", "A2"}
KNOWN_ROLES = {
    "READ_INVENTORY", "PATCH_DRAFT", "DOC_DRAFT", "TESTPLAN",
    "FAST_TRIAGE", "CHERRY_PICK_INVENTORY", "REVIEW_DRAFT", "CLOSEOUT_DRAFT",
}
ACTIVE_STATUSES = {"VERIFIED", "VERIFIED_FREE"}
INACTIVE_STATUSES = {"RETIRED_CURRENT_ENDPOINT", "ABSENT_CURRENT_ENDPOINT", "OBSOLETE_REPLACED"}


class TestRegistryFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REGISTRY_PATH.read_text())

    def test_file_exists(self):
        self.assertTrue(REGISTRY_PATH.exists())

    def test_valid_json(self):
        self.assertIsInstance(self.data, dict)

    def test_schema_version_is_stable(self):
        v = self.data["schema_version"]
        self.assertNotIn("draft", v.lower(), "schema_version still contains 'draft'")
        self.assertEqual(v, "1.0")

    def test_required_top_level_keys(self):
        for key in ("schema_version", "go_id", "models", "validated_at"):
            self.assertIn(key, self.data)

    def test_models_is_dict(self):
        self.assertIsInstance(self.data["models"], dict)

    def test_models_non_empty(self):
        self.assertGreater(len(self.data["models"]), 0)


class TestModelEntries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models = json.loads(REGISTRY_PATH.read_text())["models"]

    def test_all_have_status(self):
        for name, m in self.models.items():
            self.assertIn("status", m, f"{name} missing status")

    def test_all_statuses_valid(self):
        for name, m in self.models.items():
            self.assertIn(m["status"], VALID_STATUSES, f"{name} has unknown status: {m['status']}")

    def test_all_have_autonomy_max(self):
        for name, m in self.models.items():
            self.assertIn("autonomy_max", m, f"{name} missing autonomy_max")

    def test_all_autonomy_max_valid(self):
        for name, m in self.models.items():
            self.assertIn(m["autonomy_max"], VALID_AUTONOMY, f"{name} invalid autonomy_max: {m['autonomy_max']}")

    def test_all_have_roles_list(self):
        for name, m in self.models.items():
            self.assertIn("roles", m, f"{name} missing roles")
            self.assertIsInstance(m["roles"], list, f"{name} roles is not a list")

    def test_roles_from_known_set(self):
        for name, m in self.models.items():
            for role in m["roles"]:
                self.assertIn(role, KNOWN_ROLES, f"{name} has unknown role: {role}")


class TestModelConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models = json.loads(REGISTRY_PATH.read_text())["models"]

    def test_verified_models_have_config_id(self):
        for name, m in self.models.items():
            if m["status"] in ACTIVE_STATUSES:
                self.assertIsNotNone(m.get("config_id"), f"{name} VERIFIED but config_id is null")

    def test_verified_models_have_non_empty_roles(self):
        for name, m in self.models.items():
            if m["status"] in ACTIVE_STATUSES:
                self.assertGreater(len(m["roles"]), 0, f"{name} VERIFIED but roles is empty")

    def test_verified_models_have_a1_or_a2_autonomy(self):
        for name, m in self.models.items():
            if m["status"] in ACTIVE_STATUSES:
                self.assertIn(m["autonomy_max"], {"A1", "A2"}, f"{name} VERIFIED but autonomy_max={m['autonomy_max']}")

    def test_inactive_models_have_a0_autonomy(self):
        for name, m in self.models.items():
            if m["status"] in INACTIVE_STATUSES:
                self.assertEqual(m["autonomy_max"], "A0", f"{name} inactive but autonomy_max={m['autonomy_max']}")

    def test_inactive_models_have_empty_roles(self):
        for name, m in self.models.items():
            if m["status"] in INACTIVE_STATUSES:
                self.assertEqual(m["roles"], [], f"{name} inactive but roles non-empty: {m['roles']}")

    def test_at_least_one_verified_free_model(self):
        free = [n for n, m in self.models.items() if m["status"] == "VERIFIED_FREE"]
        self.assertGreater(len(free), 0)

    def test_at_least_one_verified_model(self):
        verified = [n for n, m in self.models.items() if m["status"] == "VERIFIED"]
        self.assertGreater(len(verified), 0)


class TestModelCounts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models = json.loads(REGISTRY_PATH.read_text())["models"]

    def test_verified_count(self):
        count = sum(1 for m in self.models.values() if m["status"] == "VERIFIED")
        self.assertGreaterEqual(count, 8)

    def test_free_count(self):
        count = sum(1 for m in self.models.values() if m["status"] == "VERIFIED_FREE")
        self.assertGreaterEqual(count, 2)

    def test_retired_count(self):
        count = sum(1 for m in self.models.values() if m["status"] == "RETIRED_CURRENT_ENDPOINT")
        self.assertGreaterEqual(count, 2)

    def test_total_models_reasonable(self):
        self.assertGreaterEqual(len(self.models), 15)
        self.assertLessEqual(len(self.models), 100)


if __name__ == "__main__":
    unittest.main()
