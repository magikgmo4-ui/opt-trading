#!/usr/bin/env python3
"""normalize_dukascopy.py — Resample Dukascopy XAUUSD tick CSV to canonical M5/M15.

Usage:
    python tools/strategy/daily_scalping/normalize_dukascopy.py \
        --input data/market/raw/xauusd_tick_2024.csv data/market/raw/xauusd_tick_2025.csv \
        --output-m5 data/market/xauusd_m5_canonical.csv \
        --output-m15 data/market/xauusd_m15_canonical.csv

Dukascopy tick CSV format:
    Timestamp,Ask,Bid,AskVolume,BidVolume
    01.01.2024 00:00:00.123,2062.500,2062.400,1.0,1.0
    Timezone: UTC
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import pandas as pd


def load_tick_csv(paths: list[Path]) -> pd.DataFrame:
    frames = []
    for path in paths:
        print(f"  [load] {path}")
        df = pd.read_csv(path)
        df.columns = [c.strip() for c in df.columns]
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)

    # Parse timestamp — format: DD.MM.YYYY HH:MM:SS.mmm UTC
    df["ts"] = pd.to_datetime(df["Timestamp"], format="%d.%m.%Y %H:%M:%S.%f", utc=True)
    df = df.sort_values("ts").drop_duplicates(subset=["ts"]).reset_index(drop=True)
    df["mid"] = (df["Ask"] + df["Bid"]) / 2
    df["spread_pt"] = (df["Ask"] - df["Bid"]).clip(lower=0)
    df = df.set_index("ts")
    return df


def resample_ohlcv(df: pd.DataFrame, freq: str, timeframe: str) -> pd.DataFrame:
    agg = df.resample(freq).agg(
        open=("mid", "first"),
        high=("mid", "max"),
        low=("mid", "min"),
        close=("mid", "last"),
        volume=("AskVolume", "sum"),
        spread=("spread_pt", "mean"),
    ).dropna(subset=["open"])

    agg["bid"] = (agg["close"] - agg["spread"] / 2).round(5)
    agg["ask"] = (agg["close"] + agg["spread"] / 2).round(5)
    agg["spread"] = agg["spread"].round(5)
    agg["source"] = "dukascopy"
    agg["symbol"] = "XAUUSD"
    agg["timeframe"] = timeframe

    agg = agg.reset_index()
    agg["timestamp"] = agg["ts"].dt.strftime("%Y-%m-%d %H:%M:%S+00:00")
    cols = ["timestamp", "open", "high", "low", "close", "volume", "bid", "ask", "spread", "source", "symbol", "timeframe"]
    return agg[cols]


def validate(df: pd.DataFrame, label: str) -> None:
    required = ["timestamp", "open", "high", "low", "close", "volume", "bid", "ask", "spread", "source", "symbol", "timeframe"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{label} — Colonnes manquantes: {missing}")
    n = len(df)
    print(f"  {label}: {n:,} barres, {df['timestamp'].iloc[0]} → {df['timestamp'].iloc[-1]}")
    if n < 50_000:
        print(f"  WARN [{label}]: {n} barres < 50 000 recommandé pour 180j")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize Dukascopy tick data to canonical XAUUSD M5/M15")
    parser.add_argument("--input", nargs="+", required=True, help="Dukascopy tick CSV file(s)")
    parser.add_argument("--output-m5", required=True)
    parser.add_argument("--output-m15", required=True)
    args = parser.parse_args()

    input_paths = [Path(p) for p in args.input]
    out_m5 = Path(args.output_m5)
    out_m15 = Path(args.output_m15)
    out_m5.parent.mkdir(parents=True, exist_ok=True)
    out_m15.parent.mkdir(parents=True, exist_ok=True)

    print(f"[load] {len(input_paths)} tick file(s)")
    df_tick = load_tick_csv(input_paths)
    print(f"  total ticks: {len(df_tick):,}")

    print("[resample] M5")
    df_m5 = resample_ohlcv(df_tick, "5min", "M5")
    validate(df_m5, "M5")
    df_m5.to_csv(out_m5, index=False)
    print(f"  → {out_m5}")

    print("[resample] M15")
    df_m15 = resample_ohlcv(df_tick, "15min", "M15")
    validate(df_m15, "M15")
    df_m15.to_csv(out_m15, index=False)
    print(f"  → {out_m15}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
