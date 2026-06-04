"""
asset_selector — per-asset selection and analysis tickets.

Reads vision analysis data and produces per-asset analysis tickets with:
- Current bias (from chart analysis)
- Support/resistance levels
- Trading plan
- Invalidation conditions
- Freshness state
- Screen type
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .vision_analysis_reader import extract_signals_from_vision, list_available_symbols, read_vision_analysis_freshness

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

_ASSET_CLASSIFICATION = {
    "BTCUSDT.P": {"asset": "BTC", "class": "CRYPTO_MAJOR", "product": "PERP"},
    "ETHUSDT.P": {"asset": "ETH", "class": "CRYPTO_MAJOR", "product": "PERP"},
    "SOLUSDT.P": {"asset": "SOL", "class": "CRYPTO_ALT_L1", "product": "PERP"},
    "DOGEUSDT.P": {"asset": "DOGE", "class": "CRYPTO_MEME", "product": "PERP"},
    "XRPUSDT.P": {"asset": "XRP", "class": "CRYPTO_ALT_L1", "product": "PERP"},
    "TVC:DXY": {"asset": "DXY", "class": "MACRO_FX", "product": "INDEX"},
    "TVC:VIX": {"asset": "VIX", "class": "MACRO_VOL", "product": "INDEX"},
    "TVC:US10Y": {"asset": "US10Y", "class": "MACRO_RATES", "product": "BOND"},
    "OANDA:XAUUSD": {"asset": "GOLD", "class": "MACRO_COMMODITY", "product": "SPOT"},
    "SPY": {"asset": "SPX", "class": "MACRO_EQUITY", "product": "ETF"},
    "NYMEX:CL1!": {"asset": "WTI", "class": "ENERGY", "product": "FUTURES"},
    "NYMEX:RB1!": {"asset": "GASOLINE", "class": "ENERGY", "product": "FUTURES"},
    "NYMEX:NG1!": {"asset": "NATGAS", "class": "ENERGY", "product": "FUTURES"},
    "BITGET:BZUSDT": {"asset": "BRENT", "class": "ENERGY", "product": "PERP"},
    "FX:EURUSD": {"asset": "EURUSD", "class": "MACRO_FX", "product": "SPOT"},
    "CRYPTOCAP:BTC.D": {"asset": "BTC_DOM", "class": "CRYPTO_MARKET", "product": "INDEX"},
    "CRYPTOCAP:TOTAL": {"asset": "TOTAL", "class": "CRYPTO_MARKET", "product": "INDEX"},
    "CRYPTOCAP:TOTAL2": {"asset": "TOTAL2", "class": "CRYPTO_MARKET", "product": "INDEX"},
    "CRYPTOCAP:TOTAL3": {"asset": "TOTAL3", "class": "CRYPTO_MARKET", "product": "INDEX"},
    "NASDAQ:IBIT": {"asset": "IBIT", "class": "CRYPTO_ETF", "product": "ETF"},
    "NASDAQ:ARKB": {"asset": "ARKB", "class": "CRYPTO_ETF", "product": "ETF"},
    "NASDAQ:BITB": {"asset": "BITB", "class": "CRYPTO_ETF", "product": "ETF"},
    "NASDAQ:FBTC": {"asset": "FBTC", "class": "CRYPTO_ETF", "product": "ETF"},
    "OTC:GBTC": {"asset": "GBTC", "class": "CRYPTO_ETF", "product": "ETF"},
}


def produce_asset_ticket(symbol: str) -> Optional[dict]:
    """Produce a per-asset analysis ticket from vision analysis data."""
    signals = extract_signals_from_vision(symbol)
    if not signals.get("available"):
        return None

    freshness = read_vision_analysis_freshness(symbol)
    classification = _ASSET_CLASSIFICATION.get(symbol, {"asset": symbol, "class": "UNKNOWN", "product": "UNKNOWN"})

    return {
        "contract": "asset_ticket.v1",
        "symbol": symbol,
        "asset": classification["asset"],
        "asset_class": classification["class"],
        "product": classification["product"],
        "produced_at": datetime.now(timezone.utc).isoformat(),
        "freshness": freshness.get("freshness", "UNKNOWN"),
        "analysis_ts": signals.get("analysis_ts"),
        "timeframe": signals.get("timeframe"),
        "screen_type": signals.get("screen_type"),
        "bias": signals.get("bias"),
        "supports": signals.get("supports", []),
        "resistances": signals.get("resistances", []),
        "plan": signals.get("plan"),
        "invalidation": signals.get("invalidation"),
    }


def produce_all_tickets() -> dict[str, dict]:
    """Produce analysis tickets for all available symbols."""
    tickets = {}
    for symbol in list_available_symbols():
        ticket = produce_asset_ticket(symbol)
        if ticket:
            tickets[symbol] = ticket
    return tickets


def produce_summary_by_class() -> dict[str, dict]:
    """Summarize tickets grouped by asset class."""
    tickets = produce_all_tickets()
    by_class: dict[str, list[dict]] = {}
    for symbol, ticket in tickets.items():
        cls = ticket.get("asset_class", "UNKNOWN")
        if cls not in by_class:
            by_class[cls] = []
        by_class[cls].append(ticket)

    summary = {}
    for cls, items in by_class.items():
        fresh = sum(1 for t in items if t.get("freshness") == "FRESH")
        bullish = sum(1 for t in items if t.get("bias") == "BULLISH")
        bearish = sum(1 for t in items if t.get("bias") == "BEARISH")
        summary[cls] = {
            "total": len(items),
            "fresh": fresh,
            "stale": len(items) - fresh,
            "bullish": bullish,
            "bearish": bearish,
            "neutral": len(items) - bullish - bearish,
            "assets": [t["asset"] for t in items],
        }
    return summary
