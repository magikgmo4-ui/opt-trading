"""health_aggregate tests — python3 -m unittest"""
from __future__ import annotations
import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.openclaw_tmux_operator.scripts.health_aggregate import (
    aggregate_machine,
    run_aggregate,
)

_FAKE_HOSTNAME = "test-host"
_MACHINES = ["db-layer", "admin-trading", "fantome"]


def _injected(sessions: list, health_status: str | None = None, reachable: bool = True) -> dict:
    health = None
    if health_status is not None:
        health = {
            "overall_status": health_status,
            "timestamp": "2026-05-19T12:00:00+00:00",
        }
    return {
        "tmux": {"reachable": reachable, "source": "injected", "sessions": sessions},
        "health": health,
    }


# ---------------------------------------------------------------------------
# run_aggregate — empty machine list
# ---------------------------------------------------------------------------

class TestRunAggregateEmpty(unittest.TestCase):

    def setUp(self):
        self.report = run_aggregate([], hostname=_FAKE_HOSTNAME)

    def test_total_zero(self):
        self.assertEqual(self.report["total"], 0)

    def test_machines_empty(self):
        self.assertEqual(self.report["machines"], {})

    def test_reachable_empty(self):
        self.assertEqual(self.report["reachable_machines"], [])

    def test_unreachable_empty(self):
        self.assertEqual(self.report["unreachable_machines"], [])

    def test_timestamp_present(self):
        self.assertIn("T", self.report["timestamp"])

    def test_orchestrator_host(self):
        self.assertEqual(self.report["orchestrator_host"], _FAKE_HOSTNAME)


# ---------------------------------------------------------------------------
# run_aggregate — all reachable, no health
# ---------------------------------------------------------------------------

class TestRunAggregateAllReachable(unittest.TestCase):

    def setUp(self):
        injected_map = {m: _injected(["openclaw-core", "desk-pro"]) for m in _MACHINES}
        self.report = run_aggregate(_MACHINES, hostname=_FAKE_HOSTNAME, injected_map=injected_map)

    def test_total(self):
        self.assertEqual(self.report["total"], len(_MACHINES))

    def test_all_reachable(self):
        self.assertEqual(sorted(self.report["reachable_machines"]), sorted(_MACHINES))

    def test_none_unreachable(self):
        self.assertEqual(self.report["unreachable_machines"], [])

    def test_machines_key_present(self):
        for m in _MACHINES:
            self.assertIn(m, self.report["machines"])

    def test_sessions_sorted(self):
        for m in _MACHINES:
            sessions = self.report["machines"][m]["tmux_sessions"]
            self.assertEqual(sessions, sorted(sessions))

    def test_no_health_status(self):
        for m in _MACHINES:
            self.assertIsNone(self.report["machines"][m]["runtime_health_status"])


# ---------------------------------------------------------------------------
# run_aggregate — one unreachable
# ---------------------------------------------------------------------------

class TestRunAggregateOneUnreachable(unittest.TestCase):

    def setUp(self):
        injected_map = {
            "db-layer": _injected(["openclaw-core"]),
            "admin-trading": _injected([], reachable=False),
            "fantome": _injected(["screeners"]),
        }
        self.report = run_aggregate(_MACHINES, hostname=_FAKE_HOSTNAME, injected_map=injected_map)

    def test_unreachable_identified(self):
        self.assertIn("admin-trading", self.report["unreachable_machines"])

    def test_reachable_does_not_include_unreachable(self):
        self.assertNotIn("admin-trading", self.report["reachable_machines"])

    def test_reachable_count(self):
        self.assertEqual(len(self.report["reachable_machines"]), 2)

    def test_machine_reachable_flag_false(self):
        self.assertFalse(self.report["machines"]["admin-trading"]["reachable"])


# ---------------------------------------------------------------------------
# aggregate_machine — local machine (hostname match)
# ---------------------------------------------------------------------------

class TestAggregateMachineLocal(unittest.TestCase):

    def setUp(self):
        self.result = aggregate_machine(
            _FAKE_HOSTNAME, _FAKE_HOSTNAME,
            injected=_injected(["openclaw-core", "screeners", "desk-pro"]),
        )

    def test_reachable_true(self):
        self.assertTrue(self.result["reachable"])

    def test_sessions_present(self):
        self.assertIn("openclaw-core", self.result["tmux_sessions"])

    def test_sessions_sorted(self):
        s = self.result["tmux_sessions"]
        self.assertEqual(s, sorted(s))

    def test_machine_field(self):
        self.assertEqual(self.result["machine"], _FAKE_HOSTNAME)


# ---------------------------------------------------------------------------
# aggregate_machine — remote, with health info
# ---------------------------------------------------------------------------

class TestAggregateMachineWithHealthInfo(unittest.TestCase):

    def setUp(self):
        self.result = aggregate_machine(
            "db-layer", _FAKE_HOSTNAME,
            injected=_injected(["openclaw-core"], health_status="PASS"),
        )

    def test_health_status_pass(self):
        self.assertEqual(self.result["runtime_health_status"], "PASS")

    def test_health_age_present(self):
        self.assertIsNotNone(self.result["runtime_health_age_minutes"])

    def test_health_age_positive(self):
        self.assertGreater(self.result["runtime_health_age_minutes"], 0)

    def test_reachable_true(self):
        self.assertTrue(self.result["reachable"])


# ---------------------------------------------------------------------------
# aggregate_machine — remote, no health
# ---------------------------------------------------------------------------

class TestAggregateMachineNoHealth(unittest.TestCase):

    def setUp(self):
        self.result = aggregate_machine(
            "fantome", _FAKE_HOSTNAME,
            injected=_injected([], health_status=None),
        )

    def test_health_status_none(self):
        self.assertIsNone(self.result["runtime_health_status"])

    def test_health_age_none(self):
        self.assertIsNone(self.result["runtime_health_age_minutes"])


# ---------------------------------------------------------------------------
# aggregate_machine — unreachable
# ---------------------------------------------------------------------------

class TestAggregateMachineUnreachable(unittest.TestCase):

    def setUp(self):
        self.result = aggregate_machine(
            "admin-trading", _FAKE_HOSTNAME,
            injected=_injected([], reachable=False),
        )

    def test_reachable_false(self):
        self.assertFalse(self.result["reachable"])

    def test_sessions_empty(self):
        self.assertEqual(self.result["tmux_sessions"], [])


# ---------------------------------------------------------------------------
# Output structure — required keys
# ---------------------------------------------------------------------------

class TestOutputStructure(unittest.TestCase):

    _MACHINE_KEYS = {
        "machine", "reachable", "tmux_source", "tmux_sessions",
        "runtime_health_status", "runtime_health_age_minutes",
    }
    _REPORT_KEYS = {
        "timestamp", "orchestrator_host", "machines",
        "reachable_machines", "unreachable_machines", "total",
    }

    def test_report_keys(self):
        report = run_aggregate(["db-layer"], hostname=_FAKE_HOSTNAME,
                               injected_map={"db-layer": _injected([])})
        self.assertTrue(self._REPORT_KEYS.issubset(set(report.keys())))

    def test_machine_keys(self):
        report = run_aggregate(["db-layer"], hostname=_FAKE_HOSTNAME,
                               injected_map={"db-layer": _injected([])})
        machine_data = report["machines"]["db-layer"]
        self.assertTrue(self._MACHINE_KEYS.issubset(set(machine_data.keys())))

    def test_report_json_serializable(self):
        report = run_aggregate(_MACHINES, hostname=_FAKE_HOSTNAME,
                               injected_map={m: _injected(["openclaw-core"]) for m in _MACHINES})
        dumped = json.dumps(report)
        loaded = json.loads(dumped)
        self.assertEqual(loaded["total"], len(_MACHINES))


# ---------------------------------------------------------------------------
# Invariants
# ---------------------------------------------------------------------------

class TestInvariants(unittest.TestCase):

    def test_reachable_plus_unreachable_equals_total(self):
        injected_map = {
            "db-layer": _injected(["openclaw-core"]),
            "admin-trading": _injected([], reachable=False),
            "fantome": _injected([]),
        }
        report = run_aggregate(_MACHINES, hostname=_FAKE_HOSTNAME, injected_map=injected_map)
        total = len(report["reachable_machines"]) + len(report["unreachable_machines"])
        self.assertEqual(total, report["total"])

    def test_machines_dict_keys_match_list(self):
        injected_map = {m: _injected([]) for m in _MACHINES}
        report = run_aggregate(_MACHINES, hostname=_FAKE_HOSTNAME, injected_map=injected_map)
        self.assertEqual(sorted(report["machines"].keys()), sorted(_MACHINES))

    def test_empty_sessions_list_type(self):
        result = aggregate_machine(
            "db-layer", _FAKE_HOSTNAME, injected=_injected([])
        )
        self.assertIsInstance(result["tmux_sessions"], list)

    def test_sessions_list_sorted(self):
        unsorted = ["z-session", "a-session", "m-session"]
        result = aggregate_machine(
            "db-layer", _FAKE_HOSTNAME, injected=_injected(unsorted)
        )
        self.assertEqual(result["tmux_sessions"], sorted(unsorted))


if __name__ == "__main__":
    unittest.main(verbosity=2)
