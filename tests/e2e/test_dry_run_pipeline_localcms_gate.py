"""
Tests unitaires pour la gate LocalCMS du E2E dry-run pipeline.

Tous les tests mockent urllib.request.urlopen — aucun appel réseau réel.
Tests subprocess vérifient le comportement de fin via rc et rapport JSON.
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = PROJECT_ROOT / "scripts" / "e2e" / "dry_run_pipeline.py"

# ── Import gate functions from the script ──────────────────────────────────────
import importlib.util as _ilu

_spec = _ilu.spec_from_file_location("_drp", _SCRIPT)
_drp = _ilu.module_from_spec(_spec)
sys.modules["_drp"] = _drp  # required so @dataclass resolves __module__ correctly
_spec.loader.exec_module(_drp)

E2ELocalCMSGateResult = _drp.E2ELocalCMSGateResult
check_localcms_available = _drp.check_localcms_available
classify_localcms_gate = _drp.classify_localcms_gate


def _mock_urlopen_ok(url, timeout=2):
    resp = MagicMock()
    resp.status = 200
    resp.__enter__ = lambda s: s
    resp.__exit__ = MagicMock(return_value=False)
    return resp


def _mock_urlopen_fail(url, timeout=2):
    raise OSError("Connection refused")


# ── Unit tests: check_localcms_available ──────────────────────────────────────

class TestCheckLocalcmsAvailable(unittest.TestCase):

    def test_reachable_returns_true(self):
        with patch("urllib.request.urlopen", _mock_urlopen_ok):
            ok, err = check_localcms_available("http://localhost:8700")
        self.assertTrue(ok)
        self.assertEqual(err, "")

    def test_unreachable_returns_false(self):
        with patch("urllib.request.urlopen", _mock_urlopen_fail):
            ok, err = check_localcms_available("http://localhost:8700")
        self.assertFalse(ok)
        self.assertIn("Connection refused", err)

    def test_never_raises(self):
        with patch("urllib.request.urlopen", _mock_urlopen_fail):
            result = check_localcms_available("http://invalid:9999")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)


# ── Unit tests: classify_localcms_gate ───────────────────────────────────────

class TestClassifyLocalcmsGate(unittest.TestCase):

    def test_default_mode_present_is_pass(self):
        with patch.object(_drp, "check_localcms_available", return_value=(True, "")):
            result = classify_localcms_gate(require=False, skip=False, url="http://x:8700")
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.mode, "default")

    def test_default_mode_absent_is_warn_skipped(self):
        with patch.object(_drp, "check_localcms_available", return_value=(False, "refused")):
            result = classify_localcms_gate(require=False, skip=False, url="http://x:8700")
        self.assertEqual(result.status, "WARN_SKIPPED")
        self.assertEqual(result.mode, "default")

    def test_require_mode_absent_is_blocked(self):
        with patch.object(_drp, "check_localcms_available", return_value=(False, "refused")):
            result = classify_localcms_gate(require=True, skip=False, url="http://x:8700")
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.mode, "require")

    def test_require_mode_present_is_pass(self):
        with patch.object(_drp, "check_localcms_available", return_value=(True, "")):
            result = classify_localcms_gate(require=True, skip=False, url="http://x:8700")
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.mode, "require")

    def test_skip_mode_always_warn_skipped(self):
        # Even if LocalCMS would be reachable, skip wins
        with patch.object(_drp, "check_localcms_available", return_value=(True, "")):
            result = classify_localcms_gate(require=False, skip=True, url="http://x:8700")
        self.assertEqual(result.status, "WARN_SKIPPED")
        self.assertEqual(result.mode, "skip")

    def test_skip_mode_no_network_call(self):
        called = []
        def _track(*a, **kw):
            called.append(True)
            return True, ""
        with patch.object(_drp, "check_localcms_available", side_effect=_track):
            classify_localcms_gate(require=False, skip=True, url="http://x:8700")
        self.assertEqual(called, [], "check_localcms_available should not be called in skip mode")

    def test_gate_result_has_required_fields(self):
        with patch.object(_drp, "check_localcms_available", return_value=(False, "err")):
            result = classify_localcms_gate(require=False, skip=False, url="http://test:8700")
        self.assertIsInstance(result, E2ELocalCMSGateResult)
        self.assertIn(result.status, ("PASS", "WARN_SKIPPED", "BLOCKED"))
        self.assertIsInstance(result.reason, str)
        self.assertIsInstance(result.url, str)
        self.assertIsInstance(result.mode, str)

    def test_blocked_reason_contains_url(self):
        with patch.object(_drp, "check_localcms_available", return_value=(False, "conn err")):
            result = classify_localcms_gate(require=True, skip=False, url="http://my-host:8700")
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("http://my-host:8700", result.reason)

    def test_warn_skipped_does_not_contain_blocked(self):
        with patch.object(_drp, "check_localcms_available", return_value=(False, "err")):
            result = classify_localcms_gate(require=False, skip=False, url="http://x:8700")
        self.assertNotEqual(result.status, "BLOCKED")

    def test_invalid_url_default_is_warn_skipped(self):
        with patch("urllib.request.urlopen", _mock_urlopen_fail):
            result = classify_localcms_gate(require=False, skip=False, url="http://bad-host:9999")
        self.assertEqual(result.status, "WARN_SKIPPED")

    def test_invalid_url_require_is_blocked(self):
        with patch("urllib.request.urlopen", _mock_urlopen_fail):
            result = classify_localcms_gate(require=True, skip=False, url="http://bad-host:9999")
        self.assertEqual(result.status, "BLOCKED")


# ── Subprocess integration tests ───────────────────────────────────────────────

class TestScriptLocalcmsGate(unittest.TestCase):
    """Tests via subprocess — vérifier rc et structure du rapport JSON."""

    def _run(self, extra_env: dict | None = None, timeout: int = 30) -> tuple[int, dict]:
        env = {**os.environ, "DRY_RUN": "1", "PAPER_MODE": "1", "ALLOW_E2E_LIVE_DRY_RUN": "1"}
        env.pop("REQUIRE_LOCALCMS_E2E", None)
        env.pop("SKIP_LOCALCMS_E2E", None)
        env.pop("LOCALCMS_URL", None)
        env.pop("ALLOW_LIVE_TRADE", None)
        if extra_env:
            env.update(extra_env)
        r = subprocess.run(
            [sys.executable, str(_SCRIPT)],
            capture_output=True, text=True, timeout=timeout, env=env,
        )
        try:
            report = json.loads(r.stdout)
        except json.JSONDecodeError:
            report = {}
        return r.returncode, report

    def test_default_mode_absent_localcms_exits_0(self):
        rc, _ = self._run()
        self.assertEqual(rc, 0, "Default mode should exit 0 even if LocalCMS absent")

    def test_default_mode_gate_status_warn_skipped(self):
        _, report = self._run()
        gate = report.get("localcms_gate", {})
        self.assertEqual(gate.get("status"), "WARN_SKIPPED")

    def test_default_mode_e2e_status_pass(self):
        _, report = self._run()
        self.assertEqual(report.get("e2e_status"), "PASS")

    def test_require_mode_absent_localcms_exits_1(self):
        rc, _ = self._run({"REQUIRE_LOCALCMS_E2E": "1"})
        self.assertEqual(rc, 1, "REQUIRE_LOCALCMS_E2E=1 should exit 1 when LocalCMS absent")

    def test_require_mode_gate_status_blocked(self):
        _, report = self._run({"REQUIRE_LOCALCMS_E2E": "1"})
        gate = report.get("localcms_gate", {})
        self.assertEqual(gate.get("status"), "BLOCKED")

    def test_require_mode_e2e_status_fail(self):
        _, report = self._run({"REQUIRE_LOCALCMS_E2E": "1"})
        self.assertEqual(report.get("e2e_status"), "FAIL")

    def test_skip_mode_exits_0(self):
        rc, _ = self._run({"SKIP_LOCALCMS_E2E": "1"})
        self.assertEqual(rc, 0)

    def test_skip_mode_gate_status_warn_skipped(self):
        _, report = self._run({"SKIP_LOCALCMS_E2E": "1"})
        gate = report.get("localcms_gate", {})
        self.assertEqual(gate.get("status"), "WARN_SKIPPED")

    def test_report_has_localcms_gate_key(self):
        _, report = self._run()
        self.assertIn("localcms_gate", report)

    def test_report_backward_compat_localcms_key(self):
        _, report = self._run()
        self.assertIn("localcms", report)
        self.assertIn("localcms_ok", report)

    def test_localcms_gate_has_status_reason_url_mode(self):
        _, report = self._run()
        gate = report.get("localcms_gate", {})
        for field in ("status", "reason", "url", "mode"):
            self.assertIn(field, gate, f"Missing gate field: {field}")

    def test_7_steps_still_present(self):
        _, report = self._run()
        step_names = [s["step"] for s in report.get("steps", [])]
        for name in ("1_signal_router", "2_proposition_engine", "3_validation_gate",
                     "4_trade_executor", "5_result_tracker", "6_datasheet_writer",
                     "7_learning_feeder"):
            self.assertIn(name, step_names, f"Missing step: {name}")

    def test_all_ok_true_in_default_mode(self):
        _, report = self._run()
        self.assertTrue(report.get("all_ok"), "all_ok should be True when product chain succeeds")

    def test_mode_in_gate_report(self):
        _, report = self._run()
        gate = report.get("localcms_gate", {})
        self.assertEqual(gate.get("mode"), "default")


if __name__ == "__main__":
    unittest.main(verbosity=2)
