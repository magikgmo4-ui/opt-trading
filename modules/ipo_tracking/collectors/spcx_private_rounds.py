"""
SPCX Private Rounds / Pre-IPO Cost Basis Collector
GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01

Reconstructs pre-IPO cost basis from public information:
  - SEC S-1 / 424B4 prospectus (preferred stock conversion, fair value history)
  - Press reports and tender offer data
  - Private market aggregator data (Forge, EquityZen, Caplight, Hiive)

All cost_basis values are marked as `cost_basis_estimated: True` unless
explicitly confirmed in a filing.
"""
from __future__ import annotations
import json, urllib.request
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]

# SpaceX funding rounds — reconstructed from public sources
# Dates and valuations are approximate from press/analyst reports
SPCX_FUNDING_ROUNDS: list[dict[str, Any]] = [
    {
        "round": "Series A",
        "date": "2002-01",
        "valuation_usd": 10000000,
        "share_price_estimated": 0.01,
        "amount_raised_usd": None,
        "investors": ["Founders"],
        "source": "estimate",
    },
    {
        "round": "Series C",
        "date": "2008-08",
        "valuation_usd": 800000000,
        "share_price_estimated": 0.50,
        "amount_raised_usd": 20000000,
        "investors": ["Founders Fund", "Draper Fisher Jurvetson"],
        "source": "press",
    },
    {
        "round": "Series D",
        "date": "2010-11",
        "valuation_usd": 1200000000,
        "share_price_estimated": 0.75,
        "amount_raised_usd": 50000000,
        "investors": ["Founders Fund", "Draper Fisher Jurvetson"],
        "source": "press",
    },
    {
        "round": "Series G",
        "date": "2015-01",
        "valuation_usd": 11000000000,
        "share_price_estimated": 6.90,
        "amount_raised_usd": 1000000000,
        "investors": ["Google", "Fidelity"],
        "source": "press",
    },
    {
        "round": "Series H",
        "date": "2017-07",
        "valuation_usd": 21000000000,
        "share_price_estimated": 13.10,
        "amount_raised_usd": 350000000,
        "investors": ["Fidelity", "DFJ"],
        "source": "press",
    },
    {
        "round": "Series J",
        "date": "2019-06",
        "valuation_usd": 33300000000,
        "share_price_estimated": 20.80,
        "amount_raised_usd": 536000000,
        "investors": ["Fidelity", "Baillie Gifford", "Founders Fund"],
        "source": "press",
    },
    {
        "round": "Series N",
        "date": "2021-02",
        "valuation_usd": 74000000000,
        "share_price_estimated": 41.90,
        "amount_raised_usd": 850000000,
        "investors": ["Sequoia", "Valor Equity", "Coatue", "D1 Capital"],
        "source": "press",
    },
    {
        "round": "Series N+",
        "date": "2022-01",
        "valuation_usd": 100000000000,
        "share_price_estimated": 56.30,
        "amount_raised_usd": 337000000,
        "investors": ["Valor Equity", "Sequoia"],
        "source": "press",
    },
    {
        "round": "Tender",
        "date": "2024-06",
        "valuation_usd": 210000000000,
        "share_price_estimated": 112.00,
        "amount_raised_usd": None,
        "investors": ["Tender Offer — Secondary"],
        "source": "press",
    },
    {
        "round": "Tender",
        "date": "2025-12",
        "valuation_usd": 350000000000,
        "share_price_estimated": 135.00,
        "amount_raised_usd": None,
        "investors": ["Tender Offer — Pre-IPO"],
        "source": "press",
    },
    {
        "round": "IPO",
        "date": "2026-06-11",
        "valuation_usd": 1770000000000,
        "share_price_estimated": 135.00,
        "amount_raised_usd": 75000000000,
        "investors": ["Public"],
        "source": "sec_filing",
    },
]


def collect_spcx_private_rounds() -> dict[str, Any]:
    """Collect SPCX pre-IPO funding round data for cost basis reconstruction.

    Returns funding round history with estimated share prices.
    All prices marked as cost_basis_estimated=True unless from a filing.
    """
    result = {
        "source": "spcx_private_rounds",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": True,
        "symbol": "SPCX",
        "ipo_price": 135.0,
        "current_price": None,

        "rounds": [],
        "summary": {
            "total_rounds": 0,
            "earliest_round_date": None,
            "latest_private_round_date": None,
            "pre_ipo_valuation_usd": None,
            "ipo_valuation_usd": 1770000000000,
            "estimated_early_investor_gain_pct": None,
            "estimated_series_a_gain_pct": None,
            "estimated_late_round_gain_pct": None,
        },

        "error": None,
    }

    # Enrich with current price if available
    try:
        from modules.ipo_tracking.collectors.yahoo_public import collect_yahoo_quote
        yahoo = collect_yahoo_quote("SPCX")
        price = yahoo.get("regular_market_price")
        if price:
            result["current_price"] = float(price)
    except Exception:
        scored = REPO_ROOT / "data" / "ipo" / "spacex" / "scored" / "latest_snapshot.json"
        if scored.exists():
            snap = json.loads(scored.read_text())
            yahoo = (snap.get("latest_events", {}) or {}).get("yahoo_chart", {})
            price = yahoo.get("regular_market_price")
            if price:
                result["current_price"] = float(price)

    current_price = result["current_price"]

    for r in SPCX_FUNDING_ROUNDS:
        price = r.get("share_price_estimated")
        gain_pct = None
        if current_price and price and price > 0:
            gain_pct = round((current_price - price) / price * 100, 1)

        entry = {
            "round": r["round"],
            "date": r["date"],
            "valuation_usd": r["valuation_usd"],
            "share_price_estimated": price,
            "amount_raised_usd": r["amount_raised_usd"],
            "investors": r["investors"],
            "source": r["source"],
            "cost_basis_estimated": r["source"] != "sec_filing",
            "current_gain_pct": gain_pct,
        }
        result["rounds"].append(entry)

    # Summary
    result["summary"]["total_rounds"] = len(result["rounds"])
    if result["rounds"]:
        result["summary"]["earliest_round_date"] = result["rounds"][0].get("date")
        pre_ipo = [r for r in result["rounds"] if r["round"] != "IPO"]
        if pre_ipo:
            result["summary"]["latest_private_round_date"] = pre_ipo[-1].get("date")
            result["summary"]["pre_ipo_valuation_usd"] = pre_ipo[-1].get("valuation_usd")

    # Gain estimates
    if current_price:
        series_a = next((r for r in result["rounds"] if "Series A" in r["round"]), None)
        if series_a:
            result["summary"]["estimated_series_a_gain_pct"] = series_a.get("current_gain_pct")

        late_rounds = [r for r in result["rounds"] if r["date"] >= "2021"]
        if late_rounds:
            avg_price = sum(
                _float(r.get("share_price_estimated", 0)) for r in late_rounds
            ) / len(late_rounds)
            if avg_price > 0:
                result["summary"]["estimated_late_round_gain_pct"] = round(
                    (current_price - avg_price) / avg_price * 100, 1
                )

        result["summary"]["estimated_early_investor_gain_pct"] = series_a.get("current_gain_pct") if series_a else None

    return result


def _float(v: Any) -> float:
    if v is None:
        return 0.0
    try:
        return float(v)
    except (ValueError, TypeError):
        return 0.0
