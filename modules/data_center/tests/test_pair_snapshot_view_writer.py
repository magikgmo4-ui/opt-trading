import json
import shutil
import tempfile
import unittest
from pathlib import Path

from modules.data_center.pair_snapshot_view_writer import write_pair_market_snapshot_view

_SINGLE_RECORD_PAYLOAD = {
    "contract_version": "v1",
    "schema_version": "v1",
    "module_id": "collector_binance_spot",
    "provider_id": "binance_spot",
    "run_id": "20260523_000000_test",
    "generated_at": "2026-05-23T00:00:00Z",
    "entity_type": "pair_market_snapshot",
    "records": [
        {
            "pair_symbol": "BTCUSDT",
            "base_asset": "BTC",
            "quote_asset": "USDT",
            "trading_status": "TRADING",
            "is_spot_trading_allowed": True,
            "last_price": "51200.00",
            "open_price_24h": "50500.00",
            "high_price_24h": "51500.00",
            "low_price_24h": "50000.00",
            "price_change_percent_24h": "1.25",
            "volume_base_24h": "1234.56000000",
            "volume_quote_24h": "63000000.00000000",
            "trade_count_24h": 111111,
            "window_open_at": "2026-05-23T00:00:00Z",
            "window_close_at": "2026-05-23T08:00:00Z",
            "weighted_avg_price_24h": "51000.00",
            "source": {"provider_symbol": "BTCUSDT"},
        }
    ],
}

_TWO_RECORD_PAYLOAD = {
    **_SINGLE_RECORD_PAYLOAD,
    "records": [
        {**_SINGLE_RECORD_PAYLOAD["records"][0]},
        {
            **_SINGLE_RECORD_PAYLOAD["records"][0],
            "pair_symbol": "ETHUSDT",
            "base_asset": "ETH",
            "source": {"provider_symbol": "ETHUSDT"},
        },
    ],
}


class TestWritePairSnapshotView(unittest.TestCase):
    def test_view_writes_latest(self):
        td = Path(tempfile.mkdtemp())
        try:
            result = write_pair_market_snapshot_view(_SINGLE_RECORD_PAYLOAD, root=td)
            expected = td / "data/data_center/views/pair_market_snapshot/latest.json"
            self.assertEqual(result["latest"], expected)
            self.assertTrue(expected.exists())
        finally:
            shutil.rmtree(td)

    def test_view_writes_by_symbol(self):
        td = Path(tempfile.mkdtemp())
        try:
            result = write_pair_market_snapshot_view(_SINGLE_RECORD_PAYLOAD, root=td)
            expected = td / "data/data_center/views/pair_market_snapshot/by_symbol/BTCUSDT.json"
            self.assertIn("BTCUSDT", result["by_symbol"])
            self.assertEqual(result["by_symbol"]["BTCUSDT"], expected)
            self.assertTrue(expected.exists())
        finally:
            shutil.rmtree(td)

    def test_view_latest_path_has_no_producer_id(self):
        td = Path(tempfile.mkdtemp())
        try:
            result = write_pair_market_snapshot_view(_SINGLE_RECORD_PAYLOAD, root=td)
            path_str = str(result["latest"])
            self.assertNotIn("collector_binance_spot", path_str)
            self.assertNotIn("binance_spot", path_str)
            self.assertIn("views/pair_market_snapshot", path_str)
        finally:
            shutil.rmtree(td)

    def test_view_by_symbol_path_has_no_producer_id(self):
        td = Path(tempfile.mkdtemp())
        try:
            result = write_pair_market_snapshot_view(_SINGLE_RECORD_PAYLOAD, root=td)
            for sym, path in result["by_symbol"].items():
                path_str = str(path)
                self.assertNotIn("collector_binance_spot", path_str)
                self.assertNotIn("binance_spot", path_str)
                self.assertIn("views/pair_market_snapshot/by_symbol", path_str)
        finally:
            shutil.rmtree(td)

    def test_view_latest_content_is_valid(self):
        td = Path(tempfile.mkdtemp())
        try:
            result = write_pair_market_snapshot_view(_SINGLE_RECORD_PAYLOAD, root=td)
            data = json.loads(result["latest"].read_text(encoding="utf-8"))
            self.assertEqual(data["entity_type"], "pair_market_snapshot")
            self.assertEqual(data["module_id"], "collector_binance_spot")
            self.assertEqual(len(data["records"]), 1)
            self.assertEqual(data["records"][0]["pair_symbol"], "BTCUSDT")
        finally:
            shutil.rmtree(td)

    def test_view_by_symbol_content_is_self_contained(self):
        """by_symbol doc has all metadata fields plus record fields."""
        td = Path(tempfile.mkdtemp())
        try:
            result = write_pair_market_snapshot_view(_SINGLE_RECORD_PAYLOAD, root=td)
            data = json.loads(result["by_symbol"]["BTCUSDT"].read_text(encoding="utf-8"))
            self.assertEqual(data["entity_type"], "pair_market_snapshot")
            self.assertEqual(data["pair_symbol"], "BTCUSDT")
            self.assertEqual(data["last_price"], "51200.00")
            self.assertEqual(data["module_id"], "collector_binance_spot")
        finally:
            shutil.rmtree(td)

    def test_view_multi_record_writes_each_symbol(self):
        td = Path(tempfile.mkdtemp())
        try:
            result = write_pair_market_snapshot_view(_TWO_RECORD_PAYLOAD, root=td)
            self.assertIn("BTCUSDT", result["by_symbol"])
            self.assertIn("ETHUSDT", result["by_symbol"])
            self.assertTrue(result["by_symbol"]["BTCUSDT"].exists())
            self.assertTrue(result["by_symbol"]["ETHUSDT"].exists())
        finally:
            shutil.rmtree(td)

    def test_view_refuses_wrong_entity_type(self):
        td = Path(tempfile.mkdtemp())
        try:
            bad = {**_SINGLE_RECORD_PAYLOAD, "entity_type": "market_metrics"}
            with self.assertRaises(ValueError) as ctx:
                write_pair_market_snapshot_view(bad, root=td)
            self.assertIn("entity_type", str(ctx.exception))
        finally:
            shutil.rmtree(td)

    def test_view_refuses_missing_entity_type(self):
        td = Path(tempfile.mkdtemp())
        try:
            bad = {k: v for k, v in _SINGLE_RECORD_PAYLOAD.items() if k != "entity_type"}
            with self.assertRaises(ValueError):
                write_pair_market_snapshot_view(bad, root=td)
        finally:
            shutil.rmtree(td)

    def test_view_creates_missing_directories(self):
        td = Path(tempfile.mkdtemp())
        try:
            view_dir = td / "data/data_center/views/pair_market_snapshot"
            self.assertFalse(view_dir.exists())
            write_pair_market_snapshot_view(_SINGLE_RECORD_PAYLOAD, root=td)
            self.assertTrue(view_dir.is_dir())
            self.assertTrue((view_dir / "by_symbol").is_dir())
        finally:
            shutil.rmtree(td)

    def test_view_empty_records_writes_latest_only(self):
        td = Path(tempfile.mkdtemp())
        try:
            empty = {**_SINGLE_RECORD_PAYLOAD, "records": []}
            result = write_pair_market_snapshot_view(empty, root=td)
            self.assertTrue(result["latest"].exists())
            self.assertEqual(result["by_symbol"], {})
        finally:
            shutil.rmtree(td)


if __name__ == "__main__":
    unittest.main()
