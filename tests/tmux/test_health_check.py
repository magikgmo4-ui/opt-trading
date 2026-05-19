"""TMUX health check tests — python3 -m unittest"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.tmux.health_check import (
    check_sessions,
    _format_summary,
    CRITICAL_SESSIONS,
    ALL_SESSIONS,
)

_ALL = sorted(ALL_SESSIONS)
_CRITICAL = sorted(CRITICAL_SESSIONS)


# ---------------------------------------------------------------------------
# Constants tests
# ---------------------------------------------------------------------------

class TestConstants(unittest.TestCase):

    def test_critical_sessions_defined(self):
        self.assertIn("openclaw-core", CRITICAL_SESSIONS)
        self.assertIn("screeners", CRITICAL_SESSIONS)
        self.assertIn("strict-workers", CRITICAL_SESSIONS)

    def test_all_sessions_superset_of_critical(self):
        self.assertTrue(CRITICAL_SESSIONS.issubset(ALL_SESSIONS))

    def test_all_sessions_count(self):
        self.assertEqual(len(ALL_SESSIONS), 10)

    def test_critical_sessions_count(self):
        self.assertEqual(len(CRITICAL_SESSIONS), 3)


# ---------------------------------------------------------------------------
# check_sessions — all up
# ---------------------------------------------------------------------------

class TestCheckAllUp(unittest.TestCase):

    def setUp(self):
        self.report = check_sessions(active=list(ALL_SESSIONS))

    def test_all_ok_true(self):
        self.assertTrue(self.report["all_ok"])

    def test_no_missing(self):
        self.assertEqual(self.report["missing"], [])

    def test_no_critical_down(self):
        self.assertEqual(self.report["critical_down"], [])

    def test_needs_alert_false(self):
        self.assertFalse(self.report["needs_alert"])

    def test_up_contains_all_sessions(self):
        self.assertEqual(sorted(self.report["up"]), _ALL)

    def test_timestamp_present(self):
        self.assertIn("T", self.report["timestamp"])


# ---------------------------------------------------------------------------
# check_sessions — no active sessions
# ---------------------------------------------------------------------------

class TestCheckNoneUp(unittest.TestCase):

    def setUp(self):
        self.report = check_sessions(active=[])

    def test_all_ok_false(self):
        self.assertFalse(self.report["all_ok"])

    def test_all_missing(self):
        self.assertEqual(sorted(self.report["missing"]), _ALL)

    def test_up_empty(self):
        self.assertEqual(self.report["up"], [])

    def test_needs_alert_true(self):
        self.assertTrue(self.report["needs_alert"])

    def test_critical_down_all_critical(self):
        self.assertEqual(sorted(self.report["critical_down"]), _CRITICAL)


# ---------------------------------------------------------------------------
# check_sessions — critical session down
# ---------------------------------------------------------------------------

class TestCheckCriticalDown(unittest.TestCase):

    def setUp(self):
        active = [s for s in ALL_SESSIONS if s != "openclaw-core"]
        self.report = check_sessions(active=active)

    def test_all_ok_false(self):
        self.assertFalse(self.report["all_ok"])

    def test_needs_alert_true(self):
        self.assertTrue(self.report["needs_alert"])

    def test_critical_down_identified(self):
        self.assertIn("openclaw-core", self.report["critical_down"])

    def test_non_critical_down_empty(self):
        self.assertEqual(self.report["non_critical_down"], [])


# ---------------------------------------------------------------------------
# check_sessions — non-critical session down
# ---------------------------------------------------------------------------

class TestCheckNonCriticalDown(unittest.TestCase):

    def setUp(self):
        active = [s for s in ALL_SESSIONS if s != "localcms-ui"]
        self.report = check_sessions(active=active)

    def test_all_ok_false(self):
        self.assertFalse(self.report["all_ok"])

    def test_needs_alert_false(self):
        self.assertFalse(self.report["needs_alert"])

    def test_critical_down_empty(self):
        self.assertEqual(self.report["critical_down"], [])

    def test_non_critical_down_identified(self):
        self.assertIn("localcms-ui", self.report["non_critical_down"])


# ---------------------------------------------------------------------------
# check_sessions — invariants
# ---------------------------------------------------------------------------

class TestCheckInvariants(unittest.TestCase):

    def test_critical_down_subset_of_missing(self):
        active = [s for s in ALL_SESSIONS if s not in ("openclaw-core", "kg-repo")]
        r = check_sessions(active=active)
        self.assertTrue(set(r["critical_down"]).issubset(set(r["missing"])))

    def test_up_subset_of_expected(self):
        active = list(ALL_SESSIONS)[:4]
        r = check_sessions(active=active)
        self.assertTrue(set(r["up"]).issubset(ALL_SESSIONS))

    def test_ignores_extra_unexpected_sessions(self):
        active = list(ALL_SESSIONS) + ["unknown-session", "some-other"]
        r = check_sessions(active=active)
        self.assertTrue(r["all_ok"])
        self.assertNotIn("unknown-session", r["up"])

    def test_up_plus_missing_equals_expected(self):
        active = list(ALL_SESSIONS)[:5]
        r = check_sessions(active=active)
        self.assertEqual(
            sorted(r["up"] + r["missing"]),
            _ALL,
        )

    def test_lists_are_sorted(self):
        active = list(ALL_SESSIONS)[:3]
        r = check_sessions(active=active)
        self.assertEqual(r["up"], sorted(r["up"]))
        self.assertEqual(r["missing"], sorted(r["missing"]))

    def test_all_required_keys_present(self):
        r = check_sessions(active=list(ALL_SESSIONS))
        for key in ("timestamp", "all_ok", "needs_alert", "up", "missing",
                    "critical_down", "non_critical_down", "summary"):
            self.assertIn(key, r)


# ---------------------------------------------------------------------------
# _format_summary
# ---------------------------------------------------------------------------

class TestFormatSummary(unittest.TestCase):

    def test_ok_tag_for_up_session(self):
        summary = _format_summary(
            frozenset({"openclaw-core"}), frozenset(), frozenset()
        )
        self.assertIn("SESSION_OK", summary)
        self.assertIn("openclaw-core", summary)

    def test_critical_down_tag(self):
        summary = _format_summary(
            frozenset(), frozenset({"screeners"}), frozenset({"screeners"})
        )
        self.assertIn("CRITICAL_DOWN", summary)
        self.assertIn("screeners", summary)

    def test_session_missing_tag_for_non_critical(self):
        summary = _format_summary(
            frozenset(), frozenset({"kg-repo"}), frozenset()
        )
        self.assertIn("SESSION_MISSING", summary)
        self.assertIn("kg-repo", summary)


if __name__ == "__main__":
    unittest.main(verbosity=2)
