"""Result tracker tests — python3 -m unittest"""
from __future__ import annotations
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.proposition_engine.app.schema import Proposition
from modules.validation_gate.app.schema import GateDecision
from modules.trade_executor.app.schema import TradeResult
from modules.result_tracker.app.schema import CloseRequest, TradeRecord
from modules.result_tracker.app.tracker import ResultTracker, _compute_pnl, _outcome


def _trade_result(**kw) -> TradeResult:
    defaults = dict(
        request_id="req-001", signal_id="sig-001",
        trade_id="paper_BTCUSDT_abc123",
        action="BUY", ticker="BTCUSDT",
        fill_price=65000.0, fill_qty=0.5, size_pct=0.5,
        sl=63000.0, tp=70000.0,
        status="dry_run", reason="paper_filled",
        duration_ms=50, dry_run=True, meta={},
    )
    defaults.update(kw)
    return TradeResult(**defaults)


def _close_req(**kw) -> CloseRequest:
    defaults = dict(
        trade_result=_trade_result(),
        close_price=67000.0,
        dry_run=True,
        fee_rate=0.0006,
    )
    defaults.update(kw)
    return CloseRequest(**defaults)


def _mock_dispatcher():
    d = MagicMock()
    d.dispatch.return_value = {"ok": True, "event_type": "result_known"}
    return d


def _tracker(dispatcher=None) -> ResultTracker:
    return ResultTracker(dispatcher=dispatcher or _mock_dispatcher())


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------

class TestSchema(unittest.TestCase):

    def test_close_request_defaults(self):
        req = CloseRequest(trade_result=_trade_result(), close_price=66000.0)
        self.assertEqual(req.opened_at, 0.0)
        self.assertEqual(req.close_timestamp, 0.0)
        self.assertTrue(req.dry_run)
        self.assertAlmostEqual(req.fee_rate, 0.0006)

    def test_trade_record_has_required_fields(self):
        r = TradeRecord(
            trade_id="t", request_id="r", signal_id="s",
            ticker="X", action="BUY",
            entry_price=100.0, close_price=110.0,
            fill_qty=1.0, size_pct=0.5,
            sl=95.0, tp=115.0,
            gross_pnl=10.0, net_pnl=9.88, fees=0.12,
            duration_s=60.0, outcome="win",
            opened_at="2026-01-01T00:00:00+00:00",
            closed_at="2026-01-01T00:01:00+00:00",
        )
        self.assertTrue(r.dry_run)
        self.assertEqual(r.meta, {})


# ---------------------------------------------------------------------------
# P&L computation unit tests
# ---------------------------------------------------------------------------

class TestComputePnl(unittest.TestCase):

    def test_buy_win(self):
        gross, net, fees = _compute_pnl("BUY", 100.0, 110.0, 1.0, 0.0006)
        self.assertGreater(gross, 0)
        self.assertGreater(net, 0)
        self.assertGreater(fees, 0)

    def test_buy_loss(self):
        gross, net, fees = _compute_pnl("BUY", 100.0, 90.0, 1.0, 0.0006)
        self.assertLess(gross, 0)
        self.assertLess(net, 0)
        self.assertGreater(fees, 0)

    def test_sell_win(self):
        gross, net, fees = _compute_pnl("SELL", 100.0, 90.0, 1.0, 0.0006)
        self.assertGreater(gross, 0)
        self.assertGreater(net, 0)

    def test_sell_loss(self):
        gross, net, fees = _compute_pnl("SELL", 100.0, 110.0, 1.0, 0.0006)
        self.assertLess(gross, 0)
        self.assertLess(net, 0)

    def test_fees_always_positive(self):
        for action in ("BUY", "SELL"):
            _, _, fees = _compute_pnl(action, 100.0, 95.0, 1.0, 0.0006)
            self.assertGreater(fees, 0)

    def test_buy_gross_formula(self):
        gross, _, _ = _compute_pnl("BUY", 65000.0, 67000.0, 0.5, 0.0)
        self.assertAlmostEqual(gross, (67000.0 - 65000.0) * 0.5)

    def test_sell_gross_formula(self):
        gross, _, _ = _compute_pnl("SELL", 65000.0, 63000.0, 0.5, 0.0)
        self.assertAlmostEqual(gross, (65000.0 - 63000.0) * 0.5)

    def test_net_equals_gross_minus_fees(self):
        gross, net, fees = _compute_pnl("BUY", 100.0, 110.0, 1.0, 0.001)
        self.assertAlmostEqual(net, gross - fees, places=6)


# ---------------------------------------------------------------------------
# Outcome tests
# ---------------------------------------------------------------------------

class TestOutcome(unittest.TestCase):

    def test_win(self):
        self.assertEqual(_outcome(10.0), "win")

    def test_loss(self):
        self.assertEqual(_outcome(-5.0), "loss")

    def test_breakeven_exact_zero(self):
        self.assertEqual(_outcome(0.0), "breakeven")

    def test_breakeven_near_zero(self):
        self.assertEqual(_outcome(1e-10), "breakeven")


# ---------------------------------------------------------------------------
# ResultTracker integration tests
# ---------------------------------------------------------------------------

class TestResultTracker(unittest.TestCase):

    def test_track_returns_trade_record(self):
        req = _close_req()
        record = _tracker().track(req)
        self.assertIsInstance(record, TradeRecord)

    def test_track_buy_win_outcome(self):
        # entry=65000, close=67000 → win
        req = _close_req(close_price=67000.0)
        record = _tracker().track(req)
        self.assertEqual(record.outcome, "win")

    def test_track_buy_loss_outcome(self):
        req = _close_req(close_price=60000.0)
        record = _tracker().track(req)
        self.assertEqual(record.outcome, "loss")

    def test_track_fields_populated(self):
        req = _close_req(close_price=67000.0)
        record = _tracker().track(req)
        self.assertEqual(record.ticker, "BTCUSDT")
        self.assertEqual(record.action, "BUY")
        self.assertEqual(record.entry_price, 65000.0)
        self.assertEqual(record.close_price, 67000.0)

    def test_track_result_known_notification_sent(self):
        mock_d = _mock_dispatcher()
        req = _close_req()
        ResultTracker(dispatcher=mock_d).track(req)
        mock_d.dispatch.assert_called_once()

    def test_track_notification_event_type(self):
        mock_d = _mock_dispatcher()
        ResultTracker(dispatcher=mock_d).track(_close_req())
        call_event = mock_d.dispatch.call_args[0][0]
        self.assertEqual(call_event.event_type, "result_known")

    def test_track_notification_payload_has_pnl(self):
        mock_d = _mock_dispatcher()
        ResultTracker(dispatcher=mock_d).track(_close_req())
        payload = mock_d.dispatch.call_args[0][0].payload
        self.assertIn("net_pnl", payload)
        self.assertIn("gross_pnl", payload)

    def test_track_dry_run_still_computes_pnl(self):
        req = _close_req(dry_run=True, close_price=67000.0)
        record = _tracker().track(req)
        self.assertNotEqual(record.gross_pnl, 0.0)
        self.assertTrue(record.dry_run)

    def test_track_duration_non_negative(self):
        record = _tracker().track(_close_req())
        self.assertGreaterEqual(record.duration_s, 0.0)

    def test_track_opened_at_closed_at_iso(self):
        record = _tracker().track(_close_req())
        self.assertIn("T", record.opened_at)
        self.assertIn("T", record.closed_at)

    def test_track_meta_has_notif(self):
        record = _tracker().track(_close_req())
        self.assertIn("notif", record.meta)

    def test_track_sell_win(self):
        req = _close_req(
            trade_result=_trade_result(action="SELL", fill_price=65000.0),
            close_price=63000.0,
        )
        record = _tracker().track(req)
        self.assertEqual(record.outcome, "win")


if __name__ == "__main__":
    unittest.main(verbosity=2)
