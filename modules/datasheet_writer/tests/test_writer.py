"""Datasheet writer tests — python3 -m unittest"""
from __future__ import annotations
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.result_tracker.app.schema import TradeRecord
from modules.datasheet_writer.app.schema import WriteResult
from modules.datasheet_writer.app.writer import DatasheetWriter, _CSV_FIELDS


def _record(**kw) -> TradeRecord:
    defaults = dict(
        trade_id="paper_BTCUSDT_abc123",
        request_id="req-001", signal_id="sig-001",
        ticker="BTCUSDT", action="BUY",
        entry_price=65000.0, close_price=67000.0,
        fill_qty=0.5, size_pct=0.5,
        sl=63000.0, tp=70000.0,
        gross_pnl=1000.0, net_pnl=961.0, fees=39.0,
        duration_s=120.0, outcome="win",
        opened_at="2026-05-16T10:00:00+00:00",
        closed_at="2026-05-16T10:02:00+00:00",
        dry_run=True, meta={"notif": {"ok": True}},
    )
    defaults.update(kw)
    return TradeRecord(**defaults)


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------

class TestSchema(unittest.TestCase):

    def test_write_result_defaults(self):
        r = WriteResult(ok=True, dry_run=True, written=False)
        self.assertEqual(r.jsonl_path, "")
        self.assertEqual(r.csv_path, "")
        self.assertEqual(r.error, "")


# ---------------------------------------------------------------------------
# Dry-run tests
# ---------------------------------------------------------------------------

class TestDryRun(unittest.TestCase):

    def test_dry_run_no_file_created(self):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            w.write(_record(), dry_run=True)
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_dry_run_result_ok(self):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            r = w.write(_record(), dry_run=True)
        self.assertTrue(r.ok)
        self.assertTrue(r.dry_run)
        self.assertFalse(r.written)


# ---------------------------------------------------------------------------
# Write tests
# ---------------------------------------------------------------------------

class TestWrite(unittest.TestCase):

    def _write(self, record=None, **kw):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            result = w.write(record or _record(**kw), dry_run=False)
            return result, Path(d)

    def test_write_creates_jsonl(self):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            result = w.write(_record(), dry_run=False)
            self.assertTrue(Path(result.jsonl_path).exists())

    def test_write_creates_csv(self):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            result = w.write(_record(), dry_run=False)
            self.assertTrue(Path(result.csv_path).exists())

    def test_write_result_ok(self):
        result, _ = self._write()
        self.assertTrue(result.ok)
        self.assertFalse(result.dry_run)
        self.assertTrue(result.written)

    def test_write_result_paths_non_empty(self):
        result, _ = self._write()
        self.assertNotEqual(result.jsonl_path, "")
        self.assertNotEqual(result.csv_path, "")

    def test_jsonl_parseable(self):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            result = w.write(_record(), dry_run=False)
            line = Path(result.jsonl_path).read_text().strip()
            data = json.loads(line)
        self.assertEqual(data["trade_id"], "paper_BTCUSDT_abc123")
        self.assertEqual(data["outcome"], "win")

    def test_jsonl_no_meta_field(self):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            result = w.write(_record(), dry_run=False)
            data = json.loads(Path(result.jsonl_path).read_text().strip())
        self.assertNotIn("meta", data)

    def test_csv_has_header_row(self):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            result = w.write(_record(), dry_run=False)
            with open(result.csv_path, newline="") as f:
                reader = csv.reader(f)
                header = next(reader)
        self.assertEqual(header, _CSV_FIELDS)

    def test_csv_header_written_once_on_multiple_appends(self):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            result = w.write(_record(trade_id="t1"), dry_run=False)
            w.write(_record(trade_id="t2"), dry_run=False)
            with open(result.csv_path, newline="") as f:
                rows = list(csv.reader(f))
        # header + 2 data rows
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], _CSV_FIELDS)

    def test_append_multiple_jsonl(self):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            r = w.write(_record(trade_id="t1"), dry_run=False)
            w.write(_record(trade_id="t2"), dry_run=False)
            lines = Path(r.jsonl_path).read_text().strip().splitlines()
        self.assertEqual(len(lines), 2)
        ids = [json.loads(l)["trade_id"] for l in lines]
        self.assertEqual(ids, ["t1", "t2"])

    def test_csv_data_row_values(self):
        with tempfile.TemporaryDirectory() as d:
            w = DatasheetWriter(output_dir=Path(d))
            result = w.write(_record(ticker="ETHUSDT", outcome="loss"), dry_run=False)
            with open(result.csv_path, newline="") as f:
                rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["ticker"], "ETHUSDT")
        self.assertEqual(rows[0]["outcome"], "loss")


if __name__ == "__main__":
    unittest.main(verbosity=2)
