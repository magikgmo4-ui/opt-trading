"""load_data.py — Load M5 canonical CSV and resample to D1."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_m5_canonical(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("timestamp").set_index("timestamp")
    for col in ("open", "high", "low", "close"):
        df[col] = df[col].astype(float)
    if "volume" not in df.columns:
        df["volume"] = 0.0
    return df


def resample_to_d1(df_m5: pd.DataFrame) -> pd.DataFrame:
    d1 = df_m5.resample("D").agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        volume=("volume", "sum"),
    )
    return d1.dropna(subset=["open"])
