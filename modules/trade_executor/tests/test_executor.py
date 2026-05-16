"""Trade executor tests — python3 -m unittest"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.proposition_engine.app.schema import Proposition
from modules.validation_gate.app.schema import GateDecision
from modules.trade_executor.app.schema import TradeRequest, TradeResult
from modules.trade_executor.app.executor import TradeExecutor


def _prop(**kw) -> Proposition:
    defaults = dict(
        request_id="req-001", signal_id="sig-001",
        action="BUY", size_pct=0.5,
        entry=65000.0, sl=63000.0, tp=70000.0,
        confidence=0.85, rationale="test",
        engines_context={}, duration_ms=0,
        dry_run=False, status="ok", error=None,
    )
    defaults.update(kw)
    return Proposition(**defaults)


def _approved_gate(**kw) -> GateDecision:
    defaults = dict(
        request_id="gate-001", signal_id="sig-001",
        verdict="APPROVED", reason="dry_run_simulated_operator",
        risk_status="ALLOW", risk_reason="confidence=0.850 >= 0.8",
        operator_approved=True, dry_run=True,
    )
    defaults.update(kw)
    return GateDecision(**defaults)


def _gate(verdict: str) -> GateDecision:
    return _approved_gate(verdict=verdict, operator_approved=(verdict == "APPROVED"))


def _mock_dispatcher():
    d = MagicMock()
    d.dispatch.return_value = {"ok": True, "event_type": "trade_executed"}
    return d


def _executor(dispatcher=None) -> TradeExecutor:
    return TradeExecutor(dispatcher=dispatcher or _mock_dispatcher())


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------

class TestSchema(unittest.TestCase):

    def test_trade_request_defaults(self):
        req = TradeRequest(gate_decision=_approved_gate(), proposition=_prop())
        self.assertEqual(req.request_id, "")
        self.assertEqual(req.ticker, "")
        self.assertTrue(req.dry_run)

    def test_trade_result_defaults(self):
        r = TradeResult(
            request_id="r", signal_id="s", trade_id="t",
            action="BUY", ticker="BTCUSDT",
            fill_price=65000.0, fill_qty=0.5, size_pct=0.5,
            sl=63000.0, tp=70000.0,
            status="dry_run", reason="paper_filled",
        )
        self.assertEqual(r.duration_ms, 0)
        self.assertTrue(r.dry_run)
        self.assertEqual(r.meta, {})


# ---------------------------------------------------------------------------
# Gate enforcement tests
# ---------------------------------------------------------------------------

class TestGateEnforcement(unittest.TestCase):

    def test_rejects_gate_hold(self):
        req = TradeRequest(gate_decision=_gate("HOLD"), proposition=_prop(), dry_run=True)
        result = _executor().execute(req)
        self.assertEqual(result.status, "rejected")
        self.assertIn("HOLD", result.reason)

    def test_rejects_gate_rejected(self):
        req = TradeRequest(gate_decision=_gate("REJECTED"), proposition=_prop(), dry_run=True)
        result = _executor().execute(req)
        self.assertEqual(result.status, "rejected")
        self.assertIn("REJECTED", result.reason)

    def test_rejects_gate_needs_review(self):
        req = TradeRequest(gate_decision=_gate("NEEDS_REVIEW"), proposition=_prop(), dry_run=True)
        result = _executor().execute(req)
        self.assertEqual(result.status, "rejected")

    def test_rejected_no_notification_sent(self):
        mock_d = _mock_dispatcher()
        req = TradeRequest(gate_decision=_gate("HOLD"), proposition=_prop(), dry_run=True)
        _executor(mock_d).execute(req)
        mock_d.dispatch.assert_not_called()

    def test_rejected_fill_price_zero(self):
        req = TradeRequest(gate_decision=_gate("REJECTED"), proposition=_prop(), dry_run=True)
        result = _executor().execute(req)
        self.assertEqual(result.fill_price, 0.0)
        self.assertEqual(result.fill_qty, 0.0)
        self.assertEqual(result.trade_id, "")


# ---------------------------------------------------------------------------
# Dry-run execution tests
# ---------------------------------------------------------------------------

class TestDryRunExecution(unittest.TestCase):

    def _run(self, **kw):
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(**kw),
            ticker="BTCUSDT",
            dry_run=True,
        )
        return _executor().execute(req)

    def test_dry_run_status(self):
        result = self._run()
        self.assertEqual(result.status, "dry_run")

    def test_dry_run_fill_price_matches_entry(self):
        result = self._run(entry=65000.0)
        self.assertEqual(result.fill_price, 65000.0)

    def test_dry_run_fill_qty_matches_size_pct(self):
        result = self._run(size_pct=0.5)
        self.assertEqual(result.fill_qty, 0.5)

    def test_dry_run_trade_id_generated(self):
        result = self._run()
        self.assertTrue(result.trade_id.startswith("paper_"))
        self.assertNotEqual(result.trade_id, "")

    def test_dry_run_buy_action(self):
        result = self._run(action="BUY")
        self.assertEqual(result.action, "BUY")

    def test_dry_run_sell_action(self):
        result = self._run(action="SELL")
        self.assertEqual(result.action, "SELL")

    def test_dry_run_sl_tp_preserved(self):
        result = self._run(sl=63000.0, tp=70000.0)
        self.assertEqual(result.sl, 63000.0)
        self.assertEqual(result.tp, 70000.0)

    def test_dry_run_duration_ms_set(self):
        result = self._run()
        self.assertGreaterEqual(result.duration_ms, 0)

    def test_dry_run_meta_has_adapter(self):
        result = self._run()
        self.assertIn("adapter", result.meta)
        self.assertTrue(result.meta["adapter"]["ok"])

    def test_dry_run_is_flagged(self):
        result = self._run()
        self.assertTrue(result.dry_run)


# ---------------------------------------------------------------------------
# Live (paper) execution — still paper adapter, no Bitget
# ---------------------------------------------------------------------------

class TestLivePaperExecution(unittest.TestCase):

    def test_live_paper_status_filled(self):
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(),
            ticker="ETHUSDT",
            dry_run=False,
        )
        result = _executor().execute(req)
        self.assertEqual(result.status, "filled")

    def test_live_paper_not_flagged_dry_run(self):
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(),
            ticker="ETHUSDT",
            dry_run=False,
        )
        result = _executor().execute(req)
        self.assertFalse(result.dry_run)


# ---------------------------------------------------------------------------
# Notification tests
# ---------------------------------------------------------------------------

class TestNotification(unittest.TestCase):

    def test_notification_sent_on_fill(self):
        mock_d = _mock_dispatcher()
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(),
            ticker="BTCUSDT",
            dry_run=True,
        )
        TradeExecutor(dispatcher=mock_d).execute(req)
        mock_d.dispatch.assert_called_once()

    def test_notification_event_type_trade_executed(self):
        mock_d = _mock_dispatcher()
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(),
            ticker="BTCUSDT",
            dry_run=True,
        )
        TradeExecutor(dispatcher=mock_d).execute(req)
        call_event = mock_d.dispatch.call_args[0][0]
        self.assertEqual(call_event.event_type, "trade_executed")

    def test_notification_payload_has_ticker(self):
        mock_d = _mock_dispatcher()
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(),
            ticker="SOLUSDT",
            dry_run=True,
        )
        TradeExecutor(dispatcher=mock_d).execute(req)
        call_event = mock_d.dispatch.call_args[0][0]
        self.assertEqual(call_event.payload["ticker"], "SOLUSDT")

    def test_notification_result_in_meta(self):
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(),
            ticker="BTCUSDT",
            dry_run=True,
        )
        result = _executor().execute(req)
        self.assertIn("notif", result.meta)
        self.assertTrue(result.meta["notif"]["ok"])

    def test_notification_dry_run_flag_passed(self):
        mock_d = _mock_dispatcher()
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(),
            ticker="BTCUSDT",
            dry_run=True,
        )
        TradeExecutor(dispatcher=mock_d).execute(req)
        call_dry_run = mock_d.dispatch.call_args[1]["dry_run"]
        self.assertTrue(call_dry_run)


# ---------------------------------------------------------------------------
# Auto request_id + signal_id pass-through
# ---------------------------------------------------------------------------

class TestMisc(unittest.TestCase):

    def test_auto_generates_request_id(self):
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(),
            dry_run=True,
        )
        self.assertEqual(req.request_id, "")
        result = _executor().execute(req)
        self.assertNotEqual(result.request_id, "")

    def test_signal_id_passed_through(self):
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(signal_id="sig-xyz"),
            dry_run=True,
        )
        result = _executor().execute(req)
        self.assertEqual(result.signal_id, "sig-xyz")

    def test_ticker_from_request(self):
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(),
            ticker="XRPUSDT",
            dry_run=True,
        )
        result = _executor().execute(req)
        self.assertEqual(result.ticker, "XRPUSDT")

    def test_ticker_fallback_to_signal_id(self):
        req = TradeRequest(
            gate_decision=_approved_gate(),
            proposition=_prop(signal_id="ADAUSDT-001"),
            ticker="",
            dry_run=True,
        )
        result = _executor().execute(req)
        self.assertEqual(result.ticker, "ADAUSDT-001")


if __name__ == "__main__":
    unittest.main(verbosity=2)
