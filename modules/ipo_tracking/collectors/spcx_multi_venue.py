"""
SPCX Multi-Venue Data Collectors
Bitget rSPCX + CoinGecko + Finnhub

All 3 are free public APIs, no auth required.
"""
from __future__ import annotations
import json, urllib.request
from datetime import datetime, timezone
from typing import Any


def collect_bitget_rspcx() -> dict[str, Any]:
    """Collect Bitget rSPCXUSDT tokenized stock data."""
    result = {
        "source": "bitget_rspcx",
        "symbol": "RSPCXUSDT",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "price": None, "open_24h": None, "high_24h": None, "low_24h": None,
        "volume_base": None, "volume_usdt": None, "ipo_price": None,
        "error": None,
    }
    try:
        req = urllib.request.Request(
            "https://api.bitget.com/api/v2/spot/market/tickers?symbol=RSPCXUSDT",
            headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 opt-trading"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        tickers = data.get("data", [])
        if tickers:
            t = tickers[0]
            result["ok"] = True
            result["price"] = float(t.get("lastPr", 0))
            result["open_24h"] = float(t.get("open", 0))
            result["high_24h"] = float(t.get("high24h", 0))
            result["low_24h"] = float(t.get("low24h", 0))
            result["volume_base"] = float(t.get("baseVolume", 0))
            result["volume_usdt"] = float(t.get("usdtVolume", 0))
            result["ipo_price"] = float(t["open"]) if float(t.get("open", 0)) == 135 else None
    except Exception as e:
        result["error"] = str(e)[:200]
    return result


def collect_coingecko_spcx() -> dict[str, Any]:
    """Collect CoinGecko market data for SPCX tokenized variants."""
    result = {
        "source": "coingecko_spcx",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "tokens": [],
        "error": None,
    }
    try:
        # Search for SPCX tokens
        req = urllib.request.Request(
            "https://api.coingecko.com/api/v3/search?query=SPCX",
            headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 opt-trading"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        coins = data.get("coins", [])[:5]
        result["ok"] = True
        for c in coins:
            result["tokens"].append({
                "id": c.get("id"),
                "name": c.get("name"),
                "symbol": c.get("symbol"),
                "market_cap_rank": c.get("market_cap_rank"),
            })

        # Get market data for the main SPCX token
        if coins:
            main_id = coins[0]["id"]
            req2 = urllib.request.Request(
                f"https://api.coingecko.com/api/v3/coins/{main_id}?localization=false&tickers=false&community_data=false&developer_data=false",
                headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 opt-trading"}
            )
            with urllib.request.urlopen(req2, timeout=8) as r2:
                detail = json.loads(r2.read().decode())
            m = detail.get("market_data", {})
            result["market_data"] = {
                "price_usd": m.get("current_price", {}).get("usd"),
                "market_cap_usd": m.get("market_cap", {}).get("usd"),
                "total_volume_usd": m.get("total_volume", {}).get("usd"),
                "high_24h_usd": m.get("high_24h", {}).get("usd"),
                "low_24h_usd": m.get("low_24h", {}).get("usd"),
                "price_change_pct_24h": m.get("price_change_percentage_24h"),
            }
    except Exception as e:
        result["error"] = str(e)[:200]
    return result


def collect_finnhub_spcx() -> dict[str, Any]:
    """Collect Finnhub SPCX quote (free tier, no key for demo)."""
    result = {
        "source": "finnhub_spcx",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "price": None, "change_pct": None, "high": None, "low": None,
        "open": None, "prev_close": None,
        "error": None,
    }
    try:
        # Finnhub free tier — works with token=demo for basic quote
        req = urllib.request.Request(
            "https://finnhub.io/api/v1/quote?symbol=SPCX&token=demo",
            headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 opt-trading"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        if data.get("c"):  # current price
            result["ok"] = True
            result["price"] = data.get("c")
            result["high"] = data.get("h")
            result["low"] = data.get("l")
            result["open"] = data.get("o")
            result["prev_close"] = data.get("pc")
            if result["prev_close"] and result["prev_close"] > 0:
                result["change_pct"] = round((result["price"] - result["prev_close"]) / result["prev_close"] * 100, 2)
    except Exception as e:
        result["error"] = str(e)[:200]
    return result


def collect_all_multi_venue() -> dict[str, Any]:
    """Collect all 3 multi-venue sources for SPCX."""
    return {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "bitget_rspcx": collect_bitget_rspcx(),
        "coingecko_spcx": collect_coingecko_spcx(),
        "finnhub_spcx": collect_finnhub_spcx(),
    }
