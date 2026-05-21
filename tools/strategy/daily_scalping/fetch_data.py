#!/usr/bin/env python3
"""fetch_data.py — Download XAUUSD (GC=F) M5/M15 OHLCV from Yahoo Finance.

Usage:
    python tools/strategy/daily_scalping/fetch_data.py \
        --out data/market \
        --period 60d
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import pandas as pd
import yfinance as yf


_TICKER = "GC=F"  # Gold futures — closest liquid proxy for XAUUSD


def _fetch(ticker: str, period: str, interval: str) -> pd.DataFrame:
    raw = yf.Ticker(ticker).history(period=period, interval=interval)
    raw.index = raw.index.tz_convert("UTC")
    raw.index.name = "timestamp"
    df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.columns = ["open", "high", "low", "close", "volume"]
    df = df[df["close"] > 0].copy()
    return df


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch XAUUSD M5/M15 OHLCV")
    parser.add_argument("--out", default="data/market", help="Output directory")
    parser.add_argument("--period", default="60d", help="yfinance period (max 60d for intraday)")
    parser.add_argument("--ticker", default=_TICKER)
    args = parser.parse_args()

    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    for interval, fname in [("5m", "xauusd_m5.csv"), ("15m", "xauusd_m15.csv")]:
        print(f"[fetch] {args.ticker} {interval} period={args.period}")
        df = _fetch(args.ticker, args.period, interval)
        path = out_dir / fname
        df.to_csv(path)
        print(f"  → {path}  ({len(df)} bars, {df.index.min().date()} → {df.index.max().date()})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
