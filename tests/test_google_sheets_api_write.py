"""
Tests for SheetsWriter + FakeSheetsClient — API write layer V1.

Covers:
- fake client writes all 11 tabs
- validation rules applied before write
- unknown sheet rejected
- missing required column rejected
- duplicate PK rejected
- no real API call without flag
- real client blocked without ALLOW_GOOGLE_SHEETS_API_WRITE=1
- real client blocked without spreadsheet_id
- dry_run produces no writes
- WriteResult fields correct
"""
from __future__ import annotations

import json
import os
import unittest
from pathlib import Path

from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient, WriteRecord
from modules.google_sheets_global_schema.sheets_writer import SheetsWriter, REAL_API_FLAG, WriteResult
from modules.google_sheets_global_schema.validator import CANONICAL_TABS, validate_rows

FIXTURES = Path(__file__).parent / "fixtures" / "google_sheets_global_schema"

ALL_TABS = sorted(CANONICAL_TABS)


def _load_fixture(tab_name: str) -> list[dict]:
    rows = []
    for line in (FIXTURES / f"{tab_name}.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def _fake_writer() -> SheetsWriter:
    return SheetsWriter(client=FakeSheetsClient())


def _dry_run_writer() -> SheetsWriter:
    return SheetsWriter(client=None, dry_run=True)


class TestFakeClientBasics(unittest.TestCase):
    def test_add_worksheet_and_retrieve(self):
        client = FakeSheetsClient()
        ws = client.add_worksheet(title="daily_sessions")
        self.assertEqual(ws.title, "daily_sessions")
        self.assertIs(client.worksheet("daily_sessions"), ws)

    def test_worksheet_not_found_raises(self):
        client = FakeSheetsClient()
        with self.assertRaises(KeyError):
            client.worksheet("nonexistent")

    def test_append_rows_stores_data(self):
        client = FakeSheetsClient()
        ws = client.add_worksheet(title="watchlists")
        ws.append_rows([["wl_1", "BTCUSDT", "H1", "True"]])
        self.assertEqual(client.total_rows_written("watchlists"), 1)

    def test_clear_resets_data(self):
        client = FakeSheetsClient()
        ws = client.add_worksheet(title="watchlists")
        ws.append_rows([["wl_1", "BTCUSDT", "H1", "True"]])
        ws.clear()
        self.assertEqual(ws.row_count, 0)

    def test_write_records_logged(self):
        client = FakeSheetsClient()
        ws = client.add_worksheet(title="watchlists")
        ws.append_rows([["wl_1", "BTCUSDT", "H1", "True"]])
        self.assertEqual(len(client.write_records), 1)
        rec: WriteRecord = client.write_records[0]
        self.assertEqual(rec.sheet_name, "watchlists")
        self.assertEqual(rec.operation, "append_rows")

    def test_reset_clears_all(self):
        client = FakeSheetsClient()
        client.add_worksheet(title="watchlists")
        client.reset()
        self.assertEqual(client.worksheets_created, [])
        self.assertEqual(client.write_records, [])


class TestFakeWriterAllTabs(unittest.TestCase):
    """Each fixture can be written via fake client with 0 validation fails."""

    def _write_tab(self, tab_name: str) -> WriteResult:
        writer = _fake_writer()
        rows = _load_fixture(tab_name)
        return writer.append_rows(tab_name, rows)

    def test_sheets_registry(self):
        r = self._write_tab("sheets_registry")
        self.assertTrue(r.ok, r.error)
        self.assertEqual(r.mode, "fake")
        self.assertGreater(r.rows_written, 0)

    def test_daily_sessions(self):
        r = self._write_tab("daily_sessions")
        self.assertTrue(r.ok, r.error)

    def test_strategy_events(self):
        r = self._write_tab("strategy_events")
        self.assertTrue(r.ok, r.error)

    def test_strategy_perf(self):
        r = self._write_tab("strategy_perf")
        self.assertTrue(r.ok, r.error)

    def test_strategy_gates(self):
        r = self._write_tab("strategy_gates")
        self.assertTrue(r.ok, r.error)

    def test_registry_candidates(self):
        r = self._write_tab("registry_candidates")
        self.assertTrue(r.ok, r.error)

    def test_market_metrics(self):
        r = self._write_tab("market_metrics")
        self.assertTrue(r.ok, r.error)

    def test_desk_snapshots(self):
        r = self._write_tab("desk_snapshots")
        self.assertTrue(r.ok, r.error)

    def test_visual_context(self):
        r = self._write_tab("visual_context")
        self.assertTrue(r.ok, r.error)

    def test_telegram_claims(self):
        r = self._write_tab("telegram_claims")
        self.assertTrue(r.ok, r.error)

    def test_watchlists(self):
        r = self._write_tab("watchlists")
        self.assertTrue(r.ok, r.error)


class TestWriterValidationGates(unittest.TestCase):
    """Validation rules must block writes before reaching the client."""

    def test_unknown_sheet_rejected(self):
        writer = _fake_writer()
        result = writer.append_rows("nonexistent_sheet", [{"foo": "bar"}])
        self.assertFalse(result.ok)
        self.assertIn("CANONICAL_TABS", result.error or "")

    def test_missing_required_column_blocked(self):
        writer = _fake_writer()
        bad_rows = [{"run_id": "r1"}]  # started_at + status missing
        result = writer.append_rows("daily_sessions", bad_rows)
        self.assertFalse(result.ok)
        self.assertTrue(len(result.validation_fails) > 0)
        self.assertEqual(result.rows_written, 0)

    def test_bad_enum_blocked(self):
        writer = _fake_writer()
        bad_rows = [{"run_id": "r1", "started_at": "2026-05-25T08:00:00Z", "status": "unknown"}]
        result = writer.append_rows("daily_sessions", bad_rows)
        self.assertFalse(result.ok)
        self.assertTrue(any("status" in f for f in result.validation_fails))

    def test_bad_timestamp_blocked(self):
        writer = _fake_writer()
        bad_rows = [{"run_id": "r1", "started_at": "2026-05-25 08:00:00", "status": "success"}]
        result = writer.append_rows("daily_sessions", bad_rows)
        self.assertFalse(result.ok)
        self.assertTrue(any("started_at" in f for f in result.validation_fails))

    def test_duplicate_pk_blocked(self):
        writer = _fake_writer()
        rows = [
            {"run_id": "r1", "started_at": "2026-05-25T08:00:00Z", "status": "success"},
            {"run_id": "r1", "started_at": "2026-05-25T09:00:00Z", "status": "fail"},
        ]
        result = writer.append_rows("daily_sessions", rows)
        self.assertFalse(result.ok)
        self.assertTrue(any("R7" in f for f in result.validation_fails))

    def test_ref_payload_blocked(self):
        bad_ref = '{"claim_id": "x", "data": "' + "a" * 80 + '"}'
        writer = _fake_writer()
        bad_rows = [{"claim_id": "c1", "claim_ts": "2026-05-25T08:00:00Z", "claim_type": "ctx", "payload_ref": bad_ref}]
        result = writer.append_rows("telegram_claims", bad_rows)
        self.assertFalse(result.ok)
        self.assertTrue(any("R8" in f for f in result.validation_fails))

    def test_validate_false_bypasses_validation(self):
        writer = _fake_writer()
        bad_rows = [{"run_id": "r1"}]
        result = writer.append_rows("daily_sessions", bad_rows, validate=False)
        # Validation skipped → write proceeds (fake client accepts anything)
        self.assertTrue(result.ok)
        self.assertEqual(result.rows_written, 1)

    def test_validation_result_fields(self):
        writer = _fake_writer()
        bad_rows = [{"run_id": None, "started_at": "2026-05-25T08:00:00Z", "status": "success"}]
        result = writer.append_rows("daily_sessions", bad_rows)
        self.assertIsInstance(result, WriteResult)
        self.assertFalse(result.ok)
        self.assertIsNotNone(result.error)
        self.assertGreater(len(result.validation_fails), 0)
        self.assertEqual(result.rows_written, 0)
        self.assertEqual(result.rows_attempted, 1)


class TestDryRunMode(unittest.TestCase):
    """Dry-run writer must not write anything."""

    def test_dry_run_ok_but_no_write(self):
        writer = _dry_run_writer()
        rows = _load_fixture("watchlists")
        result = writer.append_rows("watchlists", rows)
        self.assertTrue(result.ok)
        self.assertEqual(result.mode, "dry_run")
        self.assertEqual(result.rows_written, 0)
        self.assertGreater(result.rows_attempted, 0)

    def test_dry_run_mode_property(self):
        writer = _dry_run_writer()
        self.assertEqual(writer.mode, "dry_run")

    def test_fake_mode_property(self):
        writer = _fake_writer()
        self.assertEqual(writer.mode, "fake")


class TestRealClientBlocked(unittest.TestCase):
    """Real client must be blocked without explicit flag + spreadsheet_id."""

    class _MockRealClient:
        """Minimal mock that looks like a real gspread client but should never be called."""
        def worksheet(self, name):
            raise AssertionError("Real client called — should have been blocked")

    def setUp(self):
        os.environ.pop(REAL_API_FLAG, None)

    def tearDown(self):
        os.environ.pop(REAL_API_FLAG, None)

    def test_real_client_blocked_without_flag(self):
        writer = SheetsWriter(client=self._MockRealClient(), spreadsheet_id="dummy_id", dry_run=False)
        rows = _load_fixture("watchlists")
        result = writer.append_rows("watchlists", rows)
        self.assertFalse(result.ok)
        self.assertIn(REAL_API_FLAG, result.error or "")

    def test_real_client_blocked_without_spreadsheet_id(self):
        os.environ[REAL_API_FLAG] = "1"
        writer = SheetsWriter(client=self._MockRealClient(), spreadsheet_id=None, dry_run=False)
        rows = _load_fixture("watchlists")
        result = writer.append_rows("watchlists", rows)
        self.assertFalse(result.ok)
        self.assertIn("spreadsheet_id", result.error or "")

    def test_mode_with_no_client_is_dry_run(self):
        writer = SheetsWriter(client=None, dry_run=True)
        self.assertEqual(writer.mode, "dry_run")


class TestEnsureWorksheet(unittest.TestCase):
    def test_ensure_creates_worksheet(self):
        writer = _fake_writer()
        result = writer.ensure_worksheet("daily_sessions")
        self.assertEqual(result["sheet_name"], "daily_sessions")
        self.assertTrue(result["created"])

    def test_ensure_unknown_sheet_raises(self):
        writer = _fake_writer()
        with self.assertRaises(Exception):
            writer.ensure_worksheet("nonexistent")

    def test_ensure_no_client_returns_no_client(self):
        writer = _dry_run_writer()
        result = writer.ensure_worksheet("watchlists")
        self.assertEqual(result["mode"], "no_client")


class TestClearAndWrite(unittest.TestCase):
    def test_clear_and_write_replaces_data(self):
        client = FakeSheetsClient()
        writer = SheetsWriter(client=client)
        rows1 = _load_fixture("watchlists")
        rows2 = [{"watchlist_id": "wl_new", "symbol": "SOLUSDT", "timeframe": "H1", "enabled": True}]
        writer.clear_and_write("watchlists", rows1)
        writer.clear_and_write("watchlists", rows2)
        ops = [r.operation for r in client.write_records]
        self.assertIn("update", ops)

    def test_clear_and_write_validates_before_clear(self):
        writer = _fake_writer()
        bad_rows = [{"watchlist_id": None, "symbol": "BTCUSDT", "timeframe": "H1", "enabled": True}]
        result = writer.clear_and_write("watchlists", bad_rows)
        self.assertFalse(result.ok)
        # No clear should happen if validation fails — rows_written = 0
        self.assertEqual(result.rows_written, 0)
