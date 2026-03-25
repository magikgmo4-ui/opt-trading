import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

class BinanceAdapter:
    """Binance USD-M Futures Data Adapter"""
    BASE_URL = "https://fapi.binance.com"

    def _fetch(self, url):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(f"[BINANCE] Error fetching {url}: {e}", file=sys.stderr)
            return None

    def collect(self, symbols):
        data = []
        batch_timestamp = datetime.now(timezone.utc).isoformat()
        for symbol in symbols:
            base_symbol = symbol.upper()
            row = {
                "symbol": base_symbol,
                "exchange": "BINANCE",
                "timestamp": batch_timestamp,
                "open_interest": None,
                "funding_rate": None,
                "long_short_ratio": None,
                "liquidations_long": None,
                "liquidations_short": None,
                "volume_futures": None
            }

            # 2. Fetch Open Interest
            oi_resp = self._fetch(f"{self.BASE_URL}/fapi/v1/openInterest?symbol={base_symbol}")
            if oi_resp and "openInterest" in oi_resp:
                try:
                    row["open_interest"] = float(oi_resp["openInterest"])
                except (ValueError, TypeError):
                    pass

            # 3. Fetch Funding Rate
            fr_resp = self._fetch(f"{self.BASE_URL}/fapi/v1/premiumIndex?symbol={base_symbol}")
            if fr_resp and "lastFundingRate" in fr_resp:
                try:
                    row["funding_rate"] = float(fr_resp["lastFundingRate"])
                except (ValueError, TypeError):
                    pass

            # 4. Fetch Volume Futures
            vol_resp = self._fetch(f"{self.BASE_URL}/fapi/v1/ticker/24hr?symbol={base_symbol}")
            if vol_resp and "quoteVolume" in vol_resp:
                try:
                    row["volume_futures"] = float(vol_resp["quoteVolume"])
                except (ValueError, TypeError):
                    pass

            data.append(row)
        return data
