#!/usr/bin/env python3
"""normalize_mt5.py — Normalize MT5 History Center CSV export to XAUUSD_M5_CANONICAL.

Usage:
    python tools/strategy/daily_scalping/normalize_mt5.py \
        --input data/market/raw/xauusd_m5_raw_mt5.csv \
        --output data/market/xauusd_m5_canonical.csv \
        --timeframe M5 \
        --broker-tz UTC+2

MT5 export format (tab or comma separated):
    <DATE>\t<TIME>\t<OPEN>\t<HIGH>\t<LOW>\t<CLOSE>\t<TICKVOL>\t<VOL>\t<SPREAD>
    2024.01.02\t08:00\t2063.50\t2065.10\t2062.80\t2064.30\t1250\t0\t15
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import pandas as pd

POINT_SIZE = 0.01  # XAUUSD: 1 point = 0.01 USD


def _parse_broker_tz(tz_str: str):
    """Parse 'UTC+2' or 'UTC-3' into a pandas-compatible timezone."""
    tz_str = tz_str.strip().upper()
    if tz_str.startswith("UTC+") or tz_str.startswith("UTC-"):
        hours = int(tz_str[3:])
        return f"Etc/GMT{-hours:+d}"  # Note: POSIX sign is inverted
    return tz_str


def load_mt5_csv(path: Path) -> pd.DataFrame:
    raw = path.read_text(encoding="utf-8", errors="replace")
    # Detect separator: tab or comma
    sep = "\t" if "\t" in raw.split("\n")[0] else ","
    df = pd.read_csv(path, sep=sep, encoding="utf-8", errors="replace")

    # Normalize column names (strip angle brackets and whitespace)
    df.columns = [c.strip().strip("<>").upper() for c in df.columns]

    # Expected columns after strip: DATE, TIME, OPEN, HIGH, LOW, CLOSE, TICKVOL, VOL, SPREAD
    return df


def normalize(df: pd.DataFrame, timeframe: str, broker_tz: str) -> pd.DataFrame:
    tz = _parse_broker_tz(broker_tz)

    # Build timestamp from DATE + TIME
    dt_str = df["DATE"].astype(str) + " " + df["TIME"].astype(str)
    timestamps = pd.to_datetime(dt_str, format="%Y.%m.%d %H:%M")
    timestamps = timestamps.dt.tz_localize(tz).dt.tz_convert("UTC")

    spread_usd = df["SPREAD"].astype(float) * POINT_SIZE

    out = pd.DataFrame({
        "timestamp": timestamps.dt.strftime("%Y-%m-%d %H:%M:%S+00:00"),
        "open": df["OPEN"].astype(float),
        "high": df["HIGH"].astype(float),
        "low": df["LOW"].astype(float),
        "close": df["CLOSE"].astype(float),
        "volume": df["TICKVOL"].astype(int),
        "bid": (df["CLOSE"].astype(float) - spread_usd / 2).round(5),
        "ask": (df["CLOSE"].astype(float) + spread_usd / 2).round(5),
        "spread": spread_usd.round(5),
        "source": "mt5_export",
        "symbol": "XAUUSD",
        "timeframe": timeframe,
    })

    out = out.drop_duplicates(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    return out


def validate(df: pd.DataFrame) -> None:
    required = ["timestamp", "open", "high", "low", "close", "volume", "bid", "ask", "spread", "source", "symbol", "timeframe"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes: {missing}")
    assert (df["spread"] >= 0).all(), "spread négatif"
    assert (df["ask"] >= df["bid"]).all(), "ask < bid"
    assert (df["high"] >= df["low"]).all(), "high < low"
    n = len(df)
    print(f"  validation OK — {n:,} barres, {df['timestamp'].iloc[0]} → {df['timestamp'].iloc[-1]}")
    if n < 50_000:
        print(f"  WARN: {n} barres < 50 000 minimum recommandé pour 180j M5")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize MT5 CSV export to canonical XAUUSD format")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--timeframe", default="M5", choices=["M5", "M15", "M1", "M30", "H1"])
    parser.add_argument("--broker-tz", default="UTC+2", help="MT5 server timezone (e.g. UTC+2, UTC+3)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[load] {input_path}")
    df_raw = load_mt5_csv(input_path)
    print(f"  raw rows: {len(df_raw):,} | cols: {list(df_raw.columns)}")

    print(f"[normalize] broker-tz={args.broker_tz} → UTC, timeframe={args.timeframe}")
    df_out = normalize(df_raw, args.timeframe, args.broker_tz)

    print("[validate]")
    validate(df_out)

    df_out.to_csv(output_path, index=False)
    print(f"[save] → {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
