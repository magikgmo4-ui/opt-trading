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

class BinanceAdapter(BaseAdapter):
    def __init__(self, max_workers=5, retries=3, backoff_factor=1.0):
        super().__init__(max_workers=max_workers, retries=retries, backoff_factor=backoff_factor)

    """Binance USD-M Futures Data Adapter"""
    BASE_URL = "https://fapi.binance.com"

    def _collect_symbol(self, symbol, batch_timestamp):
        base_symbol = symbol.upper()
        row = DerivativesRow(
            symbol=base_symbol,
            exchange="BINANCE",
            timestamp=batch_timestamp
        )

        # 2. Fetch Open Interest
        oi_resp = self._fetch(f"{self.BASE_URL}/fapi/v1/openInterest?symbol={base_symbol}")
        if oi_resp and "openInterest" in oi_resp:
            try:
                row.open_interest = float(oi_resp["openInterest"])
            except (ValueError, TypeError):
                pass

        # 3. Fetch Funding Rate
        fr_resp = self._fetch(f"{self.BASE_URL}/fapi/v1/premiumIndex?symbol={base_symbol}")
        if fr_resp and "lastFundingRate" in fr_resp:
            try:
                row.funding_rate = float(fr_resp["lastFundingRate"])
            except (ValueError, TypeError):
                pass

        # 4. Fetch Volume Futures
        vol_resp = self._fetch(f"{self.BASE_URL}/fapi/v1/ticker/24hr?symbol={base_symbol}")
        if vol_resp and "quoteVolume" in vol_resp:
            try:
                row.volume_futures = float(vol_resp["quoteVolume"])
            except (ValueError, TypeError):
                pass

        # 5. Fetch Long/Short Ratio
        lsr_resp = self._fetch(f"{self.BASE_URL}/futures/data/globalLongShortAccountRatio?symbol={base_symbol}&period=5m")
        if lsr_resp and isinstance(lsr_resp, list) and len(lsr_resp) > 0:
            try:
                row.long_short_ratio = float(lsr_resp[-1].get("longShortRatio", 0.0))
            except (ValueError, TypeError):
                pass

        missing_metrics = [k for k in ["open_interest", "funding_rate", "volume_futures", "long_short_ratio"] if getattr(row, k) is None]
        if missing_metrics:
            logger.warning(f"Partial data degradation for {base_symbol}. Missing: {missing_metrics}")

        return row
