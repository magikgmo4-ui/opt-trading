import json
import time
import urllib.parse
import os
import urllib.request
from dataclasses import dataclass
from typing import List, Dict, Any

BASE = "https://api.bitget.com"

@dataclass
class Candle:
    ts_ms: int
    o: float
    h: float
    l: float
    c: float
    vol: float
    quote: float

def _get(path: str, params: Dict[str, str] | None = None) -> Dict[str, Any]:
    qs = ""
    if params:
        qs = "?" + urllib.parse.urlencode(params)
    url = BASE + path + qs
    print("BITGET_FEED url=", url, "BASE=", BASE, flush=True)
    print("BITGET_FEED url=", url, "BASE=", BASE, flush=True)
    req = urllib.request.Request(url, headers={"User-Agent":"tv-perf-bitget/1.0"})
    with urllib.request.urlopen(req, timeout=int(os.environ.get('BITGET_TIMEOUT','8'))) as r:
    print("BITGET_FEED proxies env=", {k:v for k,v in os.environ.items() if "proxy" in k.lower()}, flush=True)
    print("BITGET_FEED proxies env=", {k:v for k,v in os.environ.items() if "proxy" in k.lower()}, flush=True)
        return json.loads(r.read().decode("utf-8"))

def fetch_candles_usdt_futures(symbol: str, granularity_sec: int, limit: int = 200) -> List[Candle]:
    params = {
        "symbol": symbol,
        "productType": "USDT-FUTURES",
        "granularity": str(granularity_sec),
        "limit": str(limit),
    }
    d = _get("/api/v2/mix/market/candles", params)
    if d.get("code") != "00000":
        raise RuntimeError(f"Bitget error: {d}")
    rows = d.get("data") or []
    out: List[Candle] = []
    for r in rows:
        # ["ts","open","high","low","close","baseVol","quoteVol"]
        out.append(Candle(
            ts_ms=int(r[0]),
            o=float(r[1]),
            h=float(r[2]),
            l=float(r[3]),
            c=float(r[4]),
            vol=float(r[5]),
            quote=float(r[6]),
        ))
    # Bitget renvoie souvent du plus vieux -> plus récent (à vérifier), on trie au cas où
    out.sort(key=lambda x: x.ts_ms)
    return out

def demo():
    cs = fetch_candles_usdt_futures("BTCUSDT", 300, limit=5)
    for c in cs:
        print(c)

if __name__ == "__main__":
    demo()
