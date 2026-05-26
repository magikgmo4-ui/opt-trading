"""
Tests for google_sheets__market_reporting consumer wiring (PF_GOOGLE_SHEETS_CONSUMER).
"""
import json
import tempfile
import unittest
from pathlib import Path


_MM_V1 = {
    "input_class": "market_metrics.v1",
    "symbol": "BTCUSDT",
    "metrics_ts": "2026-05-26T10:00:00Z",
    "provider_coverage": {"collectable_metrics": ["open_interest", "funding_rate"]},
    "metrics": {"open_interest": 123.0, "funding_rate": 0.0001, "volume_futures": None},
}


def _write_latest_mm_v1(root: Path) -> Path:
    p = root / "data" / "data_center" / "views" / "market_metrics" / "latest.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(_MM_V1), encoding="utf-8")
    return p


class TestGoogleSheetsMarketReportingConsumer(unittest.TestCase):
    def test_writes_to_fake_client(self):
        from modules.data_center.google_sheets_market_reporting_consumer import consume_google_sheets_market_reporting
        from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_latest_mm_v1(root)
            client = FakeSheetsClient()
            writer = SheetsWriter(client=client)
            result = consume_google_sheets_market_reporting(writer, root=root)

        self.assertTrue(result.ok, result.error)
        self.assertEqual(result.mode, "fake")
        self.assertEqual(result.rows_written, 2)

    def test_missing_source_raises(self):
        from modules.data_center.google_sheets_market_reporting_consumer import consume_google_sheets_market_reporting
        from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = FakeSheetsClient()
            writer = SheetsWriter(client=client)
            with self.assertRaises(FileNotFoundError):
                consume_google_sheets_market_reporting(writer, root=root)

    def test_wrong_input_class_raises(self):
        from modules.data_center.google_sheets_market_reporting_consumer import consume_google_sheets_market_reporting
        from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = _write_latest_mm_v1(root)
            payload = dict(_MM_V1)
            payload["input_class"] = "other.v1"
            p.write_text(json.dumps(payload), encoding="utf-8")
            client = FakeSheetsClient()
            writer = SheetsWriter(client=client)
            with self.assertRaises(ValueError):
                consume_google_sheets_market_reporting(writer, root=root)
