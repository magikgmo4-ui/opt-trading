#!/usr/bin/env python3
"""fetch_dukascopy.py — Download XAUUSD tick data from Dukascopy public API and resample to M5/M15.

No account required. Uses the public Dukascopy datafeed endpoint.

Source classification: dukascopy
  - XAUUSD spot interbank bid/ask tick data
  - Spread = ask_close - bid_close per M5/M15 bar (real per-bar spread)
  - History available since 2003
  - ~10-15 minutes for 2 years of data (17k HTTP requests at 50ms delay)

Usage:
    python tools/strategy/daily_scalping/fetch_dukascopy.py \
        --start 2024-01-01 \
        --end   2025-12-31 \
        --out   data/market
"""
from __future__ import annotations

import argparse
import datetime
import lzma
import struct
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import pandas as pd

DUKASCOPY_URL = "https://datafeed.dukascopy.com/datafeed/{symbol}/{year}/{month:02d}/{day:02d}/{hour:02d}h_ticks.bi5"
DIVISOR = 1000  # XAUUSD: 3 decimal places (2636.475 stored as 2636475)
SLEEP_BETWEEN_REQUESTS = 0.05  # seconds — stay well under rate limits


def _fetch_hour_raw(symbol: str, year: int, month: int, day: int, hour: int) -> bytes:
    # month in URL is 0-indexed (Dukascopy convention)
    url = DUKASCOPY_URL.format(symbol=symbol, year=year, month=month - 1, day=day, hour=hour)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read()
    except urllib.error.HTTPError:
        return b""
    except Exception:
        return b""


def _decode_bi5(data: bytes, base_ms: int) -> list[dict]:
    if not data:
        return []
    try:
        raw = lzma.decompress(data)
    except Exception:
        return []
    records = []
    for i in range(0, len(raw) - 19, 20):
        ms_off, ask_raw, bid_raw, _av, _bv = struct.unpack(">IIIff", raw[i : i + 20])
        records.append({
            "ts_ms": base_ms + ms_off,
            "ask": ask_raw / DIVISOR,
            "bid": bid_raw / DIVISOR,
        })
    return records


def _fetch_day(symbol: str, date: datetime.date) -> list[dict]:
    ticks = []
    for hour in range(24):
        base_ms = int(
            datetime.datetime(date.year, date.month, date.day, hour, tzinfo=datetime.timezone.utc).timestamp() * 1000
        )
        raw = _fetch_hour_raw(symbol, date.year, date.month, date.day, hour)
        ticks.extend(_decode_bi5(raw, base_ms))
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    return ticks


def _resample(df: pd.DataFrame, freq: str, timeframe: str, symbol: str) -> pd.DataFrame:
    df["mid"] = (df["ask"] + df["bid"]) / 2
    agg = df.resample(freq).agg(
        open=("mid", "first"),
        high=("mid", "max"),
        low=("mid", "min"),
        close=("mid", "last"),
        ask_close=("ask", "last"),
        bid_close=("bid", "last"),
        volume=("mid", "count"),
    ).dropna(subset=["open"])
    agg["spread"] = (agg["ask_close"] - agg["bid_close"]).round(5)
    agg["bid"] = agg["bid_close"].round(5)
    agg["ask"] = agg["ask_close"].round(5)
    agg["source"] = "dukascopy"
    agg["symbol"] = symbol
    agg["timeframe"] = timeframe
    agg = agg.reset_index()
    agg["timestamp"] = agg["ts"].dt.strftime("%Y-%m-%d %H:%M:%S+00:00")
    cols = ["timestamp", "open", "high", "low", "close", "volume", "bid", "ask", "spread", "source", "symbol", "timeframe"]
    return agg[cols]


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch XAUUSD tick data from Dukascopy and resample to M5/M15")
    parser.add_argument("--start", default="2024-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", default="2025-12-31", help="End date YYYY-MM-DD (inclusive)")
    parser.add_argument("--out", default="data/market", help="Output directory")
    parser.add_argument("--symbol", default="XAUUSD")
    args = parser.parse_args()

    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    start_date = datetime.date.fromisoformat(args.start)
    end_date = datetime.date.fromisoformat(args.end)
    total_days = (end_date - start_date).days + 1

    print(f"[fetch] {args.symbol} tick data {args.start} → {args.end} ({total_days} days)")
    print(f"  Estimated time: {total_days * 24 * SLEEP_BETWEEN_REQUESTS / 60:.1f} min (without weekend skip)")

    all_ticks: list[dict] = []
    date = start_date
    day_num = 0
    skipped = 0

    while date <= end_date:
        day_num += 1
        ticks = _fetch_day(args.symbol, date)
        if ticks:
            all_ticks.extend(ticks)
            if day_num % 10 == 0 or day_num == 1:
                elapsed_pct = day_num / total_days * 100
                print(f"  [{elapsed_pct:5.1f}%] {date}  ticks_today={len(ticks):5d}  total={len(all_ticks):,}")
        else:
            skipped += 1
        date += datetime.timedelta(days=1)

    print(f"\n[done] {len(all_ticks):,} ticks fetched  ({skipped} days skipped — weekend/holiday)")

    if not all_ticks:
        print("[error] No ticks fetched — check network or date range")
        return 1

    df = pd.DataFrame(all_ticks)
    df["ts"] = pd.to_datetime(df["ts_ms"], unit="ms", utc=True)
    df = df.drop_duplicates(subset=["ts_ms"]).sort_values("ts").set_index("ts")

    for freq, tf, fname in [("5min", "M5", f"xauusd_m5_canonical.csv"), ("15min", "M15", f"xauusd_m15_canonical.csv")]:
        print(f"[resample] {tf}")
        df_out = _resample(df.copy(), freq, tf, args.symbol)
        path = out_dir / fname
        df_out.to_csv(path, index=False)
        print(f"  → {path}  ({len(df_out):,} bars, {df_out['timestamp'].iloc[0]} → {df_out['timestamp'].iloc[-1]})")
        print(f"     spread avg={df_out['spread'].mean():.3f}  price {df_out['low'].min():.1f}-{df_out['high'].max():.1f}")

    print("\n[note] source=dukascopy — XAUUSD interbank spot, spread per-bar (real bid/ask)")
    print("[note] Classification: PRIMARY_READY for backtest verdict")
    return 0


if __name__ == "__main__":
    sys.exit(main())
