"""
Kill switch + Telegram dry-run validation — Phase 1 readiness gate.

Validates that:
  1. TRADING_KILL_SWITCH blocks all trades regardless of confidence
  2. Kill switch takes precedence over ALLOW, CAUTION, and any operator gate
  3. No Telegram notification is sent when kill switch is active
  4. Telegram dispatcher dry_run=True returns ok without HTTP calls
  5. Dispatcher gracefully handles missing env vars (no crash)

Run: python -m unittest tests.test_kill_switch_telegram_validation -v
"""
from __future__ import annotations
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.proposition_engine.app.schema import Proposition
from modules.validation_gate.app.schema import GateRequest, GateDecision
from modules.validation_gate.app.risk_check import check_risk, KILL_SWITCH_ENV
from modules.validation_gate.app.gate import ValidationGate
from modules.notification_dispatcher.app.dispatcher import NotificationDispatcher
from modules.notification_dispatcher.app.events import PipelineEvent


def _prop(**kw) -> Proposition:
    defaults = dict(
        request_id="ks-val-001",
        signal_id="sig-ks-001",
        action="BUY",
        size_pct=0.5,
        entry=100.0,
        sl=95.0,
        tp=110.0,
        confidence=0.85,
        rationale="kill_switch_test",
        engines_context={},
        duration_ms=0,
        dry_run=False,
        status="ok",
        error=None,
    )
    defaults.update(kw)
    return Proposition(**defaults)


def _mock_dispatcher():
    d = MagicMock()
    d.dispatch.return_value = {"ok": True, "dry_run": True, "event_type": "approval_required"}
    return d


# ── Kill switch — risk_check level ──────────────────────────────────────────

class TestKillSwitchRiskCheck(unittest.TestCase):

    def test_kill_switch_blocks_high_confidence(self):
        os.environ[KILL_SWITCH_ENV] = "1"
        try:
            status, reason = check_risk(_prop(confidence=0.95))
            self.assertEqual(status, "BLOCK")
            self.assertEqual(reason, "kill_switch_active")
        finally:
            del os.environ[KILL_SWITCH_ENV]

    def test_kill_switch_blocks_medium_confidence(self):
        os.environ[KILL_SWITCH_ENV] = "1"
        try:
            status, reason = check_risk(_prop(confidence=0.70))
            self.assertEqual(status, "BLOCK")
            self.assertEqual(reason, "kill_switch_active")
        finally:
            del os.environ[KILL_SWITCH_ENV]

    def test_kill_switch_blocks_minimum_confidence(self):
        os.environ[KILL_SWITCH_ENV] = "1"
        try:
            status, reason = check_risk(_prop(confidence=0.60))
            self.assertEqual(status, "BLOCK")
            self.assertEqual(reason, "kill_switch_active")
        finally:
            del os.environ[KILL_SWITCH_ENV]

    def test_kill_switch_any_truthy_value(self):
        for val in ("1", "true", "yes", "ACTIVE"):
            os.environ[KILL_SWITCH_ENV] = val
            try:
                status, _ = check_risk(_prop(confidence=0.95))
                self.assertEqual(status, "BLOCK", f"Expected BLOCK for KILL_SWITCH={val!r}")
            finally:
                del os.environ[KILL_SWITCH_ENV]

    def test_no_kill_switch_high_confidence_allows(self):
        os.environ.pop(KILL_SWITCH_ENV, None)
        status, _ = check_risk(_prop(confidence=0.95))
        self.assertEqual(status, "ALLOW")

    def test_kill_switch_env_constant_is_trading_kill_switch(self):
        self.assertEqual(KILL_SWITCH_ENV, "TRADING_KILL_SWITCH")


# ── Kill switch — ValidationGate level (full pipeline) ──────────────────────

class TestKillSwitchGate(unittest.TestCase):

    def _gate(self, tmpdir, dispatcher=None):
        return ValidationGate(
            approval_dir=Path(tmpdir),
            dispatcher=dispatcher or _mock_dispatcher(),
        )

    def test_gate_rejected_kill_switch_high_confidence(self):
        os.environ[KILL_SWITCH_ENV] = "1"
        try:
            with tempfile.TemporaryDirectory() as d:
                dec = self._gate(d).gate(GateRequest(proposition=_prop(confidence=0.95), dry_run=True))
            self.assertEqual(dec.verdict, "REJECTED")
            self.assertEqual(dec.risk_status, "BLOCK")
            self.assertEqual(dec.reason, "kill_switch_active")
        finally:
            del os.environ[KILL_SWITCH_ENV]

    def test_gate_rejected_kill_switch_medium_confidence(self):
        os.environ[KILL_SWITCH_ENV] = "1"
        try:
            with tempfile.TemporaryDirectory() as d:
                dec = self._gate(d).gate(GateRequest(proposition=_prop(confidence=0.70), dry_run=True))
            self.assertEqual(dec.verdict, "REJECTED")
            self.assertEqual(dec.reason, "kill_switch_active")
        finally:
            del os.environ[KILL_SWITCH_ENV]

    def test_kill_switch_no_notification_sent(self):
        """Kill switch must not fire Telegram — notification only sent on ALLOW/CAUTION."""
        os.environ[KILL_SWITCH_ENV] = "1"
        mock_d = _mock_dispatcher()
        try:
            with tempfile.TemporaryDirectory() as d:
                self._gate(d, dispatcher=mock_d).gate(
                    GateRequest(proposition=_prop(confidence=0.95), dry_run=True)
                )
            mock_d.dispatch.assert_not_called()
        finally:
            del os.environ[KILL_SWITCH_ENV]

    def test_kill_switch_not_set_notification_is_sent(self):
        """Without kill switch, ALLOW confidence triggers notification."""
        os.environ.pop(KILL_SWITCH_ENV, None)
        mock_d = _mock_dispatcher()
        with tempfile.TemporaryDirectory() as d:
            self._gate(d, dispatcher=mock_d).gate(
                GateRequest(proposition=_prop(confidence=0.85), dry_run=True)
            )
        mock_d.dispatch.assert_called_once()

    def test_kill_switch_gate_decision_is_dry_run_flagged(self):
        os.environ[KILL_SWITCH_ENV] = "1"
        try:
            with tempfile.TemporaryDirectory() as d:
                dec = self._gate(d).gate(GateRequest(proposition=_prop(), dry_run=True))
            self.assertTrue(dec.dry_run)
        finally:
            del os.environ[KILL_SWITCH_ENV]

    def test_kill_switch_unset_after_test(self):
        """Guard: KILL_SWITCH_ENV is not set in the environment after this suite."""
        self.assertNotIn(KILL_SWITCH_ENV, os.environ)


# ── Telegram dispatcher — dry_run mode ──────────────────────────────────────

class TestTelegramDispatcherDryRun(unittest.TestCase):

    def _dispatch(self, event_type: str, payload: dict | None = None) -> dict:
        e = PipelineEvent(event_type=event_type, payload=payload or {})  # type: ignore[arg-type]
        return NotificationDispatcher().dispatch(e, dry_run=True)

    def test_dry_run_returns_ok(self):
        result = self._dispatch("approval_required", {
            "ticker": "BTCUSDT", "action": "BUY",
            "entry": 65000, "sl": 63000, "tp": 68000, "confidence": 0.85,
        })
        self.assertTrue(result["ok"])
        self.assertTrue(result.get("dry_run"))

    def test_dry_run_no_http_call(self):
        with patch("modules.notification_dispatcher.app.dispatcher.requests.post") as mock_post:
            self._dispatch("pipeline_info", {"message": "validation test"})
            mock_post.assert_not_called()

    def test_dry_run_returns_message(self):
        result = self._dispatch("pipeline_info", {"message": "kill switch validation"})
        self.assertIn("message", result)
        self.assertIn("kill switch validation", result["message"])

    def test_dry_run_event_type_echoed(self):
        result = self._dispatch("approval_required", {
            "ticker": "BTCUSDT", "action": "BUY",
            "entry": 1, "sl": 1, "tp": 1, "confidence": 0.9,
        })
        self.assertEqual(result["event_type"], "approval_required")

    def test_live_dispatch_missing_env_vars_returns_error(self):
        """Without env vars, live dispatch returns error dict (no crash)."""
        os.environ.pop("TELEGRAM_BOT_TOKEN", None)
        os.environ.pop("TELEGRAM_TOKEN", None)
        os.environ.pop("TELEGRAM_CHAT_ID", None)
        e = PipelineEvent(event_type="pipeline_info", payload={"message": "test"})  # type: ignore[arg-type]
        result = NotificationDispatcher().dispatch(e, dry_run=False)
        self.assertFalse(result["ok"])
        self.assertIn("error", result)

    def test_dry_run_does_not_require_env_vars(self):
        """dry_run=True must work with no Telegram env vars configured."""
        os.environ.pop("TELEGRAM_BOT_TOKEN", None)
        os.environ.pop("TELEGRAM_TOKEN", None)
        os.environ.pop("TELEGRAM_CHAT_ID", None)
        result = self._dispatch("pipeline_info", {"message": "no-env test"})
        self.assertTrue(result["ok"])
        self.assertTrue(result.get("dry_run"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
