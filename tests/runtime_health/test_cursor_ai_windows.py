"""
Tests: GO_OPT_TRADING_RUNTIME_HEALTH_CURSOR_AI_WINDOWS_ATTACH_01

Verifies that cursor-ai is treated as a Windows machine throughout the fleet:
- os_family declared in machine_runtime_map.yml
- build_config_from_scope: empty services/timers, Windows data_dir resolution
- check_forbidden_services: PASS without calling systemctl on Windows
- fleet_orchestrator: SSH PowerShell command used for cursor-ai, not Linux cat
- Linux machines (admin-trading, db-layer, fantome) unchanged
"""

import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from modules.runtime_health.machine_map import MachineMap
from modules.runtime_health import fleet_orchestrator as fo


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_real_map() -> MachineMap:
    map_path = REPO_ROOT / "config" / "machine_runtime_map.yml"
    return MachineMap.load(str(map_path))


def _cursor_ai_scope(mm: MachineMap) -> dict:
    scope = mm.scope_for("cursor-ai")
    assert scope is not None, "cursor-ai not found in machine_runtime_map.yml"
    return scope


# ---------------------------------------------------------------------------
# 1. machine_runtime_map.yml — cursor-ai os_family
# ---------------------------------------------------------------------------

class TestCursorAiMapDeclaration(unittest.TestCase):

    def setUp(self):
        self.mm = _load_real_map()
        self.scope = _cursor_ai_scope(self.mm)

    def test_hostname_alias_resolves_to_cursor_ai_scope(self):
        """DESKTOP-1KDQTBH must resolve to the cursor-ai scope."""
        scope = self.mm.scope_for("DESKTOP-1KDQTBH")
        self.assertIsNotNone(scope, "DESKTOP-1KDQTBH not found via hostname_aliases")
        self.assertEqual(scope.get("role"), "ide_patch_operator")

    def test_canonical_name_for_alias(self):
        self.assertEqual(self.mm.canonical_name_for("DESKTOP-1KDQTBH"), "cursor-ai")

    def test_canonical_name_for_direct(self):
        self.assertEqual(self.mm.canonical_name_for("cursor-ai"), "cursor-ai")

    def test_os_family_is_windows(self):
        self.assertEqual(self.scope.get("os_family", "").lower(), "windows")

    def test_repo_root_candidates_present(self):
        candidates = self.scope.get("repo_root_candidates", [])
        self.assertGreater(len(candidates), 0)
        # Must include the confirmed repo root
        joined = " ".join(candidates)
        self.assertIn("opt-trading", joined.lower())

    def test_data_dir_candidates_present(self):
        candidates = self.scope.get("data_dir_candidates", [])
        self.assertGreater(len(candidates), 0)
        for c in candidates:
            self.assertIn("runtime_health", c)

    def test_required_paths_empty(self):
        # No Linux paths in required_paths
        self.assertEqual(self.scope.get("required_paths", []), [])

    def test_required_venvs_empty(self):
        # No /opt/trading/venv
        self.assertEqual(self.scope.get("required_venvs", []), [])

    def test_required_services_empty(self):
        self.assertEqual(self.scope.get("required_services", []), [])

    def test_required_timers_empty(self):
        self.assertEqual(self.scope.get("required_timers", []), [])

    def test_no_opt_trading_in_required_paths(self):
        for entry in self.scope.get("required_paths", []):
            path = entry if isinstance(entry, str) else entry.get("path", "")
            self.assertNotIn("/opt/trading", path,
                             "Linux /opt/trading must not appear in cursor-ai required_paths")


# ---------------------------------------------------------------------------
# 2. build_config_from_scope — Windows data_dir resolution
# ---------------------------------------------------------------------------

class TestBuildConfigWindows(unittest.TestCase):

    def setUp(self):
        self.mm = _load_real_map()
        self.scope = _cursor_ai_scope(self.mm)
        self.base_cfg = {
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
                    "optional": ["/var/log/trading/webhook.log"],
                },
                "since": "10 minutes ago",
            },
            "http": {"required": [], "optional": []},
            "artifacts": {"required": [], "optional": []},
            "orchestrator": {"tmux_sessions": {"optional": ["openclaw", "trading"]}},
        }

    def test_services_empty_for_windows(self):
        cfg = self.mm.build_config_from_scope(self.scope, self.base_cfg)
        self.assertEqual(cfg["services"]["required"], [])
        self.assertEqual(cfg["services"]["optional"], [])

    def test_timers_empty_for_windows(self):
        cfg = self.mm.build_config_from_scope(self.scope, self.base_cfg)
        self.assertEqual(cfg["timers"]["required"], [])
        self.assertEqual(cfg["timers"]["optional"], [])

    def test_venvs_empty_for_windows(self):
        cfg = self.mm.build_config_from_scope(self.scope, self.base_cfg)
        self.assertEqual(cfg["venvs"], [])

    def test_linux_log_files_cleared_on_windows(self):
        cfg = self.mm.build_config_from_scope(self.scope, self.base_cfg)
        log_files = cfg.get("logs", {}).get("log_files", {})
        self.assertEqual(log_files.get("optional", []), [])

    def test_data_dir_resolved_from_candidates(self):
        # Simulate USERPROFILE pointing to a tmp dir that exists
        import tempfile, os
        with tempfile.TemporaryDirectory() as tmp:
            # Patch candidates so first one exists
            scope = dict(self.scope)
            scope["data_dir_candidates"] = [tmp + "\\runtime_health", "C:\\fallback"]
            with patch.dict(os.environ, {}, clear=False):
                cfg = self.mm.build_config_from_scope(scope, self.base_cfg)
            # Should pick the existing candidate
            self.assertEqual(cfg["data_dir"], tmp + "\\runtime_health")

    def test_data_dir_uses_first_candidate_when_none_exist(self):
        import os
        scope = dict(self.scope)
        scope["data_dir_candidates"] = [
            "C:\\nonexistent_abc123\\runtime_health",
            "C:\\also_missing\\runtime_health",
        ]
        cfg = self.mm.build_config_from_scope(scope, self.base_cfg)
        self.assertEqual(cfg["data_dir"], "C:\\nonexistent_abc123\\runtime_health")

    def test_tmux_sessions_cleared_via_scope(self):
        # cursor-ai scope declares optional_tmux_sessions: [] → orchestrator block cleared
        cfg = self.mm.build_config_from_scope(self.scope, self.base_cfg)
        tmux_opt = cfg.get("orchestrator", {}).get("tmux_sessions", {}).get("optional", ["nonempty"])
        self.assertEqual(tmux_opt, [])


# ---------------------------------------------------------------------------
# 3. check_forbidden_services — PASS without systemctl on Windows
# ---------------------------------------------------------------------------

class TestForbiddenServicesWindows(unittest.TestCase):

    def setUp(self):
        self.mm = _load_real_map()
        self.scope = _cursor_ai_scope(self.mm)

    def test_forbidden_services_pass_without_systemctl(self):
        # _run should NOT be called for Windows machines
        with patch("modules.runtime_health.machine_map.MachineMap.check_forbidden_services",
                   wraps=self.mm.check_forbidden_services):
            with patch("modules.runtime_health.healthcheck._run") as mock_run:
                results = self.mm.check_forbidden_services(self.scope)

        # All results must be PASS
        statuses = [r["status"] for r in results]
        self.assertTrue(all(s == "PASS" for s in statuses),
                        f"Expected all PASS, got {statuses}")
        # systemctl must not have been called
        for c in mock_run.call_args_list:
            cmd = c[0][0] if c[0] else c[1].get("cmd", [])
            self.assertNotIn("systemctl", str(cmd),
                             "systemctl must not be called for Windows machine")

    def test_forbidden_services_detail_mentions_windows(self):
        results = self.mm.check_forbidden_services(self.scope)
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertIn("Windows", r.get("detail", ""),
                          f"Expected Windows mention in detail: {r}")

    def test_linux_machine_still_calls_systemctl(self):
        """admin-trading (Linux) must still go through systemctl path."""
        linux_scope = self.mm.scope_for("admin-trading")
        self.assertIsNotNone(linux_scope)
        with patch("modules.runtime_health.healthcheck._run") as mock_run:
            mock_run.return_value = (1, "inactive", "")
            self.mm.check_forbidden_services(linux_scope)
        # systemctl must have been called
        called_cmds = [str(c[0][0]) for c in mock_run.call_args_list]
        self.assertTrue(any("systemctl" in cmd for cmd in called_cmds),
                        "systemctl must be called for Linux machine forbidden check")


# ---------------------------------------------------------------------------
# 4. fleet_orchestrator — SSH PowerShell for cursor-ai, not Linux cat
# ---------------------------------------------------------------------------

class TestFleetOrchestratorWindowsDispatch(unittest.TestCase):

    def _make_scope(self, os_family="windows"):
        return {
            "os_family": os_family,
            "data_dir_candidates": [
                "%USERPROFILE%\\opt-trading\\data\\runtime_health",
                "C:\\Users\\ghost\\opt-trading\\data\\runtime_health",
            ],
        }

    def test_collect_machine_status_uses_ssh_windows(self):
        """collect_machine_status dispatches to _collect_via_ssh_windows for Windows."""
        fake_json = json.dumps({"overall_status": "PASS", "timestamp": "2026-05-19T00:00:00+00:00"})
        with patch.object(fo, "_collect_via_ssh_windows", return_value=json.loads(fake_json)) as mock_win, \
             patch.object(fo, "_collect_via_sshfs", return_value=None) as mock_sshfs, \
             patch.object(fo, "_collect_via_ssh", return_value=None) as mock_ssh:
            result = fo.collect_machine_status(
                "cursor-ai", "admin-trading", "/opt/trading/data/runtime_health",
                machine_scope=self._make_scope("windows"),
            )

        mock_win.assert_called_once()
        mock_sshfs.assert_not_called()
        mock_ssh.assert_not_called()
        self.assertTrue(result["reachable"])
        self.assertEqual(result["source"], "ssh_windows")

    def test_collect_machine_status_linux_not_affected(self):
        """Linux machines still use sshfs → ssh, never ssh_windows."""
        linux_scope = {"os_family": "linux"}
        fake_json = {"overall_status": "PASS", "timestamp": "2026-05-19T00:00:00+00:00"}
        with patch.object(fo, "_collect_via_ssh_windows", return_value=None) as mock_win, \
             patch.object(fo, "_collect_via_sshfs", return_value=fake_json) as mock_sshfs:
            result = fo.collect_machine_status(
                "fantome", "admin-trading", "/opt/trading/data/runtime_health",
                machine_scope=linux_scope,
            )

        mock_win.assert_not_called()
        mock_sshfs.assert_called_once()
        self.assertEqual(result["source"], "sshfs")

    def test_ssh_windows_builds_powershell_command(self):
        """_collect_via_ssh_windows passes 'powershell' to SSH, not 'cat'."""
        candidates = [
            "%USERPROFILE%\\opt-trading\\data\\runtime_health",
            "C:\\Users\\ghost\\opt-trading\\data\\runtime_health",
        ]
        captured = []

        def fake_run(cmd, timeout=8):
            captured.append(cmd)
            return (1, "", "not found")

        with patch.object(fo, "_run", side_effect=fake_run):
            fo._collect_via_ssh_windows("cursor-ai", candidates)

        self.assertGreater(len(captured), 0)
        cmd = captured[0]
        self.assertIn("powershell", cmd)
        self.assertNotIn("cat", cmd)
        self.assertNotIn("/opt/trading", " ".join(cmd))

    def test_ssh_windows_converts_percent_vars(self):
        """_collect_via_ssh_windows encodes %USERPROFILE% → $env:USERPROFILE in base64 payload."""
        import base64
        captured = []

        def fake_run(cmd, timeout=8):
            captured.append(cmd)
            return (1, "", "")

        with patch.object(fo, "_run", side_effect=fake_run):
            fo._collect_via_ssh_windows("cursor-ai", ["%USERPROFILE%\\opt-trading\\data\\runtime_health"])

        self.assertGreater(len(captured), 0)
        cmd = captured[0]
        # Command must use -EncodedCommand
        self.assertIn("-EncodedCommand", cmd)
        # Decode the base64 payload and verify $env:USERPROFILE is present
        idx = cmd.index("-EncodedCommand") + 1
        decoded = base64.b64decode(cmd[idx]).decode("utf-16-le")
        self.assertIn("$env:USERPROFILE", decoded)
        self.assertNotIn("%USERPROFILE%", decoded)

    def test_run_fleet_passes_scope_to_collect(self):
        """run_fleet passes machine_scope so Windows machines get correct dispatch."""
        mm = _load_real_map()
        cursor_scope = _cursor_ai_scope(mm)
        self.assertEqual(cursor_scope.get("os_family", "").lower(), "windows")

        called_scopes = {}

        original_collect = fo.collect_machine_status

        def capturing_collect(machine, hostname, data_dir, machine_scope=None):
            called_scopes[machine] = machine_scope
            return {
                "machine": machine,
                "source": "none",
                "reachable": False,
                "status": "WARN",
                "detail": "mocked",
                "overall_status": None,
                "timestamp": None,
                "age_minutes": None,
            }

        with patch.object(fo, "collect_machine_status", side_effect=capturing_collect):
            fo.run_fleet(
                str(REPO_ROOT / "config" / "machine_runtime_map.yml"),
                "/tmp/fleet_test_data",
                dry_run=True,
            )

        self.assertIn("cursor-ai", called_scopes)
        scope_passed = called_scopes["cursor-ai"]
        self.assertIsNotNone(scope_passed)
        self.assertEqual(scope_passed.get("os_family", "").lower(), "windows")

        # Linux machines must also have their scope passed
        for linux_machine in ("admin-trading", "db-layer", "fantome"):
            self.assertIn(linux_machine, called_scopes)
            linux_scope = called_scopes[linux_machine]
            self.assertIsNotNone(linux_scope)
            self.assertNotEqual(linux_scope.get("os_family", "linux").lower(), "windows")


# ---------------------------------------------------------------------------
# 5. check_venv — Windows Scripts/ path support
# ---------------------------------------------------------------------------

class TestCheckVenvWindows(unittest.TestCase):

    def test_venv_found_via_scripts_python_exe(self):
        """check_venv detects Windows venv via Scripts/python.exe."""
        import tempfile, os
        from modules.runtime_health.healthcheck import check_venv

        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "Scripts"
            scripts.mkdir()
            py_exe = scripts / "python.exe"
            py_exe.write_text("# fake")

            with patch("modules.runtime_health.healthcheck._run") as mock_run:
                mock_run.return_value = (0, "Python 3.12.0", "")
                result = check_venv(tmp, label="win_venv", required=True)

        self.assertEqual(result["status"], "PASS")
        mock_run.assert_called_once()
        called_cmd = mock_run.call_args[0][0]
        self.assertIn("python.exe", str(called_cmd))

    def test_venv_missing_returns_fail(self):
        from modules.runtime_health.healthcheck import check_venv
        result = check_venv("/nonexistent_path_xyz", label="missing", required=True)
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["exists"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
