import sys
from .derivatives_collector import BaseAdapter
import time
import json
import urllib.request
import urllib.error
import concurrent.futures
from datetime import datetime, timezone

class BitgetAdapter(BaseAdapter):
    """Bitget USDT-M Futures Data Adapter"""
    BASE_URL = "https://api.bitget.com"

    def _collect_symbol(self, symbol, batch_timestamp):
        bitget_symbol = symbol.upper()
        row = {
            "symbol": bitget_symbol,
            "exchange": "BITGET",
            "timestamp": batch_timestamp,
            "open_interest": None,
            "funding_rate": None,
            "long_short_ratio": None,
            "liquidations_long": None,
            "liquidations_short": None,
            "volume_futures": None
        }

        # Fetch Open Interest
        oi_url = f"{self.BASE_URL}/api/v2/mix/market/open-interest?symbol={bitget_symbol}&productType=USDT-FUTURES"
        oi_resp = self._fetch(oi_url)
        if oi_resp and oi_resp.get("data"):
            try:
                row["open_interest"] = float(oi_resp["data"].get("openInterest", 0.0))
            except (ValueError, TypeError, KeyError):
                pass

        # Fetch Ticker for Volume
        ticker_url = f"{self.BASE_URL}/api/v2/mix/market/ticker?symbol={bitget_symbol}&productType=USDT-FUTURES"
        ticker_resp = self._fetch(ticker_url)
        if ticker_resp and ticker_resp.get("data") and len(ticker_resp["data"]) > 0:
            try:
                ticker_data = ticker_resp["data"][0]
                vol = ticker_data.get("quoteVolume") or ticker_data.get("usdtVolume") or ticker_data.get("baseVolume")
                if vol is not None:
                    row["volume_futures"] = float(vol)
            except (ValueError, TypeError, KeyError):
                pass

        # Fetch Funding Rate (V1 format often has UMCBL suffix)
        fr_url = f"{self.BASE_URL}/api/mix/v1/market/current-fundRate?symbol={bitget_symbol}_UMCBL"
        fr_resp = self._fetch(fr_url)
        if fr_resp and fr_resp.get("data"):
            try:
                row["funding_rate"] = float(fr_resp["data"].get("fundingRate", 0.0))
            except (ValueError, TypeError, KeyError):
                pass

        return row
