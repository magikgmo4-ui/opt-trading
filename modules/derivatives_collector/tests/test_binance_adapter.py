import sys
import os
import json
import time
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.derivatives_collector.app.binance_adapter import BinanceAdapter

class TestBinanceAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = BinanceAdapter()
        # Mock time.sleep to avoid hanging in tests
        self.sleep_patcher = patch('time.sleep', return_value=None)
        self.mock_sleep = self.sleep_patcher.start()

    def tearDown(self):
        self.sleep_patcher.stop()

    def _mock_response(self, data):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(data).encode('utf-8')
        mock_resp.__enter__.return_value = mock_resp
        return mock_resp

    @patch('urllib.request.urlopen')
    def test_fetch_success(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"success": True})
        res = self.adapter._fetch("http://test.com")
        self.assertEqual(res, {"success": True})
        self.assertEqual(mock_urlopen.call_count, 1)

    @patch('urllib.request.urlopen')
    def test_fetch_429_rate_limit(self, mock_urlopen):
        err_429 = HTTPError("url", 429, "Too Many Requests", {}, None)
        mock_urlopen.side_effect = [err_429, err_429, self._mock_response({"success": True})]
        res = self.adapter._fetch("http://test.com", retries=3, backoff_factor=0.1)
        self.assertEqual(res, {"success": True})
        self.assertEqual(mock_urlopen.call_count, 3)
        self.assertTrue(self.mock_sleep.called)

    @patch('urllib.request.urlopen')
    def test_fetch_418_auto_ban(self, mock_urlopen):
        err_418 = HTTPError("url", 418, "I'm a teapot (IP Banned)", {}, None)
        mock_urlopen.side_effect = err_418
        res = self.adapter._fetch("http://test.com")
        self.assertIsNone(res)
        # Should abort immediately without retrying
        self.assertEqual(mock_urlopen.call_count, 1)

    @patch('urllib.request.urlopen')
    def test_fetch_timeout(self, mock_urlopen):
        err_timeout = URLError("timeout")
        mock_urlopen.side_effect = err_timeout
        res = self.adapter._fetch("http://test.com", retries=2)
        self.assertIsNone(res)
        self.assertEqual(mock_urlopen.call_count, 2)

    @patch.object(BinanceAdapter, '_fetch')
    def test_collect_partial_degradation(self, mock_fetch):
        def mock_fetch_side_effect(url, **kwargs):
            if "openInterest" in url:
                return {"openInterest": "1000"}
            elif "premiumIndex" in url:
                return None  # Simulate endpoint failure
            elif "ticker/24hr" in url:
                return {"quoteVolume": "5000"}
            elif "globalLongShortAccountRatio" in url:
                return [{"longShortRatio": "2.0"}]
            return None

        mock_fetch.side_effect = mock_fetch_side_effect
        data = self.adapter.collect(["BTCUSDT"])
        
        self.assertEqual(len(data), 1)
        row = data[0]
        self.assertEqual(row["symbol"], "BTCUSDT")
        self.assertEqual(row["open_interest"], 1000.0)
        self.assertIsNone(row["funding_rate"])  # Expected to be None due to failure
        self.assertEqual(row["volume_futures"], 5000.0)
        self.assertEqual(row["long_short_ratio"], 2.0)
        # Verify output contract
        self.assertIn("liquidations_long", row)
        self.assertIn("liquidations_short", row)

    @patch.object(BinanceAdapter, '_collect_symbol')
    def test_collect_order_stability(self, mock_collect_symbol):
        symbols = ["A", "B", "C", "D"]
        
        def mock_symbol_fetch(sym, ts):
            return {"symbol": sym}
            
        mock_collect_symbol.side_effect = mock_symbol_fetch
        data = self.adapter.collect(symbols)
        
        output_symbols = [r["symbol"] for r in data]
        self.assertEqual(output_symbols, symbols)

if __name__ == '__main__':
    unittest.main()
