"""
Configuration for the Market Thesis Engine — PR2.

Source paths, symbol normalization, alias maps, freshness thresholds.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

# ── Repo root ──────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[2]

# ── Source paths ───────────────────────────────────────────────────────────

SOURCES = {
    "events_jsonl": REPO_ROOT / "state" / "events.jsonl",
    "events_cdp_jsonl": REPO_ROOT / "state" / "events_cdp.jsonl",
    "market_metrics": REPO_ROOT / "data" / "data_center" / "views" / "market_metrics" / "by_symbol",
    "multitf_analysis": REPO_ROOT / "data" / "data_center" / "views" / "multitf_analysis_input.v1" / "by_symbol",
    "multitf_scores": REPO_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "by_symbol",
    "signal_event": REPO_ROOT / "data" / "data_center" / "views" / "signal_event.v1" / "by_symbol",
    "vision_coinglass": REPO_ROOT / "data" / "deskpro" / "inputs" / "vision_context" / "coinglass" / "latest.json",
    "telegram_screener": REPO_ROOT / "data" / "telegram_screener" / "signals",
    "telegram_signals_dc": REPO_ROOT / "data" / "data_center" / "views" / "telegram_signals" / "by_symbol",
    "vision_analysis_dc": REPO_ROOT / "data" / "data_center" / "views" / "vision_analysis" / "by_symbol",
}

# ── Canonical symbols (the 9 target assets) ────────────────────────────────

CANONICAL_SYMBOLS: List[str] = [
    "BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU",
]

# ── Symbol normalization ───────────────────────────────────────────────────

# Maps raw symbols from various sources → canonical symbol
SYMBOL_MAP: Dict[str, str] = {
    # market_metrics.v1 (Binance-style)
    "BTCUSDT": "BTC",
    "ETHUSDT": "ETH",
    "SOLUSDT": "SOL",
    "XRPUSDT": "XRP",
    "DOGEUSDT": "DOGE",
    "BNBUSDT": "BNB",
    "ADAUSDT": "ADA",
    "PAXGUSDT": "XAU",
    "XAUUSD": "XAU",
    # vision_analysis (TradingView-style)
    "BTCUSDT.P": "BTC",
    "ETHUSDT.P": "ETH",
    "SOLUSDT.P": "SOL",
    "XRPUSDT.P": "XRP",
    "DOGEUSDT.P": "DOGE",
    "OANDA:XAUUSD": "XAU",
    # spacex_true_value / equity
    "SPCX": "SPCX",
    "NVDA": "NVDA",
    "AVGO": "AVGO",
    "MU": "MU",
    # telegram (various formats)
    "XAU/USD": "XAU",
    "BTC/USD": "BTC",
    "ETH/USD": "ETH",
    "SOL/USD": "SOL",
    "XRP/USD": "XRP",
    # market_metrics display format
    "BTC/USDT": "BTC",
    "ETH/USDT": "ETH",
    "SOL/USDT": "SOL",
    "XRP/USDT": "XRP",
    "XAU/USD": "XAU",
}

# ── Signal event alias normalization ───────────────────────────────────────

EVENT_ALIAS_MAP: Dict[str, str] = {
    "orb_break_high": "ORB_HIGH_BREAK",
    "orb_break_low": "ORB_LOW_BREAK",
    "volume_spike": "VOLUME_SURGE",
    "vwap_reclaim": "VWAP_RECLAIM",
    "vwap_loss": "VWAP_LOSS",
    "bos": "BOS",
    "bos_bull": "BOS_BULL",
    "bos_bear": "BOS_BEAR",
    "choch": "CHOCH",
    "choch_bull": "CHOCH_BULL",
    "choch_bear": "CHOCH_BEAR",
    "fvg_created": "FVG_CREATED",
    "fvg_filled": "FVG_FILLED",
    "support_test": "SUPPORT_TEST",
    "resistance_test": "RESISTANCE_TEST",
    "trend_continuation": "TREND_CONTINUATION",
    "trend_reversal": "TREND_REVERSAL",
    "liquidity_sweep_high": "LIQUIDITY_SWEEP_HIGH",
    "liquidity_sweep_low": "LIQUIDITY_SWEEP_LOW",
}

# ── Freshness thresholds (minutes) ─────────────────────────────────────────

FRESHNESS_THRESHOLDS: Dict[str, Tuple[int, int, int]] = {
    "fresh": (0, 5),        # <= 5 minutes
    "warm": (5, 30),        # <= 30 minutes
    "stale": (30, 240),     # <= 4 hours
    "expired": (240, None), # > 4 hours
}

# ── File mtime fallback ────────────────────────────────────────────────────

# When a source file has no embedded timestamp, use its mtime.
# This offset can be tuned to adjust for known clock skew or pipeline delay.
MTIME_SKEW_TOLERANCE_SECONDS: int = 10


def normalize_symbol(raw: str) -> str:
    """Normalize a raw symbol to its canonical form."""
    if raw in SYMBOL_MAP:
        return SYMBOL_MAP[raw]
    return raw.upper()


def normalize_event_alias(raw: str) -> str:
    """Normalize a signal event name to its canonical alias."""
    return EVENT_ALIAS_MAP.get(raw, raw.upper())


def source_path_for_symbol(source_key: str, symbol: str) -> Path | None:
    """Resolve the file path for a given source and canonical symbol.

    Returns None if the source key is unknown.
    """
    base = SOURCES.get(source_key)
    if base is None:
        return None

    # Reverse lookup: try raw symbol variations
    reverse_map: Dict[str, str] = {v: k for k, v in SYMBOL_MAP.items()}
    raw_candidates: List[str] = [symbol] + [k for k, v in SYMBOL_MAP.items() if v == symbol]

    # Per-source filename construction
    if source_key in ("market_metrics", "multitf_analysis", "multitf_scores"):
        # These use raw symbol + ".json" in by_symbol/
        for raw in raw_candidates:
            path = base / f"{raw}.json"
            if path.exists():
                return path
        # Fallback: try canonical symbol
        return base / f"{symbol}.json"

    if source_key == "signal_event":
        # by_symbol/{SYM}/latest.json
        for raw in raw_candidates:
            path = base / raw / "latest.json"
            if path.exists():
                return path
        return base / symbol / "latest.json"

    if source_key == "vision_coinglass":
        return base  # single file

    if source_key == "events_jsonl" or source_key == "events_cdp_jsonl":
        return base  # single file, filtered by symbol at read time

    if source_key == "telegram_screener":
        return base  # directory of individual signal files

    if source_key == "telegram_signals_dc":
        for raw in raw_candidates:
            path = base / raw / "latest.json"
            if path.exists():
                return path
        return base / symbol / "latest.json"

    if source_key == "vision_analysis_dc":
        for raw in raw_candidates:
            path = base / f"{raw}.json"
            if path.exists():
                return path
        return base / f"{symbol}.json"

    return None
