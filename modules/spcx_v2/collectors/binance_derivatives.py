"""
Binance Derivatives Proxy Collector
GO_SPACEX_MACRO_SENTIMENT_AND_DERIVATIVES_DATA_01

Collects BTC/ETH funding rate, open interest, long/short ratio from Binance Futures.
Used as risk-on/risk-off proxy for SPCX.
"""
from __future__ import annotations
import json, urllib.request
from typing import Any
from datetime import datetime, timezone


BINANCE_FUTURES = "https://fapi.binance.com"
BINANCE_SPOT = "https://api.binance.com"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]


def _fetch(url: str, timeout: int = 10) -> dict | list:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def collect_derivatives_proxy(symbols: list[str] | None = None) -> dict[str, Any]:
    symbols = symbols or SYMBOLS
    result = {
        "source": "risk_proxy_crypto_derivatives",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "note": "RISK PROXY ONLY — not SPCX direct data, max weight 0.05 in trade_ready",
        "funding": {},
        "open_interest": {},
        "long_short_ratio": {},
        "mark_prices": {},
        "error": None,
    }
    try:
        for sym in symbols:
            try:
                # Funding rate
                premium = _fetch(f"{BINANCE_FUTURES}/fapi/v1/premiumIndex?symbol={sym}")
                result["funding"][sym] = {
                    "funding_rate": float(premium.get("lastFundingRate", 0)),
                    "mark_price": float(premium.get("markPrice", 0)),
                    "index_price": float(premium.get("indexPrice", 0)),
                    "next_funding_time": premium.get("nextFundingTime"),
                }
                result["mark_prices"][sym] = float(premium.get("markPrice", 0))

                # Open Interest
                oi = _fetch(f"{BINANCE_FUTURES}/fapi/v1/openInterest?symbol={sym}")
                result["open_interest"][sym] = {
                    "open_interest": float(oi.get("openInterest", 0)),
                    "timestamp": oi.get("time"),
                }

                # Long/Short Ratio (global)
                ls = _fetch(f"{BINANCE_FUTURES}/futures/data/globalLongShortAccountRatio?symbol={sym}&period=5m&limit=1")
                if isinstance(ls, list) and ls:
                    result["long_short_ratio"][sym] = {
                        "long_account": float(ls[0].get("longAccount", 0)),
                        "short_account": float(ls[0].get("shortAccount", 0)),
                        "long_short_ratio": float(ls[0].get("longShortRatio", 0)),
                        "timestamp": ls[0].get("timestamp"),
                    }
            except Exception as e:
                result["funding"][sym] = {"error": str(e)[:100]}

        result["ok"] = bool(result["funding"])
    except Exception as e:
        result["error"] = str(e)[:200]

    return result


def compute_derivatives_risk_score(proxy: dict) -> dict[str, Any]:
    """Convert raw derivatives data into risk-on/risk-off scores."""
    scores = {
        "funding_pressure": 0.5,
        "oi_pressure": 0.5,
        "crowding_risk": 0.5,
        "overall_risk": "neutral",
    }

    funding = proxy.get("funding", {})
    oi = proxy.get("open_interest", {})
    ls = proxy.get("long_short_ratio", {})

    # Funding: very positive = overheating, very negative = bearish
    btc_funding = funding.get("BTCUSDT", {}).get("funding_rate", 0)
    if btc_funding > 0.0005:  # 0.05%+
        scores["funding_pressure"] = 0.8
    elif btc_funding > 0.0001:
        scores["funding_pressure"] = 0.6
    elif btc_funding < -0.0005:
        scores["funding_pressure"] = 0.2
    elif btc_funding < -0.0001:
        scores["funding_pressure"] = 0.35

    # Long/Short crowding
    btc_ls = ls.get("BTCUSDT", {}).get("long_short_ratio", 1.0)
    if btc_ls > 3.0:
        scores["crowding_risk"] = 0.85  # extreme long crowding
    elif btc_ls > 2.0:
        scores["crowding_risk"] = 0.65
    elif btc_ls < 0.7:
        scores["crowding_risk"] = 0.3
    elif btc_ls < 1.0:
        scores["crowding_risk"] = 0.45

    # Overall
    avg = (scores["funding_pressure"] + scores["oi_pressure"] + scores["crowding_risk"]) / 3
    if avg > 0.65:
        scores["overall_risk"] = "risk_on"
    elif avg < 0.35:
        scores["overall_risk"] = "risk_off"
    else:
        scores["overall_risk"] = "neutral"

    return scores
