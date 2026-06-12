from __future__ import annotations
import json
import urllib.parse
import urllib.request
from typing import Any
from ..io import utc_now

def collect_yahoo_quote(symbol: str = "SPCX", *, range_: str = "1d", interval: str = "1m", timeout: int = 15) -> dict[str, Any]:
    safe = urllib.parse.quote(symbol)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{safe}?range={range_}&interval={interval}"
    out = {"source": "yahoo_chart", "symbol": symbol, "collected_at": utc_now(), "url": url, "ok": False, "bars": [], "error": None}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 opt-trading spacex_super_desk"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        result = (data.get("chart", {}).get("result") or [None])[0]
        if not result:
            raise RuntimeError("no chart result")
        meta = result.get("meta", {})
        ts = result.get("timestamp") or []
        quote = (result.get("indicators", {}).get("quote") or [{}])[0]
        bars = []
        for i, t in enumerate(ts):
            bars.append({"ts": t, "open": _idx(quote.get("open"), i), "high": _idx(quote.get("high"), i), "low": _idx(quote.get("low"), i), "close": _idx(quote.get("close"), i), "volume": _idx(quote.get("volume"), i)})
        out.update({"ok": True, "currency": meta.get("currency"), "exchange": meta.get("exchangeName"), "regular_market_price": meta.get("regularMarketPrice"), "previous_close": meta.get("chartPreviousClose"), "bars": bars[-390:]})
    except Exception as exc:
        out["error"] = str(exc)
    return out

def _idx(arr, i):
    try:
        return arr[i]
    except Exception:
        return None
