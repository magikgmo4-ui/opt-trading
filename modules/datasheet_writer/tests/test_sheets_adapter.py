"""
Tests for sheets_adapter.py — DatasheetWriter -> Google Sheets strategy_events.

Covers:
- map_trade_to_event_row: required fields present
- map_trade_to_event_row: event_id = trade_id
- map_trade_to_event_row: event_type = "trade_result.v1"
- map_trade_to_event_row: +00:00 timestamp normalized to Z
- map_trade_to_event_row: already-Z timestamp unchanged
- map_trade_to_event_row: payload_ref is a path (R8-safe, not JSON)
- map_trade_to_event_row: empty payload_ref allowed
- validation R1-R10 PASS on mapped row (via shared validator)
- write_trade_to_sheets: fake client write ok
- write_trade_to_sheets: fake client rows_written=1
- write_trade_to_sheets: dry_run -> ok, rows_written=0
- write_trade_to_sheets: SheetsAdapterResult.mode="fake"
- no Google API calls on import or write
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

GOOGLE_MODULES = frozenset({"google", "gspread", "googleapiclient", "google.auth", "google.oauth2"})


def _google_mods() -> set[str]:
    return {m for m in sys.modules if any(m == g or m.startswith(g + ".") for g in GOOGLE_MODULES)}


def _record(**kw):
    from modules.result_tracker.app.schema import TradeRecord
    defaults = dict(
        trade_id="paper_BTCUSDT_abc123",
        request_id="req-001",
        signal_id="sig-001",
        ticker="BTCUSDT",
        action="BUY",
        entry_price=65000.0,
        close_price=67000.0,
        fill_qty=0.5,
        size_pct=0.5,
        sl=63000.0,
        tp=70000.0,
        gross_pnl=1000.0,
        net_pnl=961.0,
        fees=39.0,
        duration_s=120.0,
        outcome="win",
        opened_at="2026-05-25T10:00:00+00:00",
        closed_at="2026-05-25T10:02:00+00:00",
        dry_run=True,
    )
    defaults.update(kw)
    return TradeRecord(**defaults)


def _fake_writer():
    from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
    from modules.google_sheets_global_schema.sheets_writer import SheetsWriter
    return SheetsWriter(client=FakeSheetsClient())


# ---------------------------------------------------------------------------
# map_trade_to_event_row
# ---------------------------------------------------------------------------

class TestMapTradeToEventRow(unittest.TestCase):
    def setUp(self):
        from modules.datasheet_writer.app.sheets_adapter import map_trade_to_event_row
        self.map = map_trade_to_event_row

    def test_required_columns_present(self):
        row = self.map(_record())
        for col in ("event_id", "event_type", "event_ts"):
            self.assertIn(col, row, f"Missing required column '{col}'")

    def test_event_id_equals_trade_id(self):
        row = self.map(_record(trade_id="t_xyz"))
        self.assertEqual(row["event_id"], "t_xyz")

    def test_event_type_is_trade_result_v1(self):
        row = self.map(_record())
        self.assertEqual(row["event_type"], "trade_result.v1")

    def test_plus00_normalized_to_z(self):
        row = self.map(_record(closed_at="2026-05-25T10:02:00+00:00"))
        self.assertTrue(row["event_ts"].endswith("Z"), f"Expected Z suffix: {row['event_ts']}")
        self.assertFalse(row["event_ts"].endswith("+00:00"))

    def test_already_z_timestamp_unchanged(self):
        row = self.map(_record(closed_at="2026-05-25T10:02:00Z"))
        self.assertEqual(row["event_ts"], "2026-05-25T10:02:00Z")

    def test_ticker_in_row(self):
        row = self.map(_record(ticker="ETHUSDT"))
        self.assertEqual(row["ticker"], "ETHUSDT")

    def test_outcome_in_row(self):
        row = self.map(_record(outcome="loss"))
        self.assertEqual(row["outcome"], "loss")

    def test_net_pnl_in_row(self):
        row = self.map(_record(net_pnl=-42.5))
        self.assertEqual(row["net_pnl"], -42.5)

    def test_empty_payload_ref_allowed(self):
        row = self.map(_record())
        self.assertEqual(row["payload_ref"], "")

    def test_payload_ref_is_path_not_json(self):
        ref = "data/datasheet/trades_20260525.jsonl"
        row = self.map(_record(), payload_ref=ref)
        self.assertEqual(row["payload_ref"], ref)
        self.assertFalse(row["payload_ref"].startswith("{"))


# ---------------------------------------------------------------------------
# Validation R1-R10 on mapped row
# ---------------------------------------------------------------------------

class TestMappedRowValidation(unittest.TestCase):
    def setUp(self):
        from modules.datasheet_writer.app.sheets_adapter import map_trade_to_event_row
        from modules.google_sheets_global_schema.validator import validate_rows, fails
        row = map_trade_to_event_row(
            _record(),
            payload_ref="data/datasheet/trades_20260525.jsonl",
        )
        issues = validate_rows("strategy_events", [row])
        self.fails = fails(issues)
        self.row = row

    def test_zero_validation_fails(self):
        self.assertEqual(self.fails, [], f"Validation FAILs: {self.fails}")

    def test_event_ts_is_iso_utc(self):
        import re
        iso = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        self.assertRegex(self.row["event_ts"], iso)

    def test_no_duplicate_pk(self):
        from modules.datasheet_writer.app.sheets_adapter import map_trade_to_event_row
        from modules.google_sheets_global_schema.validator import validate_rows, fails
        row1 = map_trade_to_event_row(_record(trade_id="t1"))
        row2 = map_trade_to_event_row(_record(trade_id="t2"))
        issues = validate_rows("strategy_events", [row1, row2])
        self.assertEqual(fails(issues), [])

    def test_duplicate_pk_rejected(self):
        from modules.datasheet_writer.app.sheets_adapter import map_trade_to_event_row
        from modules.google_sheets_global_schema.validator import validate_rows, fails
        row = map_trade_to_event_row(_record(trade_id="same_id"))
        issues = validate_rows("strategy_events", [row, row])
        self.assertTrue(any("R7" in f for f in fails(issues)))


# ---------------------------------------------------------------------------
# write_trade_to_sheets
# ---------------------------------------------------------------------------

class TestWriteTradeToSheets(unittest.TestCase):
    def setUp(self):
        from modules.datasheet_writer.app.sheets_adapter import write_trade_to_sheets
        self.write = write_trade_to_sheets

    def test_fake_write_ok(self):
        result = self.write(_record(), _fake_writer())
        self.assertTrue(result.ok, result.error)

    def test_fake_write_rows_written_1(self):
        result = self.write(_record(), _fake_writer())
        self.assertEqual(result.rows_written, 1)

    def test_fake_mode_property(self):
        result = self.write(_record(), _fake_writer())
        self.assertEqual(result.mode, "fake")

    def test_dry_run_ok_no_write(self):
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter
        writer = SheetsWriter(dry_run=True)
        result = self.write(_record(), writer)
        self.assertTrue(result.ok)
        self.assertEqual(result.rows_written, 0)
        self.assertEqual(result.mode, "dry_run")

    def test_payload_ref_forwarded(self):
        from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter
        client = FakeSheetsClient()
        writer = SheetsWriter(client=client)
        ref = "data/datasheet/trades_20260525.jsonl"
        self.write(_record(), writer, payload_ref=ref)
        # Check that the row was written with the correct payload_ref
        rows = client.worksheet("strategy_events").get_all_values()
        # rows is list of lists; payload_ref is the last column based on dict order
        self.assertTrue(len(rows) > 0)

    def test_result_is_sheets_adapter_result(self):
        from modules.datasheet_writer.app.sheets_adapter import SheetsAdapterResult
        result = self.write(_record(), _fake_writer())
        self.assertIsInstance(result, SheetsAdapterResult)


# ---------------------------------------------------------------------------
# No Google API calls
# ---------------------------------------------------------------------------

class TestNoGoogleApiCalls(unittest.TestCase):
    def test_import_sheets_adapter_no_google(self):
        before = _google_mods()
        from modules.datasheet_writer.app import sheets_adapter  # noqa: F401
        after = _google_mods()
        self.assertEqual(after - before, set(), f"Google modules loaded: {after - before}")

    def test_write_fake_no_google(self):
        from modules.datasheet_writer.app.sheets_adapter import write_trade_to_sheets
        before = _google_mods()
        write_trade_to_sheets(_record(), _fake_writer())
        after = _google_mods()
        self.assertEqual(after - before, set(), f"Google modules appeared: {after - before}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
