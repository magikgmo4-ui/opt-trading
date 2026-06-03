"""
Tests: GO_OPT_TRADING_RUNTIME_HEALTH_FLEET_WARN_CLASSIFICATION_01

Verifies that admin-trading, db-layer, and student scope changes correctly
suppress base-config false positives via optional_http_checks / optional_artifact_paths
/ optional_log_files / optional_tmux_sessions.
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from modules.runtime_health.machine_map import MachineMap

_MAP_PATH = str(REPO_ROOT / "config" / "machine_runtime_map.yml")

BASE_CFG = {
    "data_dir": "/opt/trading/data/runtime_health",
    "services": {"required": [], "optional": []},
    "timers": {"required": [], "optional": []},
    "venvs": [],
    "ports": {"required": [], "optional": []},
    "paths": {"required": [], "optional": []},
    "env": {"required": [], "optional": []},
    "logs": {
        "journal_units": [],
        "log_files": {
            "optional": [
                "/var/log/trading/webhook.log",
                "/var/log/trading/perf.log",
            ],
        },
        "since": "10 minutes ago",
    },
    "http": {
        "required": [],
        "optional": [
            {"label": "webhook_health", "url": "http://127.0.0.1:8000/health"},
            {"label": "perf_summary", "url": "http://127.0.0.1:8010/perf/summary"},
        ],
    },
    "artifacts": {
        "optional": [
            {"path": "/opt/trading/data/deskpro/vision", "label": "desk_vision_dir", "max_age_minutes": 120},
            {"path": "/opt/trading/desk/snapshots", "label": "desk_snapshots_dir", "max_age_minutes": 120},
        ]
    },
    "orchestrator": {
        "tmux_sessions": {
            "optional": ["openclaw", "trading", "desk"],
        }
    },
}


def _mm() -> MachineMap:
    return MachineMap.load(_MAP_PATH)


def _cfg(machine: str) -> dict:
    mm = _mm()
    scope = mm.scope_for(machine)
    assert scope is not None, f"{machine} not in map"
    return mm.build_config_from_scope(scope, dict(BASE_CFG))


# ---------------------------------------------------------------------------
# admin-trading
# ---------------------------------------------------------------------------

class TestAdminTradingScope(unittest.TestCase):

    def setUp(self):
        self.cfg = _cfg("admin-trading")

    def test_http_checks_cleared(self):
        """optional_http_checks: [] removes base-config webhook_health false positive."""
        self.assertEqual(self.cfg["http"]["optional"], [])
        self.assertEqual(self.cfg["http"]["required"], [])

    def test_log_files_cleared(self):
        """optional_log_files: [] removes /var/log/trading/*.log false positives."""
        self.assertEqual(self.cfg["logs"]["log_files"].get("optional", []), [])

    def test_tmux_sessions_explicit(self):
        """optional_tmux_sessions preserved for visibility (openclaw/trading/desk)."""
        sessions = self.cfg["orchestrator"]["tmux_sessions"]["optional"]
        self.assertIn("openclaw", sessions)
        self.assertIn("trading", sessions)
        self.assertIn("desk", sessions)

    def test_log_units_preserved(self):
        """journal_units still present for real log monitoring."""
        units = self.cfg["logs"]["journal_units"]
        self.assertGreater(len(units), 0)


# ---------------------------------------------------------------------------
# db-layer
# ---------------------------------------------------------------------------

class TestDbLayerScope(unittest.TestCase):

    def setUp(self):
        self.cfg = _cfg("db-layer")

    def test_http_checks_cleared(self):
        self.assertEqual(self.cfg["http"]["optional"], [])

    def test_artifact_paths_cleared(self):
        self.assertEqual(self.cfg["artifacts"].get("optional", []), [])

    def test_log_files_cleared(self):
        self.assertEqual(self.cfg["logs"]["log_files"].get("optional", []), [])

    def test_tmux_sessions_cleared(self):
        sessions = self.cfg["orchestrator"]["tmux_sessions"]["optional"]
        self.assertEqual(sessions, [])

    def test_linux_machines_unaffected_by_windows_path(self):
        """db-layer must not have os_family=windows."""
        mm = _mm()
        scope = mm.scope_for("db-layer")
        self.assertNotEqual(scope.get("os_family", "linux").lower(), "windows")


# ---------------------------------------------------------------------------
# student
# ---------------------------------------------------------------------------

class TestStudentScope(unittest.TestCase):

    def setUp(self):
        self.cfg = _cfg("student")

    def test_http_checks_cleared(self):
        self.assertEqual(self.cfg["http"]["optional"], [])

    def test_artifact_paths_cleared(self):
        self.assertEqual(self.cfg["artifacts"].get("optional", []), [])

    def test_log_files_cleared(self):
        self.assertEqual(self.cfg["logs"]["log_files"].get("optional", []), [])

    def test_tmux_sessions_cleared(self):
        sessions = self.cfg["orchestrator"]["tmux_sessions"]["optional"]
        self.assertEqual(sessions, [])


# ---------------------------------------------------------------------------
# Cross-machine: cursor-ai and fantome unaffected
# ---------------------------------------------------------------------------

class TestOtherMachinesUnchanged(unittest.TestCase):

    def test_cursor_ai_still_windows(self):
        mm = _mm()
        scope = mm.scope_for("cursor-ai")
        self.assertEqual(scope.get("os_family", "").lower(), "windows")

    def test_fantome_tmux_sessions_empty(self):
        mm = _mm()
        scope = mm.scope_for("fantome")
        self.assertIn("optional_tmux_sessions", scope)
        self.assertEqual(scope["optional_tmux_sessions"], [])

    def test_fantome_runtime_health_timer_present(self):
        mm = _mm()
        scope = mm.scope_for("fantome")
        self.assertIn("optional_timers", scope)
        self.assertIn("opt-trading-runtime-health.timer", scope["optional_timers"])

    def test_db_layer_fleet_orchestrator_timer_present(self):
        mm = _mm()
        scope = mm.scope_for("db-layer")
        self.assertIn("optional_timers", scope)
        self.assertIn("opt-trading-fleet-orchestrator.timer", scope["optional_timers"])

    def test_all_machines_present(self):
        mm = _mm()
        for machine in ["admin-trading", "db-layer", "cursor-ai", "fantome", "student"]:
            self.assertIsNotNone(mm.scope_for(machine), f"{machine} missing from map")


if __name__ == "__main__":
    unittest.main(verbosity=2)
