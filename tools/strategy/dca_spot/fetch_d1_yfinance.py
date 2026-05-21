#!/usr/bin/env python3
"""fetch_d1_yfinance.py — Download XAUUSD-equivalent D1 bars via yfinance (GC=F).

Uses GC=F (COMEX Gold front-month futures) as proxy for XAUUSD spot.
Absolute basis difference: ~$5-10 (contango). Percentage corrections: identical.
Adequate for DCA spot strategy which measures relative corrections only.

NOT adequate for: spread-sensitive strategies, exact entry price, scalping.

Output: D1 canonical CSV — same column format as M5 canonical (timeframe=D1).
Fetch time: seconds (single HTTP call via yfinance).

Usage:
    python tools/strategy/dca_spot/fetch_d1_yfinance.py \
        --start 2020-01-01 \
        --end   2023-12-31 \
        --out   data/market/xauusd_d1_2020_2023.csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import pandas as pd
import yfinance as yf

TICKER = "GC=F"
COLUMNS = ["timestamp", "open", "high", "low", "close", "volume",
           "bid", "ask", "spread", "source", "symbol", "timeframe"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start",  default="2020-01-01")
    parser.add_argument("--end",    default="2023-12-31")
    parser.add_argument("--out",    required=True)
    parser.add_argument("--ticker", default=TICKER)
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[fetch] {args.ticker} D1  {args.start} → {args.end}")
    print(f"  source : yfinance (GC=F gold futures — OHLC proxy for XAUUSD spot)")
    print(f"  note   : spread=N/A; basis ~$5-10; % corrections identical to spot")

    end_inclusive = (pd.Timestamp(args.end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    df = yf.download(args.ticker, start=args.start, end=end_inclusive,
                     interval="1d", auto_adjust=True, progress=False)

    if df.empty:
        print("[error] No data returned")
        return 1

    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0].lower() for c in df.columns]
    else:
        df.columns = [c.lower() for c in df.columns]

    df = df.sort_index()
    df.index = pd.to_datetime(df.index, utc=True)

    rows = []
    for ts, row in df.iterrows():
        rows.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S+00:00"),
            "open":      round(float(row["open"]),   3),
            "high":      round(float(row["high"]),   3),
            "low":       round(float(row["low"]),    3),
            "close":     round(float(row["close"]),  3),
            "volume":    int(row.get("volume", 0)),
            "bid":       None,
            "ask":       None,
            "spread":    None,
            "source":    "yfinance_gcf",
            "symbol":    "XAUUSD",
            "timeframe": "D1",
        })

    out_df = pd.DataFrame(rows, columns=COLUMNS)
    out_df.to_csv(out_path, index=False)

    print(f"\n[done] {len(out_df)} D1 bars")
    print(f"  range  : {out_df['timestamp'].iloc[0]} → {out_df['timestamp'].iloc[-1]}")
    print(f"  price  : {out_df['low'].min():.1f} – {out_df['high'].max():.1f}")
    print(f"  output : {out_path}  ({out_path.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
