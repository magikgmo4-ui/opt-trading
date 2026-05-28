import json
import shutil
import tempfile
import unittest
from pathlib import Path

from modules.data_center.spot_snapshot_dc_writer import write_spot_snapshot_to_data_center

_PAYLOAD = {
    "schema": "pair_market_snapshot.v1",
    "contract_version": "v1",
    "schema_version": "v1",
    "module_id": "collector_binance_spot",
    "provider_id": "binance_spot",
    "run_id": "20260525_000000_test",
    "generated_at": "2026-05-25T00:00:00Z",
    "entity_type": "pair_market_snapshot",
    "records": [
        {
            "pair_symbol": "BTCUSDT",
            "base_asset": "BTC",
            "quote_asset": "USDT",
            "trading_status": "TRADING",
            "is_spot_trading_allowed": True,
            "last_price": "67800.00",
            "open_price_24h": "66500.00",
            "high_price_24h": "68200.00",
            "low_price_24h": "66100.00",
            "price_change_percent_24h": "1.95",
            "volume_base_24h": "1500.00000000",
            "volume_quote_24h": "101700000.00000000",
            "trade_count_24h": 250000,
            "window_open_at": "2026-05-24T00:00:00Z",
            "window_close_at": "2026-05-25T00:00:00Z",
            "weighted_avg_price_24h": "67600.00",
            "source": {"provider_symbol": "BTCUSDT"},
        }
    ],
}


class TestSpotSnapshotDcWriter(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_writes_producer_path(self):
        result = write_spot_snapshot_to_data_center(_PAYLOAD, root=self.tmp, update_registry=False)
        producer_path = self.tmp / "data/data_center/spot/collector_binance_spot/latest.json"
        self.assertTrue(producer_path.exists(), f"Producer path not written: {producer_path}")

    def test_producer_path_contains_payload(self):
        write_spot_snapshot_to_data_center(_PAYLOAD, root=self.tmp, update_registry=False)
        producer_path = self.tmp / "data/data_center/spot/collector_binance_spot/latest.json"
        data = json.loads(producer_path.read_text(encoding="utf-8"))
        self.assertEqual(data["entity_type"], "pair_market_snapshot")
        self.assertEqual(len(data["records"]), 1)

    def test_writes_consumer_view_latest(self):
        write_spot_snapshot_to_data_center(_PAYLOAD, root=self.tmp, update_registry=False)
        view_path = self.tmp / "data/data_center/views/pair_market_snapshot/latest.json"
        self.assertTrue(view_path.exists(), f"View latest not written: {view_path}")

    def test_writes_consumer_view_by_symbol(self):
        write_spot_snapshot_to_data_center(_PAYLOAD, root=self.tmp, update_registry=False)
        by_symbol_path = self.tmp / "data/data_center/views/pair_market_snapshot/by_symbol/BTCUSDT.json"
        self.assertTrue(by_symbol_path.exists(), f"by_symbol not written: {by_symbol_path}")

    def test_returns_dict_with_paths(self):
        result = write_spot_snapshot_to_data_center(_PAYLOAD, root=self.tmp, update_registry=False)
        self.assertIn("producer_latest", result)
        self.assertIn("view_latest", result)
        self.assertIn("by_symbol", result)

    def test_runtime_registry_updated_when_enabled(self):
        write_spot_snapshot_to_data_center(_PAYLOAD, root=self.tmp, update_registry=True)
        registry_path = self.tmp / "data/data_center/_registry/producers.json"
        self.assertTrue(registry_path.exists(), "Runtime registry not created")
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        producers = data.get("producers", {})
        self.assertIn("collector_binance_spot", producers)
        self.assertIsNotNone(producers["collector_binance_spot"]["last_write"])

    def test_runtime_registry_skipped_when_disabled(self):
        write_spot_snapshot_to_data_center(_PAYLOAD, root=self.tmp, update_registry=False)
        registry_path = self.tmp / "data/data_center/_registry/producers.json"
        self.assertFalse(registry_path.exists(), "Registry should not be written when update_registry=False")

    def test_static_registry_not_mutated(self):
        static_path = Path("modules/data_center/registry/producers.json")
        if static_path.exists():
            original = static_path.read_text(encoding="utf-8")
        write_spot_snapshot_to_data_center(_PAYLOAD, root=self.tmp, update_registry=True)
        if static_path.exists():
            self.assertEqual(original, static_path.read_text(encoding="utf-8"))

    def test_raises_on_wrong_entity_type(self):
        bad_payload = dict(_PAYLOAD, entity_type="other")
        with self.assertRaises(ValueError):
            write_spot_snapshot_to_data_center(bad_payload, root=self.tmp)

    def test_two_records_written_to_by_symbol(self):
        payload_two = dict(_PAYLOAD, records=[
            *_PAYLOAD["records"],
            {**_PAYLOAD["records"][0], "pair_symbol": "ETHUSDT", "base_asset": "ETH",
             "source": {"provider_symbol": "ETHUSDT"}},
        ])
        result = write_spot_snapshot_to_data_center(payload_two, root=self.tmp, update_registry=False)
        self.assertEqual(len(result["by_symbol"]), 2)
        btc_path = self.tmp / "data/data_center/views/pair_market_snapshot/by_symbol/BTCUSDT.json"
        eth_path = self.tmp / "data/data_center/views/pair_market_snapshot/by_symbol/ETHUSDT.json"
        self.assertTrue(btc_path.exists())
        self.assertTrue(eth_path.exists())


if __name__ == "__main__":
    unittest.main()
