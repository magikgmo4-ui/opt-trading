"""Mobile operator smoke tests — python3 -m unittest"""
from __future__ import annotations
import json
import subprocess
import sys
import unittest
from shutil import which
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.tmux.health_check import ALL_SESSIONS, CRITICAL_SESSIONS
from modules.openclaw_tmux_operator.scripts.health_aggregate import run_aggregate

_CMD = str(PROJECT_ROOT / "modules" / "openclaw_tmux_operator" / "scripts" / "cmd.sh")
_MOBILE_TARGETS = [
    ("db-layer", "openclaw-core"),
    ("db-layer", "fleet-status"),
    ("admin-trading", "desk-pro"),
    ("admin-trading", "screeners"),
]
_MOBILE_SESSIONS = {s for _, s in _MOBILE_TARGETS}


def _run(args: list[str]) -> tuple[int, str]:
    r = subprocess.run(["bash", _CMD] + args, capture_output=True, text=True, timeout=10)
    return r.returncode, r.stdout + r.stderr


def _bash_usable() -> bool:
    if which("bash") is None:
        return False
    try:
        r = subprocess.run(["bash", "-lc", "echo ok"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0 and r.stdout.strip() == "ok"
    except Exception:
        return False


_BASH_USABLE = _bash_usable()


# ---------------------------------------------------------------------------
# T1 — attach-hint correctness
# ---------------------------------------------------------------------------

class TestAttachHint(unittest.TestCase):

    def setUp(self):
        if not _BASH_USABLE:
            self.skipTest("bash unavailable in this environment")

    def _hint(self, host: str, session: str) -> str:
        rc, out = _run(["attach-hint", host, session])
        self.assertEqual(rc, 0, f"attach-hint exited {rc}: {out}")
        return out

    def test_db_layer_openclaw_core(self):
        out = self._hint("db-layer", "openclaw-core")
        self.assertIn("ssh db-layer", out)
        self.assertIn("tmux attach -t openclaw-core", out)

    def test_db_layer_fleet_status(self):
        out = self._hint("db-layer", "fleet-status")
        self.assertIn("ssh db-layer", out)
        self.assertIn("tmux attach -t fleet-status", out)

    def test_admin_trading_desk_pro(self):
        out = self._hint("admin-trading", "desk-pro")
        self.assertIn("ssh admin-trading", out)
        self.assertIn("tmux attach -t desk-pro", out)

    def test_admin_trading_screeners(self):
        out = self._hint("admin-trading", "screeners")
        self.assertIn("ssh admin-trading", out)
        self.assertIn("tmux attach -t screeners", out)

    def test_hint_has_two_lines(self):
        rc, out = _run(["attach-hint", "db-layer", "openclaw-core"])
        self.assertEqual(rc, 0)
        lines = [l for l in out.strip().splitlines() if l.strip()]
        self.assertEqual(len(lines), 2)

    def test_missing_host_exits_nonzero(self):
        rc, out = _run(["attach-hint"])
        self.assertNotEqual(rc, 0)

    def test_missing_session_exits_nonzero(self):
        rc, out = _run(["attach-hint", "db-layer"])
        self.assertNotEqual(rc, 0)


# ---------------------------------------------------------------------------
# T2 — mobile sessions in ALL_SESSIONS
# ---------------------------------------------------------------------------

class TestMobileSessionsInRegistry(unittest.TestCase):

    def test_openclaw_core_registered(self):
        self.assertIn("openclaw-core", ALL_SESSIONS)

    def test_fleet_status_registered(self):
        self.assertIn("fleet-status", ALL_SESSIONS)

    def test_desk_pro_registered(self):
        self.assertIn("desk-pro", ALL_SESSIONS)

    def test_screeners_registered(self):
        self.assertIn("screeners", ALL_SESSIONS)

    def test_all_mobile_targets_registered(self):
        missing = _MOBILE_SESSIONS - ALL_SESSIONS
        self.assertEqual(missing, set(), f"Not in ALL_SESSIONS: {missing}")

    def test_openclaw_core_is_critical(self):
        self.assertIn("openclaw-core", CRITICAL_SESSIONS)

    def test_screeners_is_critical(self):
        self.assertIn("screeners", CRITICAL_SESSIONS)


# ---------------------------------------------------------------------------
# T3 — health-aggregate dry-run (what mobile user reads)
# ---------------------------------------------------------------------------

class TestHealthAggregateForMobile(unittest.TestCase):

    def setUp(self):
        r = subprocess.run(
            [
                sys.executable,
                str(PROJECT_ROOT / "modules" / "openclaw_tmux_operator" / "scripts" / "health_aggregate.py"),
                "--dry-run",
                "--machines",
                "db-layer,admin-trading",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.rc = r.returncode
        self.out = r.stdout + r.stderr
        self.data = json.loads(r.stdout) if r.returncode == 0 else {}

    def test_exit_zero(self):
        self.assertEqual(self.rc, 0, self.out)

    def test_json_parseable(self):
        self.assertIsInstance(self.data, dict)

    def test_has_machines_key(self):
        self.assertIn("machines", self.data)

    def test_total_positive(self):
        self.assertGreater(self.data.get("total", 0), 0)

    def test_has_timestamp(self):
        self.assertIn("timestamp", self.data)
        self.assertIn("T", self.data["timestamp"])

    def test_has_reachable_machines(self):
        self.assertIn("reachable_machines", self.data)

    def test_machines_keys_match_total(self):
        self.assertEqual(len(self.data["machines"]), self.data["total"])


# ---------------------------------------------------------------------------
# T4 — cmd.sh usage contains mobile-relevant commands
# ---------------------------------------------------------------------------

class TestCmdUsageForMobile(unittest.TestCase):

    def setUp(self):
        if not _BASH_USABLE:
            self.skipTest("bash unavailable in this environment")
        rc, self.usage = _run([])
        # exit 2 is expected for no-args usage
        self.assertIn(rc, (0, 2))

    def test_attach_hint_in_usage(self):
        self.assertIn("attach-hint", self.usage)

    def test_health_aggregate_in_usage(self):
        self.assertIn("health-aggregate", self.usage)

    def test_session_logs_in_usage(self):
        self.assertIn("session-logs", self.usage)

    def test_tmux_status_in_usage(self):
        self.assertIn("tmux-status", self.usage)

    def test_machine_status_in_usage(self):
        self.assertIn("machine-status", self.usage)


# ---------------------------------------------------------------------------
# T5 — mobile runbook doc integrity
# ---------------------------------------------------------------------------

class TestMobileRunbookDoc(unittest.TestCase):

    _RUNBOOK = (
        PROJECT_ROOT
        / "docs/chantiers"
        / "GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01"
        / "40_MOBILE_OPERATOR_ACCESS.md"
    )

    def setUp(self):
        self.content = self._RUNBOOK.read_text(encoding="utf-8")

    def test_runbook_exists(self):
        self.assertTrue(self._RUNBOOK.exists())

    def test_termius_mentioned(self):
        self.assertIn("Termius", self.content)

    def test_termux_mentioned(self):
        self.assertIn("Termux", self.content)

    def test_tmux_attach_documented(self):
        self.assertIn("tmux attach", self.content)

    def test_forbidden_commands_listed(self):
        self.assertIn("Interdits mobile", self.content)

    def test_no_secret_commands(self):
        self.assertNotIn("cat .env", self.content)
        self.assertNotIn("git push --force", self.content)


# ---------------------------------------------------------------------------
# T6 — health_aggregate injected (mobile reading multiple machines)
# ---------------------------------------------------------------------------

class TestMobileHealthAggregateInjected(unittest.TestCase):

    def setUp(self):
        injected = {
            "db-layer": {
                "tmux": {"reachable": True, "source": "injected",
                         "sessions": ["openclaw-core", "fleet-status"]},
                "health": {"overall_status": "PASS", "timestamp": "2026-05-19T12:00:00+00:00"},
            },
            "admin-trading": {
                "tmux": {"reachable": True, "source": "injected",
                         "sessions": ["desk-pro", "screeners"]},
                "health": None,
            },
        }
        self.report = run_aggregate(
            ["db-layer", "admin-trading"],
            hostname="test-host",
            injected_map=injected,
        )

    def test_both_machines_reachable(self):
        self.assertEqual(len(self.report["reachable_machines"]), 2)

    def test_db_layer_has_openclaw_core(self):
        sessions = self.report["machines"]["db-layer"]["tmux_sessions"]
        self.assertIn("openclaw-core", sessions)

    def test_db_layer_health_pass(self):
        status = self.report["machines"]["db-layer"]["runtime_health_status"]
        self.assertEqual(status, "PASS")

    def test_admin_trading_has_desk_pro(self):
        sessions = self.report["machines"]["admin-trading"]["tmux_sessions"]
        self.assertIn("desk-pro", sessions)

    def test_json_serializable(self):
        dumped = json.dumps(self.report)
        loaded = json.loads(dumped)
        self.assertEqual(loaded["total"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
