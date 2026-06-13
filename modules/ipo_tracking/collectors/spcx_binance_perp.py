"""
SPCX Binance Perpetual Collector
Collects SPCXUSDT perpetual data: OHLCV, funding, OI, order book, L/S ratio.
This is a DIRECT SPCX derivative (not a risk proxy).
"""
from __future__ import annotations
import json, urllib.request
from datetime import datetime, timezone
from typing import Any

BINANCE_FAPI = "https://fapi.binance.com"
SYMBOL = "SPCXUSDT"


def _fetch(url: str, timeout: int = 8) -> Any:
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 opt-trading spcx"
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def collect_spcx_perp() -> dict[str, Any]:
    """Collect full SPCXUSDT perpetual data."""
    result = {
        "source": "spcx_binance_perpetual",
        "symbol": SYMBOL,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "price": None,
        "mark_price": None,
        "index_price": None,
        "funding_rate": None,
        "next_funding_time": None,
        "open_interest": None,
        "volume_24h": None,
        "high_24h": None,
        "low_24h": None,
        "change_pct_24h": None,
        "bid": None,
        "ask": None,
        "spread_pct": None,
        "bars_1m": [],
        "error": None,
    }

    try:
        # Ticker 24h
        ticker = _fetch(f"{BINANCE_FAPI}/fapi/v1/ticker/24hr?symbol={SYMBOL}")
        result["ok"] = True
        result["price"] = float(ticker["lastPrice"])
        result["volume_24h"] = float(ticker["volume"])
        result["high_24h"] = float(ticker["highPrice"])
        result["low_24h"] = float(ticker["lowPrice"])
        result["change_pct_24h"] = float(ticker["priceChangePercent"])
    except Exception as e:
        result["error"] = f"ticker: {e}"
        return result

    try:
        # Premium index
        prem = _fetch(f"{BINANCE_FAPI}/fapi/v1/premiumIndex?symbol={SYMBOL}")
        result["mark_price"] = float(prem["markPrice"])
        result["index_price"] = float(prem["indexPrice"])
        result["funding_rate"] = float(prem["lastFundingRate"])
        result["next_funding_time"] = prem["nextFundingTime"]
    except Exception:
        pass

    try:
        # Open Interest
        oi = _fetch(f"{BINANCE_FAPI}/fapi/v1/openInterest?symbol={SYMBOL}")
        result["open_interest"] = float(oi["openInterest"])
    except Exception:
        pass

    try:
        # Order book
        book = _fetch(f"{BINANCE_FAPI}/fapi/v1/depth?symbol={SYMBOL}&limit=5")
        bids = book.get("bids", [])
        asks = book.get("asks", [])
        if bids and asks:
            result["bid"] = float(bids[0][0])
            result["ask"] = float(asks[0][0])
            if result["bid"] > 0:
                result["spread_pct"] = round((result["ask"] - result["bid"]) / result["bid"] * 100, 4)
    except Exception:
        pass

    try:
        # Recent 1m bars
        klines = _fetch(f"{BINANCE_FAPI}/fapi/v1/klines?symbol={SYMBOL}&interval=1m&limit=60")
        for k in klines:
            result["bars_1m"].append({
                "ts": k[0],
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5]),
            })
    except Exception:
        pass

    return result


def collect_spcx_perp_historical(limit: int = 500) -> list[dict]:
    """Collect historical 1m bars for backtesting."""
    try:
        klines = _fetch(f"{BINANCE_FAPI}/fapi/v1/klines?symbol={SYMBOL}&interval=1m&limit={limit}", timeout=15)
        return [{
            "ts": k[0],
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
        } for k in klines]
    except Exception:
        return []
