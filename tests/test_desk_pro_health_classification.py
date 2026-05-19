"""Tests for _compute_health classification: infra vs business-level fails.

Classification rule (mirrors deskpro_watchdog.sh logic):
  infra_fail_count = checks where status=fail AND check != webhook_activity
  - infra_fail_count > 0  →  watchdog ALERT (infrastructure issue)
  - only webhook_activity failing  →  watchdog WARN only (business/activity gap)
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.desk_pro.api.routes import _compute_health


def _infra_fail_count(checks: list) -> int:
    """Mirrors the watchdog infra_count logic: fail checks excluding webhook_activity."""
    return sum(1 for c in checks if c["status"] == "fail" and c["check"] != "webhook_activity")


def _make_data(
    webhook=True,
    perf=True,
    last_event_age_sec=100,
    error_count=0,
    sources=None,
) -> dict:
    """Build a minimal _compute_health input."""
    return {
        "webhook": {"ok": True} if webhook else None,
        "perf": {"ok": True} if perf else None,
        "webhook_metrics": {"last_event_age_sec": last_event_age_sec} if last_event_age_sec is not None else None,
        "error_count": error_count,
        "sources": sources or {},
    }


class TestComputeHealthStatus(unittest.TestCase):

    def test_all_pass_is_healthy(self):
        h = _compute_health(_make_data())
        self.assertEqual(h["status"], "healthy")

    def test_webhook_activity_warn_age_none_is_degraded(self):
        data = _make_data(last_event_age_sec=None)
        data["webhook_metrics"] = None
        h = _compute_health(data)
        self.assertEqual(h["status"], "degraded")
        wa = next(c for c in h["checks"] if c["check"] == "webhook_activity")
        self.assertEqual(wa["status"], "warn")

    def test_webhook_activity_warn_stale_is_degraded(self):
        data = _make_data(last_event_age_sec=5000)  # 3600 < 5000 < 7200
        h = _compute_health(data)
        self.assertEqual(h["status"], "degraded")
        wa = next(c for c in h["checks"] if c["check"] == "webhook_activity")
        self.assertEqual(wa["status"], "warn")

    def test_webhook_activity_fail_old_is_down(self):
        data = _make_data(last_event_age_sec=9000)  # > 7200
        h = _compute_health(data)
        self.assertEqual(h["status"], "down")
        wa = next(c for c in h["checks"] if c["check"] == "webhook_activity")
        self.assertEqual(wa["status"], "fail")

    def test_webhook_unreachable_is_down(self):
        data = _make_data(webhook=False)
        h = _compute_health(data)
        self.assertEqual(h["status"], "down")
        wh = next(c for c in h["checks"] if c["check"] == "webhook")
        self.assertEqual(wh["status"], "fail")

    def test_perf_unreachable_is_down(self):
        data = _make_data(perf=False)
        h = _compute_health(data)
        self.assertEqual(h["status"], "down")
        pf = next(c for c in h["checks"] if c["check"] == "perf")
        self.assertEqual(pf["status"], "fail")

    def test_probe_errors_warn_threshold(self):
        data = _make_data(error_count=10)  # 5 < 10 <= 20
        h = _compute_health(data)
        self.assertEqual(h["status"], "degraded")
        pe = next(c for c in h["checks"] if c["check"] == "probe_errors")
        self.assertEqual(pe["status"], "warn")

    def test_probe_errors_fail_threshold(self):
        data = _make_data(error_count=25)  # > 20
        h = _compute_health(data)
        self.assertEqual(h["status"], "down")
        pe = next(c for c in h["checks"] if c["check"] == "probe_errors")
        self.assertEqual(pe["status"], "fail")

    def test_webhook_activity_pass_within_threshold(self):
        data = _make_data(last_event_age_sec=60)
        h = _compute_health(data)
        wa = next(c for c in h["checks"] if c["check"] == "webhook_activity")
        self.assertEqual(wa["status"], "pass")


class TestInfraFailClassification(unittest.TestCase):
    """Validate the watchdog's infra_count classification logic."""

    def test_all_pass_infra_count_zero(self):
        h = _compute_health(_make_data())
        self.assertEqual(_infra_fail_count(h["checks"]), 0)

    def test_webhook_activity_fail_alone_infra_count_zero(self):
        """webhook_activity:fail must NOT trigger watchdog ALERT — business level only."""
        data = _make_data(last_event_age_sec=9000)
        h = _compute_health(data)
        self.assertEqual(h["status"], "down")
        self.assertEqual(_infra_fail_count(h["checks"]), 0)

    def test_webhook_activity_warn_infra_count_zero(self):
        data = _make_data(last_event_age_sec=None)
        data["webhook_metrics"] = None
        h = _compute_health(data)
        self.assertEqual(h["status"], "degraded")
        self.assertEqual(_infra_fail_count(h["checks"]), 0)

    def test_webhook_fail_infra_count_nonzero(self):
        """webhook:fail (port unreachable) must trigger watchdog ALERT."""
        data = _make_data(webhook=False)
        h = _compute_health(data)
        self.assertGreaterEqual(_infra_fail_count(h["checks"]), 1)

    def test_perf_fail_infra_count_nonzero(self):
        """perf:fail must trigger watchdog ALERT."""
        data = _make_data(perf=False)
        h = _compute_health(data)
        self.assertGreaterEqual(_infra_fail_count(h["checks"]), 1)

    def test_probe_errors_fail_infra_count_nonzero(self):
        """probe_errors:fail must trigger watchdog ALERT."""
        data = _make_data(error_count=25)
        h = _compute_health(data)
        self.assertGreaterEqual(_infra_fail_count(h["checks"]), 1)

    def test_mixed_webhook_fail_and_activity_fail_infra_count_nonzero(self):
        """Both infra and business failing — infra_count still ≥ 1."""
        data = _make_data(webhook=False, last_event_age_sec=9000)
        h = _compute_health(data)
        self.assertEqual(h["status"], "down")
        self.assertGreaterEqual(_infra_fail_count(h["checks"]), 1)

    def test_webhook_activity_fail_with_all_infra_pass_infra_count_zero(self):
        """Real scenario: ports UP, app healthy, only webhook_activity:fail → no ALERT."""
        data = _make_data(webhook=True, perf=True, last_event_age_sec=9000, error_count=0)
        h = _compute_health(data)
        self.assertEqual(h["status"], "down")
        self.assertEqual(_infra_fail_count(h["checks"]), 0,
                         "webhook_activity:fail alone must not produce infra_count > 0")
