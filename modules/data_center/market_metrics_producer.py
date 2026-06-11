"""
market_metrics_producer.py — fetch market data from Binance public API, publish to data_center.

Produces:
    market_metrics.v1 — current prices, 24h stats for tracked pairs
    Writes to: data/data_center/views/market_metrics/by_symbol/{SYMBOL}.json
               data/data_center/views/market_metrics/latest.json

Also fetches historical klines for backtest resolution (last 90 days, daily candles).

Usage:
    python -m modules.data_center.market_metrics_producer
    python -m modules.data_center.market_metrics_producer --klines  # also fetch historical
"""

from __future__ import annotations

import json
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_BINANCE_API = "https://api.binance.com"

# Pairs we track (Binance symbols)
_TRACKED_PAIRS = {
    "BTCUSDT": {"asset": "BTC", "pair_display": "BTC/USDT", "priority": "P0"},
    "ETHUSDT": {"asset": "ETH", "pair_display": "ETH/USDT", "priority": "P0"},
    "SOLUSDT": {"asset": "SOL", "pair_display": "SOL/USDT", "priority": "P1"},
    "XRPUSDT": {"asset": "XRP", "pair_display": "XRP/USDT", "priority": "P1"},
    "DOGEUSDT": {"asset": "DOGE", "pair_display": "DOGE/USDT", "priority": "P2"},
    "BNBUSDT": {"asset": "BNB", "pair_display": "BNB/USDT", "priority": "P1"},
    "ADAUSDT": {"asset": "ADA", "pair_display": "ADA/USDT", "priority": "P2"},
    "AVAXUSDT": {"asset": "AVAX", "pair_display": "AVAX/USDT", "priority": "P2"},
    "LINKUSDT": {"asset": "LINK", "pair_display": "LINK/USDT", "priority": "P2"},
    "INJUSDT": {"asset": "INJ", "pair_display": "INJ/USDT", "priority": "P2"},
    "APTUSDT": {"asset": "APT", "pair_display": "APT/USDT", "priority": "P2"},
    "OPUSDT": {"asset": "OP", "pair_display": "OP/USDT", "priority": "P2"},
    # XAU/USD proxy via PAXG (PAX Gold token)
    "PAXGUSDT": {"asset": "XAUUSD", "pair_display": "XAU/USD", "priority": "P0"},
}

_KLINES_DIR = _PROJECT_ROOT / "data" / "market_data" / "klines"


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp"
    ) as fh:
        json.dump(payload, fh, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def _fetch_json(url: str) -> Optional[dict | list]:
    """Fetch JSON from URL, return None on error."""
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def fetch_ticker_prices(symbols: Optional[list[str]] = None) -> dict[str, dict]:
    """Fetch 24hr ticker prices from Binance. Returns {SYMBOL: {price, change_pct, volume, ...}}"""
    syms = symbols or list(_TRACKED_PAIRS.keys())
    # Binance ticker endpoint
    syms_param = json.dumps(syms)
    url = f"{_BINANCE_API}/api/v3/ticker/24hr?symbols={syms_param}"
    data = _fetch_json(url)
    if not data or not isinstance(data, list):
        return {}

    result = {}
    for ticker in data:
        if not isinstance(ticker, dict):
            continue
        sym = ticker.get("symbol", "")
        if sym not in _TRACKED_PAIRS:
            continue
        result[sym] = {
            "symbol": sym,
            "price": float(ticker.get("lastPrice", 0)),
            "price_change_pct": float(ticker.get("priceChangePercent", 0)),
            "high_24h": float(ticker.get("highPrice", 0)),
            "low_24h": float(ticker.get("lowPrice", 0)),
            "volume_24h": float(ticker.get("volume", 0)),
            "quote_volume_24h": float(ticker.get("quoteVolume", 0)),
        }
    return result


def fetch_klines(symbol: str, interval: str = "1d", limit: int = 90) -> list[dict]:
    """Fetch historical klines from Binance. Returns list of {open_time, open, high, low, close, volume}"""
    url = f"{_BINANCE_API}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    data = _fetch_json(url)
    if not data or not isinstance(data, list):
        return []

    klines = []
    for k in data:
        if not isinstance(k, list) or len(k) < 6:
            continue
        klines.append({
            "open_time": int(k[0]),
            "open_time_iso": datetime.fromtimestamp(int(k[0]) / 1000, tz=timezone.utc).isoformat(),
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
        })
    return klines


def produce_market_metrics() -> dict:
    """Fetch market data and publish to data_center views.
    
    Produces:
      - market_metrics.v1 (per-symbol prices, 24h stats)
      - pair_market_snapshot.v1 (OHLCV snapshot for Desk Pro)
    """
    now = datetime.now(timezone.utc).isoformat()
    tickers = fetch_ticker_prices()
    if not tickers:
        return {"error": "no_ticker_data", "produced_at": now}

    # Build per-symbol views for market_metrics.v1
    for sym, ticker in tickers.items():
        info = _TRACKED_PAIRS.get(sym, {})
        pair_display = info.get("pair_display", sym)
        symbol_dir = _VIEWS_DIR / "market_metrics" / "by_symbol" / sym
        symbol_dir.mkdir(parents=True, exist_ok=True)

        payload = {
            "input_class": "market_metrics.v1",
            "provider_id": "binance_public_api",
            "symbol": pair_display,
            "binance_symbol": sym,
            "priority": info.get("priority", "P2"),
            "produced_at": now,
            "metrics": {
                "price": ticker["price"],
                "price_change_24h_pct": ticker["price_change_pct"],
                "high_24h": ticker["high_24h"],
                "low_24h": ticker["low_24h"],
                "volume_24h": ticker["volume_24h"],
                "quote_volume_24h": ticker["quote_volume_24h"],
            },
        }
        _atomic_write(symbol_dir / "latest.json", payload)

        # Also produce pair_market_snapshot.v1 for Desk Pro
        snap_dir = _VIEWS_DIR / "pair_market_snapshot" / "by_symbol" / sym
        snap_dir.mkdir(parents=True, exist_ok=True)
        snapshot = {
            "input_class": "pair_market_snapshot.v1",
            "provider_id": "binance_public_api",
            "symbol": pair_display,
            "binance_symbol": sym,
            "produced_at": now,
            "snapshot": {
                "price": ticker["price"],
                "change_24h_pct": ticker["price_change_pct"],
                "high_24h": ticker["high_24h"],
                "low_24h": ticker["low_24h"],
                "volume_24h": ticker["volume_24h"],
            },
            "freshness_state": "fresh",
        }
        _atomic_write(snap_dir / "latest.json", snapshot)

    # Build global latest for market_metrics.v1
    global_payload = {
        "input_class": "market_metrics.v1",
        "provider_id": "binance_public_api",
        "produced_at": now,
        "total_pairs": len(tickers),
        "pairs": [
            {
                "symbol": _TRACKED_PAIRS.get(sym, {}).get("pair_display", sym),
                "price": t["price"],
                "change_24h_pct": t["price_change_pct"],
            }
            for sym, t in sorted(tickers.items())
        ],
    }
    _atomic_write(_VIEWS_DIR / "market_metrics" / "latest.json", global_payload)

    # Global latest for pair_market_snapshot.v1
    snap_global = {
        "input_class": "pair_market_snapshot.v1",
        "provider_id": "binance_public_api",
        "produced_at": now,
        "total_pairs": len(tickers),
        "pairs": list(tickers.keys()),
    }
    _atomic_write(_VIEWS_DIR / "pair_market_snapshot" / "latest.json", snap_global)

    # Update runtime registry
    from modules.data_center.runtime_registry import update_producer_last_write
    for contract in ("market_metrics.v1", "pair_market_snapshot.v1"):
        update_producer_last_write(
            producer_id="binance_public_api",
            contract_class=contract,
            output_path=str(_VIEWS_DIR / "market_metrics" / "latest.json"),
            status="ok",
            evidence={"pairs_fetched": len(tickers)},
        )

    return global_payload


def produce_klines(symbols: Optional[list[str]] = None) -> dict:
    """Fetch historical klines for backtesting and store locally."""
    syms = symbols or list(_TRACKED_PAIRS.keys())
    now = datetime.now(timezone.utc).isoformat()
    results = {}

    for sym in syms:
        info = _TRACKED_PAIRS.get(sym, {})
        pair_display = info.get("pair_display", sym)
        klines = fetch_klines(sym, interval="1d", limit=90)

        if not klines:
            continue

        # Store klines
        sym_dir = _KLINES_DIR / sym
        sym_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "input_class": "market_klines.v1",
            "provider_id": "binance_public_api",
            "symbol": pair_display,
            "binance_symbol": sym,
            "interval": "1d",
            "produced_at": now,
            "klines": klines,
            "date_range": f"{klines[0]['open_time_iso'][:10]} → {klines[-1]['open_time_iso'][:10]}",
        }
        _atomic_write(sym_dir / "latest.json", payload)
        results[sym] = {"count": len(klines), "date_range": payload["date_range"]}

    return {"produced_at": now, "pairs": results}


def resolve_tp_sl_outcome(
    entry: float, sl: float, tp: float, direction: str,
    signal_ts: str, klines: list[dict],
) -> dict:
    """Determine if a trade hit TP or SL first using historical klines.

    Args:
        entry: entry price
        sl: stop loss price
        tp: take profit price
        direction: LONG or SHORT
        signal_ts: ISO timestamp of the signal
        klines: list of daily klines [{open_time_iso, high, low, close}, ...]

    Returns:
        {outcome: TP_HIT|SL_HIT|OPEN, hit_ts: ISO, hit_price: float, days_to_outcome: int}
    """
    if not klines:
        return {"outcome": "OPEN", "reason": "no_klines"}

    # Parse signal timestamp
    try:
        signal_dt = datetime.fromisoformat(signal_ts.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return {"outcome": "OPEN", "reason": "invalid_ts"}

    # Find klines after signal date
    for i, k in enumerate(klines):
        try:
            k_dt = datetime.fromisoformat(k["open_time_iso"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            continue

        if k_dt.date() < signal_dt.date():
            continue

        high = k["high"]
        low = k["low"]

        if direction == "LONG":
            if low <= sl:
                return {"outcome": "SL_HIT", "hit_price": sl, "hit_ts": k["open_time_iso"], "days": i}
            if high >= tp:
                return {"outcome": "TP_HIT", "hit_price": tp, "hit_ts": k["open_time_iso"], "days": i}
        else:  # SHORT
            if high >= sl:
                return {"outcome": "SL_HIT", "hit_price": sl, "hit_ts": k["open_time_iso"], "days": i}
            if low <= tp:
                return {"outcome": "TP_HIT", "hit_price": tp, "hit_ts": k["open_time_iso"], "days": i}

    return {"outcome": "OPEN", "reason": "no_outcome_in_klines", "days": len(klines)}


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if "--klines" in args:
        result = produce_klines()
        print("Klines fetched:", json.dumps(result, indent=2, default=str))
    else:
        result = produce_market_metrics()
        if "error" in result:
            print("ERROR:", result["error"])
        else:
            print(f"Market metrics: {result['total_pairs']} pairs fetched")
            for p in result.get("pairs", []):
                print(f"  {p['symbol']:12s} \${p['price']:>12,.2f} ({p['change_24h_pct']:+.2f}%)")
