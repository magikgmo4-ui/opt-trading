#!/usr/bin/env python3
"""fetch_bitget.py — Download XAUUSDT M5/M15 OHLCV from Bitget USDT-Futures API.

Source classification: bitget_xauusdt_futures_approx
  - XAUUSDT perpetual futures (Bitget) ≠ XAUUSD spot broker
  - Spread: snapshot from ticker API, applied uniformly to all historical bars
  - Historical depth: ~30 days M5 (Bitget API limit, tested 2026-05-20)
  - Use for: improved smoke / CONTEXT_RECENT_ONLY
  - Do NOT use as PRIMARY_READY for 180-day backtest verdict

Usage:
    python tools/strategy/daily_scalping/fetch_bitget.py \
        --out data/market \
        --days 30
"""
from __future__ import annotations

import argparse
import datetime
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import pandas as pd
import requests

BITGET_CANDLES_URL = "https://api.bitget.com/api/v2/mix/market/candles"
BITGET_TICKER_URL = "https://api.bitget.com/api/v2/mix/market/ticker"
SOURCE_TAG = "bitget_xauusdt_futures_approx"


def _fetch_ticker_spread(symbol: str, product_type: str) -> tuple[float, float]:
    r = requests.get(
        BITGET_TICKER_URL,
        params={"symbol": symbol, "productType": product_type},
        timeout=10,
    )
    r.raise_for_status()
    j = r.json()
    d = j.get("data", [{}])
    d = d[0] if isinstance(d, list) and d else (d if isinstance(d, dict) else {})
    bid = float(d.get("bidPr", 0) or 0)
    ask = float(d.get("askPr", 0) or 0)
    return bid, ask


def _fetch_candles_page(
    symbol: str,
    product_type: str,
    granularity_sec: int,
    start_ms: int,
    end_ms: int,
) -> list:
    params = {
        "symbol": symbol,
        "productType": product_type,
        "granularity": str(granularity_sec),
        "startTime": str(start_ms),
        "endTime": str(end_ms),
        "limit": "200",
    }
    r = requests.get(BITGET_CANDLES_URL, params=params, timeout=20)
    r.raise_for_status()
    j = r.json()
    if j.get("code") not in (None, "00000", 0):
        raise RuntimeError(f"Bitget error code={j.get('code')} msg={j.get('msg')}")
    return j.get("data") or []


def _fetch_all(
    symbol: str,
    product_type: str,
    granularity_sec: int,
    days: int,
) -> list:
    now_ms = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
    start_ms = now_ms - days * 24 * 60 * 60 * 1000
    page_ms = 200 * granularity_sec * 1000
    all_candles = []
    cursor = start_ms
    while cursor < now_ms:
        end_ms = min(cursor + page_ms, now_ms)
        page = _fetch_candles_page(symbol, product_type, granularity_sec, cursor, end_ms)
        all_candles.extend(page)
        if not page:
            cursor = end_ms + granularity_sec * 1000
        else:
            last_ts = int(page[-1][0])
            cursor = last_ts + granularity_sec * 1000
        time.sleep(0.1)
    return all_candles


def _to_dataframe(
    candles: list,
    granularity_sec: int,
    symbol: str,
    bid: float,
    ask: float,
) -> pd.DataFrame:
    rows = []
    timeframe = f"M{granularity_sec // 60}"
    spread = round(ask - bid, 6)
    for c in candles:
        ts_ms = int(c[0])
        ts = datetime.datetime.fromtimestamp(ts_ms / 1000, tz=datetime.timezone.utc)
        rows.append({
            "timestamp": ts.isoformat(),
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5]),
            "bid": bid,
            "ask": ask,
            "spread": spread,
            "source": SOURCE_TAG,
            "symbol": symbol,
            "timeframe": timeframe,
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.drop_duplicates(subset=["timestamp"]).sort_values("timestamp")
    return df


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch XAUUSDT M5/M15 from Bitget API")
    parser.add_argument("--out", default="data/market")
    parser.add_argument("--days", type=int, default=30, help="Days of history (max ~30 for M5)")
    parser.add_argument("--symbol", default="XAUUSDT")
    parser.add_argument("--product-type", default="USDT-FUTURES")
    args = parser.parse_args()

    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[ticker] {args.symbol} — fetching current bid/ask for spread")
    bid, ask = _fetch_ticker_spread(args.symbol, args.product_type)
    spread = round(ask - bid, 6)
    print(f"  bid={bid} ask={ask} spread={spread}")

    for gran_sec, fname in [(300, f"xauusdt_m5_bitget.csv"), (900, f"xauusdt_m15_bitget.csv")]:
        tf = f"M{gran_sec // 60}"
        print(f"[fetch] {args.symbol} {tf} days={args.days}")
        candles = _fetch_all(args.symbol, args.product_type, gran_sec, args.days)
        print(f"  raw candles: {len(candles)}")
        df = _to_dataframe(candles, gran_sec, args.symbol, bid, ask)
        path = out_dir / fname
        df.to_csv(path, index=False)
        if not df.empty:
            print(f"  → {path}  ({len(df)} bars, {df['timestamp'].iloc[0]} → {df['timestamp'].iloc[-1]})")
        else:
            print(f"  → {path}  (0 bars — API returned no data for {args.days}d lookback)")

    print(f"\n[note] Source={SOURCE_TAG}")
    print(f"[note] XAUUSDT futures ≠ XAUUSD spot broker — spread is ticker snapshot, not per-bar historical")
    print(f"[note] Max historical depth ~30 days M5 (Bitget API limit, tested 2026-05-20)")
    print(f"[note] Use for CONTEXT_RECENT_ONLY or improved smoke — not for 180-day backtest verdict")
    return 0


if __name__ == "__main__":
    sys.exit(main())
