import sys
import time
import json
import urllib.request
import urllib.error
import concurrent.futures
from datetime import datetime, timezone

class BinanceAdapter:
    """Binance USD-M Futures Data Adapter"""
    BASE_URL = "https://fapi.binance.com"

    def _fetch(self, url, retries=3, backoff_factor=1.0):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    return json.loads(response.read().decode('utf-8'))
            except Exception as e:
                wait_time = backoff_factor * (2 ** attempt)
                error_msg = str(e)
                
                if isinstance(e, urllib.error.HTTPError):
                    if e.code == 429:
                        error_msg = "Rate limit exceeded (429)"
                        wait_time = max(wait_time, 2.0)
                    elif e.code == 418:
                        error_msg = "IP auto-banned (418)"
                        print(f"[BINANCE][FATAL] {error_msg} for {url}. Aborting.", file=sys.stderr)
                        return None
                    else:
                        error_msg = f"HTTP {e.code}"
                elif isinstance(e, urllib.error.URLError):
                    error_msg = f"Network/Timeout ({e.reason})"

                if attempt == retries - 1:
                    print(f"[BINANCE][ERROR] Final fetch failure for {url} after {retries} attempts: {error_msg}", file=sys.stderr)
                    return None
                    
                print(f"[BINANCE][WARN] Fetch failed for {url} (attempt {attempt+1}/{retries}): {error_msg}. Retrying in {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)

    def _collect_symbol(self, symbol, batch_timestamp):
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

        # 5. Fetch Long/Short Ratio
        lsr_resp = self._fetch(f"{self.BASE_URL}/futures/data/globalLongShortAccountRatio?symbol={base_symbol}&period=5m")
        if lsr_resp and isinstance(lsr_resp, list) and len(lsr_resp) > 0:
            try:
                row["long_short_ratio"] = float(lsr_resp[-1].get("longShortRatio", 0.0))
            except (ValueError, TypeError):
                pass

        missing_metrics = [k for k in ["open_interest", "funding_rate", "volume_futures", "long_short_ratio"] if row[k] is None]
        if missing_metrics:
            print(f"[BINANCE][WARN] Partial data degradation for {base_symbol}. Missing: {missing_metrics}", file=sys.stderr)

        return row

    def collect(self, symbols):
        data = []
        batch_timestamp = datetime.now(timezone.utc).isoformat()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = executor.map(lambda sym: self._collect_symbol(sym, batch_timestamp), symbols)
            for row in results:
                data.append(row)
                
        return data
