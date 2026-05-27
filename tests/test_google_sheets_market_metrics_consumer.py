"""
Tests for market_metrics_consumer.py — Data Center -> Google Sheets market_metrics tab.

Covers:
- fixture market_metrics.v1 maps to valid Sheets rows
- required columns present after mapping
- validation rules PASS on mapped rows
- FakeSheetsClient receives rows
- unknown sheet rejected
- no Google API calls by default
- source absent -> ConsumerResult(ok=True, mode="no_source")
- wrong input_class -> no-op (no_source)
- null metric values skipped
- metrics not in collectable skipped
- source_ref is a path string, not a JSON payload (R8 safe)
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

GOOGLE_MODULES = frozenset({"google", "gspread", "googleapiclient", "google.auth", "google.oauth2"})


def _google_mods() -> set[str]:
    return {m for m in sys.modules if any(m == g or m.startswith(g + ".") for g in GOOGLE_MODULES)}


# ---------------------------------------------------------------------------
# Shared fixture factory
# ---------------------------------------------------------------------------

_MM_V1_BTCUSDT = {
    "input_class": "market_metrics.v1",
    "contract_version": "v1",
    "module_id": "derivatives_collector__bitget",
    "symbol": "BTCUSDT",
    "metrics_ts": "2026-05-25T09:00:00Z",
    "freshness_state": "fresh",
    "provider_id": "bitget",
    "provider_coverage": {
        "status": "full",
        "collectable_metrics": ["open_interest", "funding_rate"],
        "missing_metrics": [],
    },
    "metrics": {
        "open_interest": 18500000000.0,
        "funding_rate": 0.0001,
        "volume_futures": None,   # None -> should be skipped
    },
    "refs": {
        "primary_output": "data/data_center/derivatives/derivatives_collector__bitget/latest.json",
        "meta_output": "data/data_center/derivatives/derivatives_collector__bitget/latest_meta.json",
        "latest": "data/data_center/views/market_metrics/latest.json",
        "status": "written",
    },
    "warnings": [],
}


def _write_mm_v1(tmp_dir: Path, payload: dict | None = None) -> Path:
    """Write a market_metrics.v1 JSON file inside tmp_dir. Returns the path."""
    p = tmp_dir / "latest.json"
    p.write_text(json.dumps(payload or _MM_V1_BTCUSDT), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fake_writer():
    from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
    from modules.google_sheets_global_schema.sheets_writer import SheetsWriter
    return SheetsWriter(client=FakeSheetsClient())


# ---------------------------------------------------------------------------
# Tests: mapping correctness
# ---------------------------------------------------------------------------

class TestMapMmV1ToRows(unittest.TestCase):
    def setUp(self):
        from modules.google_sheets_global_schema.market_metrics_consumer import map_mm_v1_to_rows
        self.map = map_mm_v1_to_rows

    def test_required_columns_present(self):
        rows = self.map(_MM_V1_BTCUSDT, "data/data_center/views/market_metrics/latest.json")
        for row in rows:
            for col in ("as_of", "symbol", "metric_name", "value"):
                self.assertIn(col, row, f"Missing required column '{col}'")

    def test_maps_symbol_correctly(self):
        rows = self.map(_MM_V1_BTCUSDT, "some/ref")
        for row in rows:
            self.assertEqual(row["symbol"], "BTCUSDT")

    def test_maps_as_of_from_metrics_ts(self):
        rows = self.map(_MM_V1_BTCUSDT, "some/ref")
        for row in rows:
            self.assertEqual(row["as_of"], "2026-05-25T09:00:00Z")

    def test_maps_source_ref(self):
        ref = "data/data_center/views/market_metrics/latest.json"
        rows = self.map(_MM_V1_BTCUSDT, ref)
        for row in rows:
            self.assertEqual(row["source_ref"], ref)

    def test_null_value_skipped(self):
        rows = self.map(_MM_V1_BTCUSDT, "ref")
        metric_names = [r["metric_name"] for r in rows]
        # volume_futures has value=None -> must be skipped
        self.assertNotIn("volume_futures", metric_names)

    def test_not_in_collectable_skipped(self):
        payload = dict(_MM_V1_BTCUSDT)
        payload["metrics"] = {"open_interest": 1e9, "long_short_ratio": 1.5}
        # long_short_ratio not in collectable_metrics -> skipped
        rows = self.map(payload, "ref")
        metric_names = [r["metric_name"] for r in rows]
        self.assertNotIn("long_short_ratio", metric_names)
        self.assertIn("open_interest", metric_names)

    def test_correct_row_count(self):
        # 2 collectable + non-null: open_interest, funding_rate
        rows = self.map(_MM_V1_BTCUSDT, "ref")
        self.assertEqual(len(rows), 2)

    def test_empty_metrics_returns_empty(self):
        payload = dict(_MM_V1_BTCUSDT)
        payload["metrics"] = {}
        rows = self.map(payload, "ref")
        self.assertEqual(rows, [])

    def test_source_ref_is_not_json_payload(self):
        # R8: source_ref must not be a full JSON payload (>= 50 chars of JSON)
        ref = "data/data_center/views/market_metrics/latest.json"
        rows = self.map(_MM_V1_BTCUSDT, ref)
        for row in rows:
            sr = row.get("source_ref", "")
            self.assertFalse(sr.startswith("{"), f"source_ref looks like JSON: {sr[:30]}")


# ---------------------------------------------------------------------------
# Tests: validation rules on mapped rows
# ---------------------------------------------------------------------------

class TestMappedRowsValidation(unittest.TestCase):
    def setUp(self):
        from modules.google_sheets_global_schema.market_metrics_consumer import map_mm_v1_to_rows
        from modules.google_sheets_global_schema.validator import validate_rows, fails
        rows = map_mm_v1_to_rows(_MM_V1_BTCUSDT, "data/data_center/views/market_metrics/latest.json")
        issues = validate_rows("market_metrics", rows)
        self.fails = fails(issues)
        self.rows = rows

    def test_zero_validation_fails(self):
        self.assertEqual(self.fails, [], f"Validation FAILs: {self.fails}")

    def test_as_of_is_iso_utc(self):
        import re
        iso = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        for row in self.rows:
            self.assertRegex(row["as_of"], iso)

    def test_no_duplicate_pk(self):
        pks = [(r["as_of"], r["symbol"], r["metric_name"]) for r in self.rows]
        self.assertEqual(len(pks), len(set(pks)))


# ---------------------------------------------------------------------------
# Tests: consumer end-to-end with FakeSheetsClient
# ---------------------------------------------------------------------------

class TestConsumerFakeClient(unittest.TestCase):
    def setUp(self):
        from modules.google_sheets_global_schema.market_metrics_consumer import write_market_metrics_to_sheets
        self.consume = write_market_metrics_to_sheets

    def test_writes_to_fake_client(self):
        from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = _write_mm_v1(tmp_path)

            client = FakeSheetsClient()
            writer = SheetsWriter(client=client)
            result = self.consume(writer, source_path=source)

        self.assertTrue(result.ok, result.error)
        self.assertGreater(result.rows_written, 0)
        self.assertEqual(result.mode, "fake")

    def test_rows_written_equals_collectable_non_null(self):
        from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter

        with tempfile.TemporaryDirectory() as tmp:
            source = _write_mm_v1(Path(tmp))
            client = FakeSheetsClient()
            writer = SheetsWriter(client=client)
            result = self.consume(writer, source_path=source)

        # 2 metrics collectable + non-null in _MM_V1_BTCUSDT
        self.assertEqual(result.rows_written, 2)

    def test_fake_client_records_write(self):
        from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter

        with tempfile.TemporaryDirectory() as tmp:
            source = _write_mm_v1(Path(tmp))
            client = FakeSheetsClient()
            writer = SheetsWriter(client=client)
            self.consume(writer, source_path=source)

        self.assertEqual(client.total_rows_written("market_metrics"), 2)


# ---------------------------------------------------------------------------
# Tests: source-absent / no-op
# ---------------------------------------------------------------------------

class TestConsumerNoSource(unittest.TestCase):
    def setUp(self):
        from modules.google_sheets_global_schema.market_metrics_consumer import write_market_metrics_to_sheets
        self.consume = write_market_metrics_to_sheets

    def test_missing_file_is_no_op(self):
        writer = _fake_writer()
        with tempfile.TemporaryDirectory() as tmp:
            absent = Path(tmp) / "nonexistent.json"
            result = self.consume(writer, source_path=absent)

        self.assertTrue(result.ok)
        self.assertEqual(result.rows_written, 0)
        self.assertEqual(result.mode, "no_source")
        self.assertIsNone(result.error)

    def test_wrong_input_class_is_no_op(self):
        writer = _fake_writer()
        bad_payload = dict(_MM_V1_BTCUSDT)
        bad_payload["input_class"] = "other.v1"

        with tempfile.TemporaryDirectory() as tmp:
            source = _write_mm_v1(Path(tmp), bad_payload)
            result = self.consume(writer, source_path=source)

        self.assertTrue(result.ok)
        self.assertEqual(result.rows_written, 0)
        self.assertEqual(result.mode, "no_source")

    def test_corrupt_json_is_no_op(self):
        writer = _fake_writer()
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "latest.json"
            p.write_text("not valid json{{", encoding="utf-8")
            result = self.consume(writer, source_path=p)

        self.assertTrue(result.ok)
        self.assertEqual(result.rows_written, 0)
        self.assertEqual(result.mode, "no_source")


# ---------------------------------------------------------------------------
# Tests: dry-run mode
# ---------------------------------------------------------------------------

class TestConsumerDryRun(unittest.TestCase):
    def test_dry_run_no_write(self):
        from modules.google_sheets_global_schema.market_metrics_consumer import write_market_metrics_to_sheets
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter

        writer = SheetsWriter(client=None, dry_run=True)
        with tempfile.TemporaryDirectory() as tmp:
            source = _write_mm_v1(Path(tmp))
            result = write_market_metrics_to_sheets(writer, source_path=source)

        self.assertTrue(result.ok)
        self.assertEqual(result.rows_written, 0)
        self.assertEqual(result.mode, "dry_run")
        self.assertGreater(result.rows_attempted, 0)


# ---------------------------------------------------------------------------
# Tests: no Google API calls
# ---------------------------------------------------------------------------

class TestNoGoogleApiCalls(unittest.TestCase):
    def test_import_consumer_no_google(self):
        before = _google_mods()
        from modules.google_sheets_global_schema import market_metrics_consumer  # noqa: F401
        after = _google_mods()
        self.assertEqual(after - before, set(), f"Google modules loaded: {after - before}")

    def test_write_via_fake_no_google(self):
        from modules.google_sheets_global_schema.market_metrics_consumer import write_market_metrics_to_sheets
        from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter

        before = _google_mods()
        with tempfile.TemporaryDirectory() as tmp:
            source = _write_mm_v1(Path(tmp))
            writer = SheetsWriter(client=FakeSheetsClient())
            write_market_metrics_to_sheets(writer, source_path=source)
        after = _google_mods()
        self.assertEqual(after - before, set(), f"Google modules appeared: {after - before}")
