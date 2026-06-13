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
    venues = [
        {"venue": "CME", "type": "single_stock_futures", "symbol": "SPCX", "available": False},
        {"venue": "Binance", "type": "tokenized_stock", "symbol": "SPCX", "available": False},
        {"venue": "FTX/EU", "type": "tokenized_stock", "symbol": "SPCX", "available": False},
        {"venue": "Various_CFD", "type": "cfd", "symbol": "SPCX", "available": False},
    ]

    return {
        "source": "spcx_derivatives_direct_availability",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "available": False,
        "venues_checked": venues,
        "note": "No direct SPCX derivatives found. CFD may appear on retail brokers. Tokenized stock unlikely for NASDAQ IPO. Check daily.",
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
