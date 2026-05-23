import sys
import logging
from .derivatives_collector import BaseAdapter, DerivativesRow
import time
import json
import urllib.request
import urllib.error
import concurrent.futures
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class BitgetAdapter(BaseAdapter):
    def __init__(self, max_workers=5, retries=3, backoff_factor=1.0):
        super().__init__("BITGET", max_workers=max_workers, retries=retries, backoff_factor=backoff_factor)

    """Bitget USDT-M Futures Data Adapter"""
    BASE_URL = "https://api.bitget.com"

    def _collect_symbol(self, symbol, batch_timestamp):
        bitget_symbol = symbol.upper()
        row = DerivativesRow(
            symbol=bitget_symbol,
            exchange="BITGET",
            timestamp=batch_timestamp
        )

        # Fetch Open Interest
        oi_url = f"{self.BASE_URL}/api/v2/mix/market/open-interest?symbol={bitget_symbol}&productType=USDT-FUTURES"
        oi_resp = self._fetch(oi_url)
        if oi_resp and oi_resp.get("data"):
            try:
                row.open_interest = float(oi_resp["data"].get("openInterest", 0.0))
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
                    row.volume_futures = float(vol)
            except (ValueError, TypeError, KeyError):
                pass

        # Fetch Funding Rate (V1 format often has UMCBL suffix)
        fr_url = f"{self.BASE_URL}/api/mix/v1/market/current-fundRate?symbol={bitget_symbol}_UMCBL"
        fr_resp = self._fetch(fr_url)
        if fr_resp and fr_resp.get("data"):
            try:
                row.funding_rate = float(fr_resp["data"].get("fundingRate", 0.0))
            except (ValueError, TypeError, KeyError):
                pass

        # Fetch Long/Short Ratio
        lsr_url = (
            f"{self.BASE_URL}/api/v2/mix/market/account-long-short-ratio"
            f"?symbol={bitget_symbol}&productType=USDT-FUTURES&period=1H"
        )
        lsr_resp = self._fetch(lsr_url)
        if lsr_resp and lsr_resp.get("data") and len(lsr_resp["data"]) > 0:
            try:
                lsr_data = lsr_resp["data"][0]
                long_r = float(lsr_data.get("longRatio", 0))
                short_r = float(lsr_data.get("shortRatio", 0))
                if short_r > 0:
                    row.long_short_ratio = round(long_r / short_r, 4)
            except (ValueError, TypeError, KeyError):
                pass

        # Fetch Liquidations (public forceOrders — side=sell → long liq, side=buy → short liq)
        liq_url = (
            f"{self.BASE_URL}/api/v2/mix/market/liquidation-order"
            f"?symbol={bitget_symbol}&productType=USDT-FUTURES&pageSize=100"
        )
        liq_resp = self._fetch(liq_url)
        if liq_resp and liq_resp.get("data") is not None:
            orders = liq_resp["data"].get("liquidationOrderList", [])
            if isinstance(orders, list):
                try:
                    liq_long = sum(
                        float(o.get("fillQty") or o.get("size", 0))
                        * float(o.get("fillPrice") or o.get("price", 0))
                        for o in orders if str(o.get("side", "")).lower() == "sell"
                    )
                    liq_short = sum(
                        float(o.get("fillQty") or o.get("size", 0))
                        * float(o.get("fillPrice") or o.get("price", 0))
                        for o in orders if str(o.get("side", "")).lower() == "buy"
                    )
                    row.liquidations_long = round(liq_long, 2)
                    row.liquidations_short = round(liq_short, 2)
                except (ValueError, TypeError, KeyError):
                    pass

        return row
