import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.derivatives_collector.app.binance_adapter import BinanceAdapter


def _order(side, qty, avg_price):
    return {"side": side, "executedQty": str(qty), "averagePrice": str(avg_price), "status": "FILLED"}


_OI_RESP = {"openInterest": "72145.89"}
_FR_RESP = {"lastFundingRate": "0.000125"}
_VOL_RESP = {"quoteVolume": "4890123456.78"}
_LSR_RESP = [{"longShortRatio": "1.8234"}]


class TestBinanceLiquidationsPatch(unittest.TestCase):
    def setUp(self):
        self.adapter = BinanceAdapter()
        self.sleep_patcher = patch("time.sleep", return_value=None)
        self.sleep_patcher.start()

    def tearDown(self):
        self.sleep_patcher.stop()

    def _mock_all(self, liq_data=None):
        def side_effect(url, **kwargs):
            if "openInterest" in url:
                return _OI_RESP
            if "premiumIndex" in url:
                return _FR_RESP
            if "ticker/24hr" in url:
                return _VOL_RESP
            if "globalLongShortAccountRatio" in url:
                return _LSR_RESP
            if "forceOrders" in url:
                return liq_data
            return None

        return side_effect

    @patch.object(BinanceAdapter, "_fetch")
    def test_liquidations_populated_from_orders(self, mock_fetch):
        orders = [
            _order("SELL", 0.5, 60000),   # long liq = 30000
            _order("SELL", 0.3, 60000),   # long liq += 18000
            _order("BUY", 0.2, 60000),    # short liq = 12000
        ]
        mock_fetch.side_effect = self._mock_all(liq_data=orders)
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertAlmostEqual(row["liquidations_long"], 48000.0, places=1)
        self.assertAlmostEqual(row["liquidations_short"], 12000.0, places=1)

    @patch.object(BinanceAdapter, "_fetch")
    def test_empty_orders_gives_zero(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(liq_data=[])
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertEqual(row["liquidations_long"], 0.0)
        self.assertEqual(row["liquidations_short"], 0.0)

    @patch.object(BinanceAdapter, "_fetch")
    def test_endpoint_none_keeps_null(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(liq_data=None)
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertIsNone(row["liquidations_long"])
        self.assertIsNone(row["liquidations_short"])

    @patch.object(BinanceAdapter, "_fetch")
    def test_sell_only_short_is_zero(self, mock_fetch):
        orders = [_order("SELL", 1.0, 50000)]
        mock_fetch.side_effect = self._mock_all(liq_data=orders)
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertAlmostEqual(row["liquidations_long"], 50000.0, places=1)
        self.assertEqual(row["liquidations_short"], 0.0)

    @patch.object(BinanceAdapter, "_fetch")
    def test_buy_only_long_is_zero(self, mock_fetch):
        orders = [_order("BUY", 1.0, 50000)]
        mock_fetch.side_effect = self._mock_all(liq_data=orders)
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertEqual(row["liquidations_long"], 0.0)
        self.assertAlmostEqual(row["liquidations_short"], 50000.0, places=1)

    @patch.object(BinanceAdapter, "_fetch")
    def test_malformed_order_graceful(self, mock_fetch):
        orders = [{"side": "SELL"}, {"side": "BUY", "executedQty": "bad", "averagePrice": "bad"}]
        mock_fetch.side_effect = self._mock_all(liq_data=orders)
        # should not raise, liquidations remain None on parse error
        data = self.adapter.collect(["BTCUSDT"])
        self.assertIsNotNone(data[0])

    @patch.object(BinanceAdapter, "_fetch")
    def test_existing_metrics_unaffected(self, mock_fetch):
        orders = [_order("SELL", 0.1, 60000)]
        mock_fetch.side_effect = self._mock_all(liq_data=orders)
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertEqual(row["open_interest"], 72145.89)
        self.assertAlmostEqual(row["funding_rate"], 0.000125, places=8)
        self.assertEqual(row["volume_futures"], 4890123456.78)
        self.assertAlmostEqual(row["long_short_ratio"], 1.8234, places=4)

    @patch.object(BinanceAdapter, "_fetch")
    def test_url_contains_symbol_and_limit(self, mock_fetch):
        called_urls = []

        def capture(url, **kwargs):
            called_urls.append(url)
            if "openInterest" in url:
                return _OI_RESP
            if "premiumIndex" in url:
                return _FR_RESP
            if "ticker/24hr" in url:
                return _VOL_RESP
            if "globalLongShortAccountRatio" in url:
                return _LSR_RESP
            if "forceOrders" in url:
                return []
            return None

        mock_fetch.side_effect = capture
        self.adapter.collect(["BTCUSDT"])
        liq_urls = [u for u in called_urls if "forceOrders" in u]
        self.assertEqual(len(liq_urls), 1)
        self.assertIn("BTCUSDT", liq_urls[0])
        self.assertIn("limit=100", liq_urls[0])

    @patch.object(BinanceAdapter, "_fetch")
    def test_rounding_to_two_decimals(self, mock_fetch):
        orders = [_order("SELL", 0.001, 60000.123)]
        mock_fetch.side_effect = self._mock_all(liq_data=orders)
        data = self.adapter.collect(["BTCUSDT"])
        val = data[0]["liquidations_long"]
        self.assertIsNotNone(val)
        # 0.001 * 60000.123 = 60.000123 → rounded to 60.0
        self.assertEqual(val, round(0.001 * 60000.123, 2))


if __name__ == "__main__":
    unittest.main()
