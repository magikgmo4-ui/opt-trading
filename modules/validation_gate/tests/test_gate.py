"""Validation gate tests — python3 -m unittest"""
from __future__ import annotations
import os
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.proposition_engine.app.schema import Proposition
from modules.validation_gate.app.schema import GateRequest, GateDecision
from modules.validation_gate.app.risk_check import check_risk
from modules.validation_gate.app.operator_gate import OperatorGate
from modules.validation_gate.app.gate import ValidationGate


def _prop(**kw) -> Proposition:
    defaults = dict(
        request_id="req-001",
        signal_id="sig-001",
        action="BUY",
        size_pct=0.5,
        entry=100.0,
        sl=95.0,
        tp=110.0,
        confidence=0.85,
        rationale="test",
        engines_context={},
        duration_ms=0,
        dry_run=False,
        status="ok",
        error=None,
    )
    defaults.update(kw)
    return Proposition(**defaults)


def _mock_dispatcher(dry_run_ok: bool = True):
    d = MagicMock()
    d.dispatch.return_value = {"ok": True, "dry_run": dry_run_ok, "event_type": "approval_required"}
    return d


# ---------------------------------------------------------------------------
# risk_check unit tests
# ---------------------------------------------------------------------------

class TestRiskCheck(unittest.TestCase):

    def test_risk_check_kill_switch(self):
        os.environ["TRADING_KILL_SWITCH"] = "1"
        try:
            status, reason = check_risk(_prop())
            self.assertEqual(status, "BLOCK")
            self.assertEqual(reason, "kill_switch_active")
        finally:
            del os.environ["TRADING_KILL_SWITCH"]

    def test_risk_check_action_hold(self):
        status, reason = check_risk(_prop(action="HOLD"))
        self.assertEqual(status, "BLOCK")
        self.assertIn("HOLD", reason)

    def test_risk_check_action_skip(self):
        status, reason = check_risk(_prop(action="SKIP"))
        self.assertEqual(status, "BLOCK")
        self.assertIn("SKIP", reason)

    def test_risk_check_proposition_error(self):
        status, reason = check_risk(_prop(status="error", error="bridge_timeout"))
        self.assertEqual(status, "BLOCK")
        self.assertIn("proposition_error", reason)

    def test_risk_check_low_confidence(self):
        status, reason = check_risk(_prop(confidence=0.3))
        self.assertEqual(status, "BLOCK")
        self.assertIn("confidence", reason)

    def test_risk_check_boundary_low(self):
        # Exactly at threshold — BLOCK (< not <=)
        status, reason = check_risk(_prop(confidence=0.599))
        self.assertEqual(status, "BLOCK")

    def test_risk_check_medium_confidence(self):
        status, reason = check_risk(_prop(confidence=0.7))
        self.assertEqual(status, "CAUTION")
        self.assertIn("confidence", reason)

    def test_risk_check_high_confidence(self):
        status, reason = check_risk(_prop(confidence=0.85))
        self.assertEqual(status, "ALLOW")
        self.assertIn("confidence", reason)

    def test_risk_check_boundary_high(self):
        # Exactly at HIGH_CONFIDENCE threshold — ALLOW
        status, _ = check_risk(_prop(confidence=0.8))
        self.assertEqual(status, "ALLOW")


# ---------------------------------------------------------------------------
# GateDecision / GateRequest schema tests
# ---------------------------------------------------------------------------

class TestSchema(unittest.TestCase):

    def test_schema_gate_decision_defaults(self):
        d = GateDecision(
            request_id="r", signal_id="s",
            verdict="APPROVED", reason="ok",
            risk_status="ALLOW", risk_reason="high_confidence",
        )
        self.assertIsNone(d.operator_approved)
        self.assertEqual(d.duration_ms, 0)
        self.assertFalse(d.dry_run)
        self.assertEqual(d.meta, {})

    def test_schema_gate_request_defaults(self):
        req = GateRequest(proposition=_prop())
        self.assertEqual(req.request_id, "")
        self.assertTrue(req.require_operator)
        self.assertEqual(req.timeout_s, 60)
        self.assertEqual(req.poll_interval_s, 2.0)
        self.assertFalse(req.dry_run)


# ---------------------------------------------------------------------------
# OperatorGate unit tests
# ---------------------------------------------------------------------------

class TestOperatorGate(unittest.TestCase):

    def test_operator_gate_approve(self):
        with tempfile.TemporaryDirectory() as d:
            og = OperatorGate(Path(d))
            og.write_approval("req-test", "APPROVE")
            result = og.poll("req-test", timeout_s=2, poll_interval_s=0.01)
            self.assertTrue(result)

    def test_operator_gate_reject(self):
        with tempfile.TemporaryDirectory() as d:
            og = OperatorGate(Path(d))
            og.write_approval("req-test", "REJECT")
            result = og.poll("req-test", timeout_s=2, poll_interval_s=0.01)
            self.assertFalse(result)

    def test_operator_gate_timeout(self):
        with tempfile.TemporaryDirectory() as d:
            og = OperatorGate(Path(d))
            result = og.poll("req-missing", timeout_s=0.05, poll_interval_s=0.01)
            self.assertIsNone(result)

    def test_operator_gate_file_deleted_after_read(self):
        with tempfile.TemporaryDirectory() as d:
            og = OperatorGate(Path(d))
            og.write_approval("req-del", "APPROVE")
            og.poll("req-del", timeout_s=2, poll_interval_s=0.01)
            self.assertFalse((Path(d) / "req-del.json").exists())


# ---------------------------------------------------------------------------
# ValidationGate gate() tests
# ---------------------------------------------------------------------------

class TestValidationGate(unittest.TestCase):

    def _gate(self, tmpdir, dispatcher=None):
        return ValidationGate(
            approval_dir=Path(tmpdir),
            dispatcher=dispatcher or _mock_dispatcher(),
        )

    # --- BLOCK paths ---

    def test_gate_rejected_kill_switch(self):
        os.environ["TRADING_KILL_SWITCH"] = "1"
        try:
            with tempfile.TemporaryDirectory() as d:
                g = self._gate(d)
                req = GateRequest(proposition=_prop(), dry_run=True)
                dec = g.gate(req)
            self.assertEqual(dec.verdict, "REJECTED")
            self.assertEqual(dec.risk_status, "BLOCK")
            self.assertEqual(dec.reason, "kill_switch_active")
        finally:
            del os.environ["TRADING_KILL_SWITCH"]

    def test_gate_rejected_hold_action(self):
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(proposition=_prop(action="HOLD"), dry_run=True)
            dec = g.gate(req)
        self.assertEqual(dec.verdict, "REJECTED")
        self.assertIn("HOLD", dec.reason)

    def test_gate_rejected_low_confidence(self):
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(proposition=_prop(confidence=0.2), dry_run=True)
            dec = g.gate(req)
        self.assertEqual(dec.verdict, "REJECTED")
        self.assertIn("confidence", dec.reason)

    # --- dry_run operator gate ---

    def test_gate_approved_dry_run_high_confidence(self):
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(proposition=_prop(confidence=0.85), dry_run=True)
            dec = g.gate(req)
        self.assertEqual(dec.verdict, "APPROVED")
        self.assertTrue(dec.dry_run)
        self.assertTrue(dec.operator_approved)

    def test_gate_hold_dry_run_medium_confidence_below_threshold(self):
        # confidence=0.65 passes risk (CAUTION) but < dry_run 0.7 threshold → HOLD
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(proposition=_prop(confidence=0.65), dry_run=True)
            dec = g.gate(req)
        self.assertEqual(dec.verdict, "HOLD")
        self.assertFalse(dec.operator_approved)

    def test_gate_approved_dry_run_at_threshold(self):
        # confidence=0.70 exactly at threshold → APPROVED
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(proposition=_prop(confidence=0.70), dry_run=True)
            dec = g.gate(req)
        self.assertEqual(dec.verdict, "APPROVED")

    # --- require_operator=False ---

    def test_gate_no_operator_allow(self):
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(proposition=_prop(confidence=0.85), require_operator=False)
            dec = g.gate(req)
        self.assertEqual(dec.verdict, "APPROVED")
        self.assertIsNone(dec.operator_approved)

    def test_gate_no_operator_caution_needs_review(self):
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(proposition=_prop(confidence=0.7), require_operator=False)
            dec = g.gate(req)
        self.assertEqual(dec.verdict, "NEEDS_REVIEW")
        self.assertIsNone(dec.operator_approved)

    # --- live operator approval via file ---

    def test_gate_operator_approved_via_file(self):
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(
                proposition=_prop(confidence=0.85),
                dry_run=False,
                require_operator=True,
                timeout_s=2,
                poll_interval_s=0.01,
            )
            req.request_id = "live-approve-test"
            g.operator_gate.write_approval("live-approve-test", "APPROVE")
            dec = g.gate(req)
        self.assertEqual(dec.verdict, "APPROVED")
        self.assertTrue(dec.operator_approved)

    def test_gate_operator_rejected_via_file(self):
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(
                proposition=_prop(confidence=0.85),
                dry_run=False,
                require_operator=True,
                timeout_s=2,
                poll_interval_s=0.01,
            )
            req.request_id = "live-reject-test"
            g.operator_gate.write_approval("live-reject-test", "REJECT")
            dec = g.gate(req)
        self.assertEqual(dec.verdict, "REJECTED")
        self.assertFalse(dec.operator_approved)
        self.assertEqual(dec.reason, "operator_rejected")

    def test_gate_operator_timeout_returns_hold(self):
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(
                proposition=_prop(confidence=0.85),
                dry_run=False,
                require_operator=True,
                timeout_s=0.05,
                poll_interval_s=0.01,
            )
            req.request_id = "live-timeout-test"
            dec = g.gate(req)
        self.assertEqual(dec.verdict, "HOLD")
        self.assertIsNone(dec.operator_approved)
        self.assertEqual(dec.reason, "operator_timeout")

    # --- notification dispatch ---

    def test_gate_notification_sent_on_approval_required(self):
        with tempfile.TemporaryDirectory() as d:
            mock_d = _mock_dispatcher()
            g = self._gate(d, dispatcher=mock_d)
            req = GateRequest(
                proposition=_prop(confidence=0.85),
                ticker="BTCUSDT",
                dry_run=True,
            )
            g.gate(req)
        mock_d.dispatch.assert_called_once()
        call_event = mock_d.dispatch.call_args[0][0]
        self.assertEqual(call_event.event_type, "approval_required")
        self.assertEqual(call_event.payload["ticker"], "BTCUSDT")

    def test_gate_notification_not_sent_when_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            mock_d = _mock_dispatcher()
            g = self._gate(d, dispatcher=mock_d)
            req = GateRequest(proposition=_prop(action="HOLD"), dry_run=True)
            g.gate(req)
        mock_d.dispatch.assert_not_called()

    # --- request_id auto-generated ---

    def test_gate_auto_generates_request_id(self):
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(proposition=_prop(confidence=0.85), dry_run=True)
            self.assertEqual(req.request_id, "")
            dec = g.gate(req)
        self.assertNotEqual(dec.request_id, "")

    # --- meta field ---

    def test_gate_meta_contains_notif_result(self):
        with tempfile.TemporaryDirectory() as d:
            g = self._gate(d)
            req = GateRequest(proposition=_prop(confidence=0.85), dry_run=True)
            dec = g.gate(req)
        self.assertIn("notif", dec.meta)
        self.assertTrue(dec.meta["notif"]["ok"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
