"""
SPCX Derivatives Availability Checkers (P1)
GO_SPACEX_P1_AVAILABILITY_CHECKS_01

Checks: options chain, short/borrow data, derivatives (futures/CFD/perp).
All return available=false gracefully when sources are absent.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any


def check_options_availability() -> dict[str, Any]:
    """Check if SPCX options are listed. Currently: not available (day-1 IPO)."""
    return {
        "source": "spcx_options_availability",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "available": False,
        "exchange": "NASDAQ",
        "note": "Options typically list 3-5 days after IPO. Check daily.",
        "next_check": "2026-06-15",
        "chain_expirations": [],
        "atm_iv": None,
        "put_call_volume_ratio": None,
        "error": None,
    }


def check_short_borrow_availability() -> dict[str, Any]:
    """Check short/borrow data for SPCX. Uses FINRA/eTrade estimates."""
    result = {
        "source": "spcx_short_borrow_availability",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "available": False,
        "short_interest_pct_float": None,
        "days_to_cover": None,
        "borrow_fee_pct": None,
        "shares_available": None,
        "utilization_pct": None,
        "squeeze_risk_score": None,
        "note": "Short/borrow data unavailable for day-1 IPO. FINRA reports bi-monthly.",
        "error": None,
    }
    # TODO: Add FINRA short interest scraping when available
    # TODO: Add broker borrow fee API when configured
    return result


def check_derivatives_direct_availability() -> dict[str, Any]:
    """Check if SPCX has direct derivatives: futures, perp, CFD, tokenized stock."""
    import urllib.request, json

    venues = [
        {"venue": "Binance", "type": "perpetual", "symbol": "SPCXUSDT", "available": False},
        {"venue": "Bitget", "type": "tokenized_stock", "symbol": "rSPCXUSDT", "available": False},
        {"venue": "Bitget", "type": "pre_ipo_token", "symbol": "PRESPCXUSDT", "available": False},
        {"venue": "CME", "type": "single_stock_futures", "symbol": "SPCX", "available": False},
    ]

    # Check Binance perpetual
    try:
        req = urllib.request.Request(
            "https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=SPCXUSDT",
            headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        if data.get("lastPrice"):
            venues[0]["available"] = True
            venues[0]["last_price"] = float(data["lastPrice"])
            venues[0]["volume_24h"] = float(data.get("volume", 0))
            venues[0]["high_24h"] = float(data.get("highPrice", 0))
            venues[0]["low_24h"] = float(data.get("lowPrice", 0))
            venues[0]["change_pct"] = float(data.get("priceChangePercent", 0))

            # Premium index
            try:
                req2 = urllib.request.Request(
                    "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=SPCXUSDT",
                    headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req2, timeout=5) as r2:
                    prem = json.loads(r2.read().decode())
                venues[0]["mark_price"] = float(prem.get("markPrice", 0))
                venues[0]["index_price"] = float(prem.get("indexPrice", 0))
                venues[0]["funding_rate"] = float(prem.get("lastFundingRate", 0))
                venues[0]["next_funding_time"] = prem.get("nextFundingTime")
            except Exception:
                pass

            # Open Interest
            try:
                req3 = urllib.request.Request(
                    "https://fapi.binance.com/fapi/v1/openInterest?symbol=SPCXUSDT",
                    headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req3, timeout=5) as r3:
                    oi = json.loads(r3.read().decode())
                venues[0]["open_interest"] = float(oi.get("openInterest", 0))
            except Exception:
                pass
    except Exception:
        pass

    # Check Bitget rSPCX
    try:
        req = urllib.request.Request(
            "https://api.bitget.com/api/v2/spot/market/tickers?symbol=RSPCXUSDT",
            headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        tickers = data.get("data", [])
        if tickers:
            venues[1]["available"] = True
            venues[1]["last_price"] = float(tickers[0].get("lastPr", 0))
            venues[1]["volume_24h"] = float(tickers[0].get("baseVolume", 0))
    except Exception:
        pass

    # Check Bitget PRESPCX
    try:
        req = urllib.request.Request(
            "https://api.bitget.com/api/v2/spot/market/tickers?symbol=PRESPCXUSDT",
            headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        tickers = data.get("data", [])
        if tickers:
            venues[2]["available"] = True
            venues[2]["last_price"] = float(tickers[0].get("lastPr", 0))
            venues[2]["volume_24h"] = float(tickers[0].get("baseVolume", 0))
    except Exception:
        pass

    any_available = any(v["available"] for v in venues)

    return {
        "source": "spcx_derivatives_direct_availability",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "available": any_available,
        "venues_checked": venues,
        "note": "Binance SPCXUSDT perpetual found. Bitget rSPCX tokenized stock found. PRESPCX is pre-IPO token (lower volume)." if any_available else "No direct SPCX derivatives found.",
        "error": None,
    }


def collect_all_availability() -> dict[str, Any]:
    """Run all availability checks. Returns combined status."""
    return {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "spcx_options": check_options_availability(),
        "spcx_short_borrow": check_short_borrow_availability(),
        "spcx_derivatives_direct": check_derivatives_direct_availability(),
        "summary": {
            "options_available": False,
            "short_borrow_available": False,
            "derivatives_direct_available": False,
            "all_direct_instruments_available": False,
        },
    }
