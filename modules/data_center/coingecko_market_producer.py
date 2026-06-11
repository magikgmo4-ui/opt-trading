"""
coingecko_market_producer.py — free market data from CoinGecko API → data_center.

CoinGecko is free, no API key required (rate limit: 10-30 calls/min).

Produces:
    market_metrics.v1 — prices, 24h change for tracked pairs
    pair_market_snapshot.v1 — OHLCV snapshots for Desk Pro

Usage:
    python -m modules.data_center.coingecko_market_producer
    python -m modules.data_center.coingecko_market_producer --history
"""

from __future__ import annotations

import json
import tempfile
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_COINGECKO = "https://api.coingecko.com/api/v3"

# CoinGecko coin IDs for our tracked pairs
_COIN_MAP = {
    "BTC/USDT": {"id": "bitcoin", "symbol": "btc"},
    "ETH/USDT": {"id": "ethereum", "symbol": "eth"},
    "SOL/USDT": {"id": "solana", "symbol": "sol"},
    "XRP/USDT": {"id": "ripple", "symbol": "xrp"},
    "DOGE/USDT": {"id": "dogecoin", "symbol": "doge"},
    "BNB/USDT": {"id": "binancecoin", "symbol": "bnb"},
    "ADA/USDT": {"id": "cardano", "symbol": "ada"},
    "AVAX/USDT": {"id": "avalanche-2", "symbol": "avax"},
    "LINK/USDT": {"id": "chainlink", "symbol": "link"},
    "INJ/USDT": {"id": "injective-protocol", "symbol": "inj"},
    "APT/USDT": {"id": "aptos", "symbol": "apt"},
    "OP/USDT": {"id": "optimism", "symbol": "op"},
    "XAU/USD": {"id": "tether-gold", "symbol": "xaut"},
}
_HISTORY_DIR = _PROJECT_ROOT / "data" / "market_data" / "coingecko_history"


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp") as fh:
        json.dump(payload, fh, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def _fetch_json(url: str) -> Optional[dict]:
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  CoinGecko fetch error: {e}")
        return None


def fetch_prices(coin_ids: Optional[list[str]] = None) -> dict:
    """Fetch current prices from CoinGecko simple/price endpoint."""
    ids = coin_ids or [c["id"] for c in _COIN_MAP.values()]
    ids_param = ",".join(ids)
    url = f"{_COINGECKO}/simple/price?ids={ids_param}&vs_currencies=usd&include_24hr_change=true"
    data = _fetch_json(url)
    return data if isinstance(data, dict) else {}


def fetch_history(coin_id: str, days: int = 90) -> Optional[list[dict]]:
    """Fetch historical daily prices from CoinGecko market_chart."""
    url = f"{_COINGECKO}/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
    data = _fetch_json(url)
    if not data or not isinstance(data, dict):
        return None

    prices = data.get("prices", [])
    klines = []
    for p in prices:
        if isinstance(p, list) and len(p) >= 2:
            ts_ms = p[0]
            klines.append({
                "open_time": ts_ms,
                "open_time_iso": datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat(),
                "price": p[1],
            })
    return klines


def produce_metrics() -> dict:
    """Fetch CoinGecko prices and publish to data_center."""
    now = datetime.now(timezone.utc).isoformat()
    prices = fetch_prices()

    if not prices:
        return {"error": "no_coingecko_data", "produced_at": now}

    # Write per-symbol views
    tickers = {}
    for pair_display, coin in _COIN_MAP.items():
        coin_data = prices.get(coin["id"], {})
        price = coin_data.get("usd")
        change = coin_data.get("usd_24h_change")
        if price is None:
            continue

        sym_safe = pair_display.replace("/", "_").replace(":", "_")
        tickers[sym_safe] = {"price": price, "change_pct": change}

        # market_metrics.v1
        mm_dir = _VIEWS_DIR / "market_metrics" / "by_symbol" / sym_safe
        mm_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write(mm_dir / "latest.json", {
            "input_class": "market_metrics.v1",
            "provider_id": "coingecko_public_api",
            "symbol": pair_display,
            "produced_at": now,
            "metrics": {
                "price": price,
                "price_change_24h_pct": change,
            },
        })

        # pair_market_snapshot.v1
        snap_dir = _VIEWS_DIR / "pair_market_snapshot" / "by_symbol" / sym_safe
        snap_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write(snap_dir / "latest.json", {
            "input_class": "pair_market_snapshot.v1",
            "provider_id": "coingecko_public_api",
            "symbol": pair_display,
            "produced_at": now,
            "snapshot": {"price": price, "change_24h_pct": change},
            "freshness_state": "fresh",
        })

    # Global latest
    _atomic_write(_VIEWS_DIR / "market_metrics" / "latest.json", {
        "input_class": "market_metrics.v1",
        "provider_id": "coingecko_public_api",
        "produced_at": now,
        "total_pairs": len(tickers),
        "pairs": [{"symbol": k, "price": v["price"], "change_24h_pct": v["change_pct"]} for k, v in sorted(tickers.items())],
    })
    _atomic_write(_VIEWS_DIR / "pair_market_snapshot" / "latest.json", {
        "input_class": "pair_market_snapshot.v1",
        "provider_id": "coingecko_public_api",
        "produced_at": now,
        "total_pairs": len(tickers),
        "pairs": list(tickers.keys()),
    })

    # Runtime registry
    from modules.data_center.runtime_registry import update_producer_last_write
    for contract in ("market_metrics.v1", "pair_market_snapshot.v1"):
        update_producer_last_write(
            producer_id="coingecko_public_api", contract_class=contract,
            output_path=str(_VIEWS_DIR / "market_metrics" / "latest.json"),
            status="ok", evidence={"pairs": len(tickers)},
        )

    return {"produced_at": now, "pairs": len(tickers)}


def produce_history(days: int = 90) -> dict:
    """Fetch historical data from CoinGecko for backtesting (rate-limited)."""
    results = {}
    for pair_display, coin in _COIN_MAP.items():
        print(f"  Fetching {coin['id']}...")
        klines = fetch_history(coin["id"], days=days)
        if not klines:
            continue

        sym_safe = pair_display.replace("/", "_")
        hist_path = _HISTORY_DIR / f"{sym_safe}.json"
        hist_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "input_class": "market_klines.v1",
            "provider_id": "coingecko_public_api",
            "symbol": pair_display,
            "interval": "1d",
            "produced_at": datetime.now(timezone.utc).isoformat(),
            "klines": klines,
            "date_range": f"{klines[0]['open_time_iso'][:10]} -> {klines[-1]['open_time_iso'][:10]}",
        }
        _atomic_write(hist_path, payload)
        results[pair_display] = {"count": len(klines)}
        time.sleep(1.5)  # Rate limit: ~40 calls/min

    return {"pairs": results}


if __name__ == "__main__":
    import sys
    if "--history" in sys.argv:
        produce_history()
    else:
        result = produce_metrics()
        if "error" in result:
            print("ERROR:", result["error"])
        else:
            print(f"CoinGecko metrics: {result['pairs']} pairs updated")
