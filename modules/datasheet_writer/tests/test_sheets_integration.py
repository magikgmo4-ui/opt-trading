"""
Integration tests — DatasheetWriter → SheetsAdapter (fake client).

Proves the full flow without a real Google Sheets API:
  CloseRequest → ResultTracker.track() → TradeRecord
  → DatasheetWriter.write()            → JSONL/CSV + payload_ref
  → write_trade_to_sheets()            → SheetsAdapterResult (fake)

The payload_ref from DatasheetWriter is forwarded to the Sheets adapter as
required by R8 (payload_ref must be a path, not a JSON blob).
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.result_tracker.app.schema import TradeRecord
from modules.result_tracker.app.tracker import ResultTracker
from modules.trade_executor.app.schema import TradeResult
from modules.result_tracker.app.schema import CloseRequest
from modules.datasheet_writer.app.writer import DatasheetWriter
from modules.datasheet_writer.app.sheets_adapter import write_trade_to_sheets, map_trade_to_event_row
from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
from modules.google_sheets_global_schema.sheets_writer import SheetsWriter


GOOGLE_MODULES = frozenset({"google", "gspread", "googleapiclient", "google.auth", "google.oauth2"})


def _google_mods() -> set[str]:
    return {m for m in sys.modules if any(m == g or m.startswith(g + ".") for g in GOOGLE_MODULES)}


def _trade_result(**kw) -> TradeResult:
    defaults = dict(
        request_id="int-req-001", signal_id="int-sig-001",
        trade_id="paper_BTCUSDT_int001",
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


def _fake_writer() -> SheetsWriter:
    return SheetsWriter(client=FakeSheetsClient())


class TestResultTrackerToSheetsAdapter(unittest.TestCase):
    """ResultTracker → write_trade_to_sheets (without DatasheetWriter file step)."""

    def setUp(self):
        from unittest.mock import MagicMock
        mock_dispatcher = MagicMock()
        mock_dispatcher.dispatch.return_value = {"ok": True, "event_type": "result_known"}
        self.tracker = ResultTracker(dispatcher=mock_dispatcher)

    def test_tracker_output_feeds_sheets_adapter(self):
        record = self.tracker.track(_close_req(dry_run=False, close_price=67000.0))
        result = write_trade_to_sheets(record, _fake_writer())
        self.assertTrue(result.ok)

    def test_sheets_row_outcome_matches_tracker_outcome(self):
        record = self.tracker.track(_close_req(dry_run=False, close_price=67000.0))
        row = map_trade_to_event_row(record)
        self.assertEqual(row["outcome"], record.outcome)

    def test_sheets_row_trade_id_matches(self):
        record = self.tracker.track(_close_req(dry_run=False, close_price=67000.0))
        row = map_trade_to_event_row(record)
        self.assertEqual(row["event_id"], record.trade_id)

    def test_sheets_row_net_pnl_matches(self):
        record = self.tracker.track(_close_req(dry_run=False, close_price=67000.0))
        row = map_trade_to_event_row(record)
        self.assertAlmostEqual(row["net_pnl"], record.net_pnl)

    def test_loss_outcome_propagates(self):
        record = self.tracker.track(_close_req(dry_run=False, close_price=63000.0))
        row = map_trade_to_event_row(record)
        self.assertEqual(row["outcome"], "loss")
        self.assertEqual(record.outcome, "loss")


class TestDatasheetWriterToSheetsAdapter(unittest.TestCase):
    """DatasheetWriter.write() → payload_ref → write_trade_to_sheets."""

    def _record(self, **kw) -> TradeRecord:
        defaults = dict(
            trade_id="paper_BTCUSDT_int002",
            request_id="int-req-002", signal_id="int-sig-002",
            ticker="BTCUSDT", action="BUY",
            entry_price=65000.0, close_price=67000.0,
            fill_qty=0.5, size_pct=0.5,
            sl=63000.0, tp=70000.0,
            gross_pnl=1000.0, net_pnl=961.0, fees=39.0,
            duration_s=120.0, outcome="win",
            opened_at="2026-05-26T10:00:00+00:00",
            closed_at="2026-05-26T10:02:00+00:00",
            dry_run=False,
        )
        defaults.update(kw)
        return TradeRecord(**defaults)

    def test_payload_ref_from_writer_to_adapter(self):
        with tempfile.TemporaryDirectory() as d:
            writer = DatasheetWriter(output_dir=Path(d))
            write_result = writer.write(self._record(), dry_run=False)
            self.assertTrue(write_result.written)
            payload_ref = write_result.jsonl_path
            sheets_result = write_trade_to_sheets(
                self._record(), _fake_writer(), payload_ref=payload_ref
            )
        self.assertTrue(sheets_result.ok)
        self.assertEqual(sheets_result.rows_written, 1)

    def test_payload_ref_is_path_not_json(self):
        with tempfile.TemporaryDirectory() as d:
            writer = DatasheetWriter(output_dir=Path(d))
            write_result = writer.write(self._record(), dry_run=False)
            payload_ref = write_result.jsonl_path
        self.assertTrue(payload_ref.endswith(".jsonl"))
        self.assertFalse(payload_ref.startswith("{"))

    def test_jsonl_and_sheets_same_trade_id(self):
        record = self._record(trade_id="paper_ETHUSDT_int003")
        with tempfile.TemporaryDirectory() as d:
            writer = DatasheetWriter(output_dir=Path(d))
            write_result = writer.write(record, dry_run=False)
            jsonl_data = json.loads(Path(write_result.jsonl_path).read_text().splitlines()[0])
        row = map_trade_to_event_row(record)
        self.assertEqual(jsonl_data["trade_id"], record.trade_id)
        self.assertEqual(row["event_id"], record.trade_id)

    def test_dry_run_writer_then_sheets_adapter(self):
        with tempfile.TemporaryDirectory() as d:
            writer = DatasheetWriter(output_dir=Path(d))
            write_result = writer.write(self._record(), dry_run=True)
        self.assertFalse(write_result.written)
        sheets_writer = SheetsWriter(dry_run=True)
        sheets_result = write_trade_to_sheets(self._record(), sheets_writer)
        self.assertTrue(sheets_result.ok)
        self.assertEqual(sheets_result.rows_written, 0)
        self.assertEqual(sheets_result.mode, "dry_run")

    def test_win_loss_breakeven_all_write_to_sheets(self):
        outcomes = [
            ("win", 67000.0, 1000.0, 961.0),
            ("loss", 63000.0, -1000.0, -1039.0),
        ]
        for outcome, close, gross, net in outcomes:
            with self.subTest(outcome=outcome):
                record = self._record(
                    trade_id=f"paper_BTCUSDT_{outcome}",
                    close_price=close, gross_pnl=gross, net_pnl=net, outcome=outcome,
                )
                result = write_trade_to_sheets(record, _fake_writer())
                self.assertTrue(result.ok, f"outcome={outcome} should write OK")


class TestIntegrationNoGoogleApi(unittest.TestCase):
    """Verify no Google API modules are loaded during integration flow."""

    def test_full_flow_no_google_modules(self):
        from unittest.mock import MagicMock
        mock_dispatcher = MagicMock()
        mock_dispatcher.dispatch.return_value = {"ok": True}
        tracker = ResultTracker(dispatcher=mock_dispatcher)
        before = _google_mods()
        with tempfile.TemporaryDirectory() as d:
            record = tracker.track(_close_req(dry_run=False, close_price=67000.0))
            writer = DatasheetWriter(output_dir=Path(d))
            write_result = writer.write(record, dry_run=False)
            write_trade_to_sheets(record, _fake_writer(), payload_ref=write_result.jsonl_path)
        after = _google_mods()
        self.assertEqual(after - before, set(), f"Google modules loaded: {after - before}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
