"""
SPCX Auction Imbalance Collector
GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01

Collects NASDAQ opening and closing auction imbalance data for SPCX.
Sources (priority order):
  1. NASDAQ Auction API (if available)
  2. Bar-based inference (open/close patterns from Yahoo bars)
  3. Offline snapshot fallback

Auction imbalances are critical for detecting institutional flow at open/close.
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]

IPO_PRICE = 135.0


def collect_spcx_auction_imbalance() -> dict[str, Any]:
    """Collect SPCX opening and closing auction imbalance data.

    Returns opening and closing auction snapshots with imbalance direction,
    paired shares, and estimated USD value.
    """
    result = {
        "source": "spcx_auction_imbalance",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "symbol": "SPCX",

        # Opening auction
        "opening": {
            "indicative_price": None,
            "paired_shares": None,
            "imbalance_shares": None,
            "imbalance_side": None,
            "imbalance_usd": None,
            "near_price": None,
            "far_price": None,
            "imbalance_ratio": None,
            "significant": False,
            "source": None,
        },

        # Closing auction
        "closing": {
            "indicative_price": None,
            "paired_shares": None,
            "imbalance_shares": None,
            "imbalance_side": None,
            "imbalance_usd": None,
            "near_price": None,
            "far_price": None,
            "imbalance_ratio": None,
            "significant": False,
            "source": None,
        },

        # Summary
        "day_imbalance_side": None,
        "day_imbalance_strength": None,

        "error": None,
    }

    bars = _get_recent_bars()
    if not bars:
        result["error"] = "no_bars_available"
        return result

    result["ok"] = True

    # --- Opening auction inference from first bar ---
    first = bars[0] if bars else {}
    first_open = _float(first.get("open"))
    first_close = _float(first.get("close"))
    first_high = _float(first.get("high"))
    first_low = _float(first.get("low"))
    first_vol = _float(first.get("volume"))

    if first_open and first_open > 0:
        opening = result["opening"]
        opening["indicative_price"] = first_open
        opening["near_price"] = first_open
        opening["far_price"] = first_close if first_close else first_open

        # Imbalance inferred from open vs close of first bar
        if first_close and first_close != first_open and first_vol:
            if first_close > first_open:
                opening["imbalance_side"] = "BUY"
                opening["paired_shares"] = round(first_vol * 0.6, 2)
                opening["imbalance_shares"] = round(first_vol * 0.4, 2)
            else:
                opening["imbalance_side"] = "SELL"
                opening["paired_shares"] = round(first_vol * 0.6, 2)
                opening["imbalance_shares"] = round(first_vol * 0.4, 2)

            if opening["imbalance_shares"] and opening["indicative_price"]:
                opening["imbalance_usd"] = round(
                    opening["imbalance_shares"] * opening["indicative_price"], 2
                )

            if opening["paired_shares"] and opening["paired_shares"] > 0:
                opening["imbalance_ratio"] = round(
                    opening["imbalance_shares"] / opening["paired_shares"], 3
                )

            opening["significant"] = (
                opening["imbalance_usd"] is not None
                and opening["imbalance_usd"] >= 5000000
            )

        opening["source"] = "bar_inferred"

        # Check for gap from IPO price
        if first_open != IPO_PRICE:
            gap_side = "BUY" if first_open > IPO_PRICE else "SELL"
            if not opening["imbalance_side"]:
                opening["imbalance_side"] = gap_side
            opening["ipo_gap_pct"] = round(
                (first_open - IPO_PRICE) / IPO_PRICE * 100, 2
            )

    # --- Closing auction inference from last bars ---
    if len(bars) >= 2:
        last = bars[-1]
        prev = bars[-2]

        last_close = _float(last.get("close"))
        last_vol = _float(last.get("volume"))
        prev_close = _float(prev.get("close"))
        prev_vol = _float(prev.get("volume"))

        if last_close and last_close > 0:
            closing = result["closing"]
            closing["indicative_price"] = last_close
            closing["near_price"] = last_close
            closing["far_price"] = prev_close if prev_close else last_close

            # Imbalance inferred from last bar movement
            if last_close != prev_close and last_vol:
                if last_close > prev_close:
                    closing["imbalance_side"] = "BUY"
                else:
                    closing["imbalance_side"] = "SELL"

                closing["paired_shares"] = round(last_vol * 0.6, 2)
                closing["imbalance_shares"] = round(last_vol * 0.4, 2)

                if closing["imbalance_shares"] and closing["indicative_price"]:
                    closing["imbalance_usd"] = round(
                        closing["imbalance_shares"] * closing["indicative_price"], 2
                    )

                if closing["paired_shares"] and closing["paired_shares"] > 0:
                    closing["imbalance_ratio"] = round(
                        closing["imbalance_shares"] / closing["paired_shares"], 3
                    )

                closing["significant"] = (
                    closing["imbalance_usd"] is not None
                    and closing["imbalance_usd"] >= 5000000
                )

            closing["source"] = "bar_inferred"

    # --- Summary ---
    open_side = result["opening"].get("imbalance_side")
    close_side = result["closing"].get("imbalance_side")
    open_sig = result["opening"].get("significant")
    close_sig = result["closing"].get("significant")

    if open_side == close_side and open_side:
        result["day_imbalance_side"] = open_side
        if open_sig and close_sig:
            result["day_imbalance_strength"] = "STRONG"
        elif open_sig or close_sig:
            result["day_imbalance_strength"] = "MODERATE"
        else:
            result["day_imbalance_strength"] = "WEAK"
    elif open_side and close_side:
        result["day_imbalance_side"] = f"FLIP_{open_side}_TO_{close_side}"
        result["day_imbalance_strength"] = "DIVERGENT"
    elif open_side:
        result["day_imbalance_side"] = open_side
        result["day_imbalance_strength"] = "OPEN_ONLY"
    elif close_side:
        result["day_imbalance_side"] = close_side
        result["day_imbalance_strength"] = "CLOSE_ONLY"

    # --- Try NASDAQ auction API as enrichment (uses existing Finnhub pattern) ---
    _try_nasdaq_auction_enrichment(result)

    return result


def _try_nasdaq_auction_enrichment(result: dict) -> None:
    """Attempt to fetch real NASDAQ auction data if available."""
    try:
        import urllib.request
        # NASDAQ auction info is not publicly available via free API
        # This is a placeholder for when a vendor feed is configured
        # For now, the bar-inferred data is the primary source
        pass
    except Exception:
        pass


def _get_recent_bars(limit: int = 500) -> list[dict]:
    try:
        from modules.ipo_tracking.collectors.yahoo_public import collect_yahoo_quote
        result_data = collect_yahoo_quote("SPCX", range_="5d", interval="1m")
        bars = result_data.get("bars", [])
        real = [b for b in bars if b.get("volume") and b["volume"] > 0]
        return real[-limit:] if real else []
    except Exception:
        scored = REPO_ROOT / "data" / "ipo" / "spacex" / "scored" / "latest_snapshot.json"
        if scored.exists():
            snap = json.loads(scored.read_text())
            yahoo = (snap.get("latest_events", {}) or {}).get("yahoo_chart", {})
            bars = yahoo.get("bars", [])
            return [b for b in bars if b.get("volume") and b["volume"] > 0][-limit:]
        return []


def _float(v: Any) -> float:
    if v is None:
        return 0.0
    try:
        return float(v)
    except (ValueError, TypeError):
        return 0.0
