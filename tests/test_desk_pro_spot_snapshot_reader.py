import json
import shutil
import tempfile
import unittest
from pathlib import Path

from modules.desk_pro.service.spot_snapshot_reader import read_spot_snapshot

_PAYLOAD = {
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
            "last_price": "67800.00",
            "trading_status": "TRADING",
        }
    ],
}


class TestSpotSnapshotReader(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _write_fixture(self, payload=None):
        p = self.tmp / "latest.json"
        p.write_text(json.dumps(payload or _PAYLOAD), encoding="utf-8")
        return p

    def test_reads_valid_payload(self):
        path = self._write_fixture()
        result = read_spot_snapshot(path=path)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_has_correct_entity_type(self):
        path = self._write_fixture()
        result = read_spot_snapshot(path=path)
        self.assertEqual(result["entity_type"], "pair_market_snapshot")

    def test_has_records(self):
        path = self._write_fixture()
        result = read_spot_snapshot(path=path)
        self.assertGreater(len(result["records"]), 0)

    def test_returns_none_if_file_absent(self):
        result = read_spot_snapshot(path=self.tmp / "nonexistent.json")
        self.assertIsNone(result)

    def test_returns_none_if_wrong_entity_type(self):
        path = self._write_fixture({"entity_type": "other", "data": 1})
        result = read_spot_snapshot(path=path)
        self.assertIsNone(result)

    def test_returns_none_if_malformed_json(self):
        path = self.tmp / "bad.json"
        path.write_text("not json {{{{", encoding="utf-8")
        result = read_spot_snapshot(path=path)
        self.assertIsNone(result)

    def test_returns_none_if_not_dict(self):
        path = self._write_fixture([1, 2, 3])
        result = read_spot_snapshot(path=path)
        self.assertIsNone(result)

    def test_never_raises(self):
        for payload in [None, "bad", 42, {}, {"entity_type": "pair_market_snapshot"}]:
            try:
                if payload is None:
                    read_spot_snapshot(path=self.tmp / "nonexistent.json")
                else:
                    path = self.tmp / "p.json"
                    path.write_text(json.dumps(payload), encoding="utf-8")
                    read_spot_snapshot(path=path)
            except Exception as exc:
                self.fail(f"read_spot_snapshot raised unexpectedly: {exc}")


if __name__ == "__main__":
    unittest.main()
