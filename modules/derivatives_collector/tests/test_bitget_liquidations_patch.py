import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.derivatives_collector.app.bitget_adapter import BitgetAdapter


def _order(side, qty, price, use_alt_fields=False):
    if use_alt_fields:
        return {"side": side, "size": str(qty), "price": str(price)}
    return {"side": side, "fillQty": str(qty), "fillPrice": str(price)}


_OI_RESP = {"data": {"openInterest": "18234.56"}}
_TICKER_RESP = {"data": [{"quoteVolume": "67890123.45"}]}
_FR_RESP = {"data": {"fundingRate": "0.0001"}}
_LSR_RESP = {"data": [{"longRatio": "0.58", "shortRatio": "0.42"}]}


class TestBitgetLiquidationsPatch(unittest.TestCase):
    def setUp(self):
        self.adapter = BitgetAdapter()
        self.sleep_patcher = patch("time.sleep", return_value=None)
        self.sleep_patcher.start()

    def tearDown(self):
        self.sleep_patcher.stop()

    def _mock_all(self, liq_data=None):
        def side_effect(url, **kwargs):
            if "open-interest" in url:
                return _OI_RESP
            if "ticker" in url:
                return _TICKER_RESP
            if "fundRate" in url:
                return _FR_RESP
            if "account-long-short-ratio" in url:
                return _LSR_RESP
            if "liquidation-order" in url:
                return liq_data
            return None

        return side_effect

    @patch.object(BitgetAdapter, "_fetch")
    def test_liquidations_populated_from_orders(self, mock_fetch):
        orders = [
            _order("sell", 0.5, 60000),
            _order("sell", 0.3, 60000),
            _order("buy", 0.2, 60000),
        ]
        mock_fetch.side_effect = self._mock_all(
            liq_data={"data": {"liquidationOrderList": orders}}
        )
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertAlmostEqual(row["liquidations_long"], 48000.0, places=1)
        self.assertAlmostEqual(row["liquidations_short"], 12000.0, places=1)

    @patch.object(BitgetAdapter, "_fetch")
    def test_empty_list_gives_zero(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(
            liq_data={"data": {"liquidationOrderList": []}}
        )
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertEqual(row["liquidations_long"], 0.0)
        self.assertEqual(row["liquidations_short"], 0.0)

    @patch.object(BitgetAdapter, "_fetch")
    def test_endpoint_none_keeps_null(self, mock_fetch):
        mock_fetch.side_effect = self._mock_all(liq_data=None)
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertIsNone(row["liquidations_long"])
        self.assertIsNone(row["liquidations_short"])

    @patch.object(BitgetAdapter, "_fetch")
    def test_alt_fields_size_price(self, mock_fetch):
        orders = [_order("sell", 1.0, 50000, use_alt_fields=True)]
        mock_fetch.side_effect = self._mock_all(
            liq_data={"data": {"liquidationOrderList": orders}}
        )
        data = self.adapter.collect(["BTCUSDT"])
        self.assertAlmostEqual(data[0]["liquidations_long"], 50000.0, places=1)

    @patch.object(BitgetAdapter, "_fetch")
    def test_side_case_insensitive(self, mock_fetch):
        orders = [
            {"side": "SELL", "fillQty": "1.0", "fillPrice": "50000"},
            {"side": "BUY", "fillQty": "0.5", "fillPrice": "50000"},
        ]
        mock_fetch.side_effect = self._mock_all(
            liq_data={"data": {"liquidationOrderList": orders}}
        )
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertAlmostEqual(row["liquidations_long"], 50000.0, places=1)
        self.assertAlmostEqual(row["liquidations_short"], 25000.0, places=1)

    @patch.object(BitgetAdapter, "_fetch")
    def test_sell_only_short_is_zero(self, mock_fetch):
        orders = [_order("sell", 1.0, 50000)]
        mock_fetch.side_effect = self._mock_all(
            liq_data={"data": {"liquidationOrderList": orders}}
        )
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertAlmostEqual(row["liquidations_long"], 50000.0, places=1)
        self.assertEqual(row["liquidations_short"], 0.0)

    @patch.object(BitgetAdapter, "_fetch")
    def test_buy_only_long_is_zero(self, mock_fetch):
        orders = [_order("buy", 0.5, 60000)]
        mock_fetch.side_effect = self._mock_all(
            liq_data={"data": {"liquidationOrderList": orders}}
        )
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertEqual(row["liquidations_long"], 0.0)
        self.assertAlmostEqual(row["liquidations_short"], 30000.0, places=1)

    @patch.object(BitgetAdapter, "_fetch")
    def test_existing_metrics_unaffected(self, mock_fetch):
        orders = [_order("sell", 0.1, 60000)]
        mock_fetch.side_effect = self._mock_all(
            liq_data={"data": {"liquidationOrderList": orders}}
        )
        data = self.adapter.collect(["BTCUSDT"])
        row = data[0]
        self.assertEqual(row["open_interest"], 18234.56)
        self.assertEqual(row["volume_futures"], 67890123.45)
        self.assertAlmostEqual(row["funding_rate"], 0.0001, places=6)
        self.assertIsNotNone(row["long_short_ratio"])

    @patch.object(BitgetAdapter, "_fetch")
    def test_url_contains_symbol_and_page_size(self, mock_fetch):
        called_urls = []

        def capture(url, **kwargs):
            called_urls.append(url)
            if "open-interest" in url:
                return _OI_RESP
            if "ticker" in url:
                return _TICKER_RESP
            if "fundRate" in url:
                return _FR_RESP
            if "account-long-short-ratio" in url:
                return _LSR_RESP
            if "liquidation-order" in url:
                return {"data": {"liquidationOrderList": []}}
            return None

        mock_fetch.side_effect = capture
        self.adapter.collect(["BTCUSDT"])
        liq_urls = [u for u in called_urls if "liquidation-order" in u]
        self.assertEqual(len(liq_urls), 1)
        self.assertIn("BTCUSDT", liq_urls[0])
        self.assertIn("pageSize=100", liq_urls[0])

    @patch.object(BitgetAdapter, "_fetch")
    def test_rounding_to_two_decimals(self, mock_fetch):
        orders = [_order("buy", 0.001, 60000.123)]
        mock_fetch.side_effect = self._mock_all(
            liq_data={"data": {"liquidationOrderList": orders}}
        )
        data = self.adapter.collect(["BTCUSDT"])
        val = data[0]["liquidations_short"]
        self.assertEqual(val, round(0.001 * 60000.123, 2))


if __name__ == "__main__":
    unittest.main()
