import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.derivatives_collector.app.bitget_adapter import BitgetAdapter


class TestBitgetLSRPatch(unittest.TestCase):
    def setUp(self):
        self.adapter = BitgetAdapter()
        self.sleep_patcher = patch("time.sleep", return_value=None)
        self.sleep_patcher.start()

    def tearDown(self):
        self.sleep_patcher.stop()

    def _mock_all(self, lsr_data=None, oi_data=None, ticker_data=None, fr_data=None):
        def side_effect(url, **kwargs):
            if "open-interest" in url:
                return oi_data or {"data": {"openInterest": "18234.56"}}
            if "ticker" in url:
                return ticker_data or {"data": [{"quoteVolume": "67890123.45"}]}
            if "fundRate" in url:
                return fr_data or {"data": {"fundingRate": "0.0001"}}
            if "account-long-short-ratio" in url:
                return lsr_data
            return None

        return side_effect

    @patch.object(BitgetAdapter, "_fetch")
    def test_lsr_populated_from_ratio(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(
            lsr_data={"data": [{"longRatio": "0.58", "shortRatio": "0.42"}]}
        )
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertIsNotNone(row["long_short_ratio"])
        self.assertAlmostEqual(row["long_short_ratio"], round(0.58 / 0.42, 4), places=4)

    @patch.object(BitgetAdapter, "_fetch")
    def test_lsr_none_when_endpoint_returns_none(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(lsr_data=None)
        data = self.adapter.collect(["BTCUSDT"])
        self.assertIsNone(data[0]["long_short_ratio"])

    @patch.object(BitgetAdapter, "_fetch")
    def test_lsr_none_when_data_empty_list(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(lsr_data={"data": []})
        data = self.adapter.collect(["BTCUSDT"])
        self.assertIsNone(data[0]["long_short_ratio"])

    @patch.object(BitgetAdapter, "_fetch")
    def test_lsr_none_when_short_ratio_zero(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(
            lsr_data={"data": [{"longRatio": "0.58", "shortRatio": "0.0"}]}
        )
        data = self.adapter.collect(["BTCUSDT"])
        self.assertIsNone(data[0]["long_short_ratio"])

    @patch.object(BitgetAdapter, "_fetch")
    def test_lsr_none_when_fields_missing(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(
            lsr_data={"data": [{"ts": "1716163200000"}]}
        )
        data = self.adapter.collect(["BTCUSDT"])
        self.assertIsNone(data[0]["long_short_ratio"])

    @patch.object(BitgetAdapter, "_fetch")
    def test_lsr_none_when_fields_non_numeric(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(
            lsr_data={"data": [{"longRatio": "n/a", "shortRatio": "n/a"}]}
        )
        data = self.adapter.collect(["BTCUSDT"])
        self.assertIsNone(data[0]["long_short_ratio"])

    @patch.object(BitgetAdapter, "_fetch")
    def test_existing_metrics_unaffected(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(
            lsr_data={"data": [{"longRatio": "0.60", "shortRatio": "0.40"}]}
        )
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertEqual(row["open_interest"], 18234.56)
        self.assertEqual(row["volume_futures"], 67890123.45)
        self.assertAlmostEqual(row["funding_rate"], 0.0001, places=6)

    @patch.object(BitgetAdapter, "_fetch")
    def test_liquidations_remain_none(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(
            lsr_data={"data": [{"longRatio": "0.60", "shortRatio": "0.40"}]}
        )
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertIsNone(row["liquidations_long"])
        self.assertIsNone(row["liquidations_short"])

    @patch.object(BitgetAdapter, "_fetch")
    def test_lsr_url_contains_correct_params(self, mock_fetch):
        called_urls = []

        def capture_urls(url, **kwargs):
            called_urls.append(url)
            if "open-interest" in url:
                return {"data": {"openInterest": "1000"}}
            if "ticker" in url:
                return {"data": [{"quoteVolume": "1000"}]}
            if "fundRate" in url:
                return {"data": {"fundingRate": "0.0001"}}
            if "account-long-short-ratio" in url:
                return {"data": [{"longRatio": "0.6", "shortRatio": "0.4"}]}
            return None

        mock_fetch.side_effect = capture_urls
        self.adapter.collect(["BTCUSDT"])
        lsr_urls = [u for u in called_urls if "account-long-short-ratio" in u]
        self.assertEqual(len(lsr_urls), 1)
        self.assertIn("BTCUSDT", lsr_urls[0])
        self.assertIn("USDT-FUTURES", lsr_urls[0])


if __name__ == "__main__":
    unittest.main()
