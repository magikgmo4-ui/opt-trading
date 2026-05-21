"""load_data.py — Load canonical CSVs and resample to D1."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def _load_canonical(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("timestamp").set_index("timestamp")
    for col in ("open", "high", "low", "close"):
        df[col] = df[col].astype(float)
    if "volume" not in df.columns:
        df["volume"] = 0.0
    return df


def load_m5_canonical(path: str | Path) -> pd.DataFrame:
    return _load_canonical(path)


def load_d1_canonical(path: str | Path) -> pd.DataFrame:
    """Load a D1 canonical CSV (produced by fetch_d1_dukascopy.py). No resample needed."""
    return _load_canonical(path)


def resample_to_d1(df_m5: pd.DataFrame) -> pd.DataFrame:
    d1 = df_m5.resample("D").agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        volume=("volume", "sum"),
    )
    return d1.dropna(subset=["open"])
