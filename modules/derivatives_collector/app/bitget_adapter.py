import sys
import time
import json
import urllib.request
import urllib.error
import concurrent.futures
from datetime import datetime, timezone

class BitgetAdapter:
    """Bitget USDT-M Futures Data Adapter"""
    BASE_URL = "https://api.bitget.com"

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
                        print(f"[BITGET][FATAL] {error_msg} for {url}. Aborting.", file=sys.stderr)
                        return None
                    else:
                        error_msg = f"HTTP {e.code}"
                elif isinstance(e, urllib.error.URLError):
                    error_msg = f"Network/Timeout ({e.reason})"

                if attempt == retries - 1:
                    print(f"[BITGET][ERROR] Final fetch failure for {url} after {retries} attempts: {error_msg}", file=sys.stderr)
                    return None
                    
                print(f"[BITGET][WARN] Fetch failed for {url} (attempt {attempt+1}/{retries}): {error_msg}. Retrying in {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)

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

    def collect(self, symbols):
        data = []
        batch_timestamp = datetime.now(timezone.utc).isoformat()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = executor.map(lambda sym: self._collect_symbol(sym, batch_timestamp), symbols)
            for row in results:
                data.append(row)
                
        return data
