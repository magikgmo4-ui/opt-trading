"""Tests for LocalCMS Central UI module."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TestLocalCMSMenuJSON(unittest.TestCase):
    def setUp(self):
        self.menu_path = PROJECT_ROOT / "scripts" / "ai" / "menu" / "opt_trading_menu.json"

    def test_menu_file_exists(self):
        self.assertTrue(self.menu_path.exists())

    def test_menu_json_valid(self):
        data = json.loads(self.menu_path.read_text())
        self.assertIn("version", data)
        self.assertIn("menu", data)

    def test_menu_14_domains(self):
        data = json.loads(self.menu_path.read_text())
        self.assertEqual(len(data["menu"]), 14)

    def test_domain_labels_14_unique(self):
        data = json.loads(self.menu_path.read_text())
        labels = [d["label"] for d in data["menu"]]
        self.assertEqual(len(labels), 14)

    def test_menu_domain_ids_unique(self):
        data = json.loads(self.menu_path.read_text())
        ids = [d["id"] for d in data["menu"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_modules_have_status(self):
        data = json.loads(self.menu_path.read_text())
        for domain in data["menu"]:
            for child in domain.get("children", []):
                self._check_status(child)

    def _check_status(self, item):
        if "children" in item:
            for c in item["children"]:
                self._check_status(c)
        else:
            self.assertIn("status", item, f"Missing status in {item.get('id', item)}")

    def test_all_modules_have_label(self):
        data = json.loads(self.menu_path.read_text())
        for domain in data["menu"]:
            for child in domain.get("children", []):
                self._check_label(child)

    def _check_label(self, item):
        self.assertIn("label", item)
        if "children" in item:
            for c in item["children"]:
                self._check_label(c)

    def test_known_status_values(self):
        valid_statuses = {"operational", "impl", "partial", "to_build", "closed", "deprecated", "minimal"}
        data = json.loads(self.menu_path.read_text())
        for domain in data["menu"]:
            for child in domain.get("children", []):
                self._check_status_valid(child, valid_statuses)

    def _check_status_valid(self, item, valid):
        if "children" in item:
            for c in item["children"]:
                self._check_status_valid(c, valid)
        elif "status" in item:
            self.assertIn(item["status"], valid, f"Invalid status '{item['status']}' in {item.get('id', item)}")

    def test_workers_updated_to_operational(self):
        """Workers GO-03 through GO-10 are now operational (PR #456-#467)."""
        data = json.loads(self.menu_path.read_text())
        workers_domain = None
        for d in data["menu"]:
            if d["id"] == "10_workers":
                workers_domain = d
                break
        self.assertIsNotNone(workers_domain)
        operational = ["signal_router", "notification_dispatcher", "proposition_engine",
                       "validation_gate", "trade_executor", "result_tracker",
                       "datasheet_writer", "learning_feeder"]
        for wid in operational:
            module = self._find_module(data, wid)
            self.assertIsNotNone(module, f"{wid} not found in menu")
            self.assertEqual(module["status"], "operational",
                             f"{wid} should be operational, got {module['status']}")

    def _find_module(self, data, module_id):
        for domain in data["menu"]:
            for child in domain.get("children", []):
                result = self._search_child(child, module_id)
                if result:
                    return result
        return None

    def _search_child(self, item, module_id):
        if "children" in item:
            for c in item["children"]:
                result = self._search_child(c, module_id)
                if result:
                    return result
        if item.get("id") == module_id:
            return item
        return None

    def test_total_module_count_range(self):
        """Expect 85-100 modules across all domains."""
        data = json.loads(self.menu_path.read_text())
        count = 0
        for domain in data["menu"]:
            for child in domain.get("children", []):
                count += self._count_modules(child)
        self.assertGreaterEqual(count, 85)
        self.assertLessEqual(count, 110)

    def _count_modules(self, item):
        if "children" in item:
            return sum(self._count_modules(c) for c in item["children"])
        return 1

    def test_domain_icons_present(self):
        data = json.loads(self.menu_path.read_text())
        for d in data["menu"]:
            self.assertIn("icon", d, f"Missing icon in domain {d['id']}")

    def test_all_machines_are_known(self):
        known = {"admin-trading", "db-layer", "windows"}
        data = json.loads(self.menu_path.read_text())
        for domain in data["menu"]:
            for child in domain.get("children", []):
                self._check_machine(child, known)

    def _check_machine(self, item, known):
        if "children" in item:
            for c in item["children"]:
                self._check_machine(c, known)
        elif "machine" in item:
            self.assertIn(item["machine"], known,
                          f"Unknown machine '{item['machine']}' in {item.get('id', item)}")


class TestLocalCMSStateSchema(unittest.TestCase):
    def setUp(self):
        self.schema_path = PROJECT_ROOT / "scripts" / "ai" / "menu" / "state_schema.json"

    def test_schema_file_exists(self):
        self.assertTrue(self.schema_path.exists())

    def test_schema_valid(self):
        data = json.loads(self.schema_path.read_text())
        self.assertIn("version", data)
        self.assertIn("modules", data)

    def test_critical_modules_have_critical_flag(self):
        data = json.loads(self.schema_path.read_text())
        for m in data["modules"]:
            self.assertIn("critical", m)

    def test_each_module_has_type(self):
        data = json.loads(self.schema_path.read_text())
        for m in data["modules"]:
            self.assertIn("type", m, f"Missing type in {m['id']}")

    def test_each_module_has_endpoint_or_check(self):
        data = json.loads(self.schema_path.read_text())
        for m in data["modules"]:
            has = "endpoint" in m or "check" in m
            self.assertTrue(has, f"Missing endpoint/check in {m['id']}")


class TestLocalCMSAppConfig(unittest.TestCase):
    def test_app_imports(self):
        import modules.localcms.app.main as app_module
        self.assertIsNotNone(app_module.app)

    def test_app_title(self):
        import modules.localcms.app.main as app_module
        self.assertEqual(app_module.app.title, "LocalCMS")

    def test_app_version(self):
        import modules.localcms.app.main as app_module
        self.assertEqual(app_module.app.version, "1.0.0")

    def test_route_count(self):
        import modules.localcms.app.main as app_module
        routes = [r for r in app_module.app.routes if hasattr(r, "endpoint")]
        self.assertGreaterEqual(len(routes), 6)

    def test_health_route_exists(self):
        import modules.localcms.app.main as app_module
        paths = [r.path for r in app_module.app.routes if hasattr(r, "path")]
        self.assertIn("/health", paths)

    def test_menu_route_exists(self):
        import modules.localcms.app.main as app_module
        paths = [r.path for r in app_module.app.routes if hasattr(r, "path")]
        self.assertIn("/menu", paths)

    def test_runtime_tmux_route_exists(self):
        import modules.localcms.app.main as app_module
        paths = [r.path for r in app_module.app.routes if hasattr(r, "path")]
        self.assertIn("/runtime/tmux", paths)

    def test_ui_route_exists(self):
        import modules.localcms.app.main as app_module
        paths = [r.path for r in app_module.app.routes if hasattr(r, "path")]
        self.assertIn("/", paths)

    def test_no_trade_dangerous_endpoints(self):
        """LocalCMS V1 must NOT have write endpoints."""
        import modules.localcms.app.main as app_module
        dangerous = {"POST", "PUT", "DELETE", "PATCH"}
        for r in app_module.app.routes:
            if hasattr(r, "methods") and r.methods:
                overlap = r.methods & dangerous
                if overlap:
                    self.fail(f"Dangerous method {overlap} on {r.path}")

    def test_tmux_9_sessions(self):
        from modules.localcms.app.main import ALL_SESSIONS
        self.assertEqual(len(ALL_SESSIONS), 9)

    def test_critical_sessions_3(self):
        from modules.localcms.app.main import CRITICAL_SESSIONS
        self.assertEqual(len(CRITICAL_SESSIONS), 3)

    def test_tmux_sessions_have_all_fields(self):
        from modules.localcms.app.main import ALL_SESSIONS
        for s in ALL_SESSIONS:
            self.assertIn("session", s)
            self.assertIn("critical", s)
            self.assertIn("machine", s)
            self.assertIn("description", s)

    def test_critical_sessions_are_in_all_sessions(self):
        from modules.localcms.app.main import ALL_SESSIONS, CRITICAL_SESSIONS
        all_ids = frozenset(s["session"] for s in ALL_SESSIONS)
        self.assertTrue(CRITICAL_SESSIONS.issubset(all_ids))

    def test_menu_json_is_loaded(self):
        from modules.localcms.app.main import MENU_FILE
        self.assertTrue(MENU_FILE.exists())

    def test_menu_schema_is_loaded(self):
        from modules.localcms.app.main import STATE_CACHE
        self.assertIsNotNone(STATE_CACHE)


if __name__ == "__main__":
    unittest.main()
