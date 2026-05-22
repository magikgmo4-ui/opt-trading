"""fetch_fng.py — Fetch Fear & Greed Index (Alternative.me) + synthetic gap fill.

Alternative.me covers 2020-05-12 → today (crypto sentiment).
Gap 2020-01-02 → 2020-05-11: synthetic FNG from D1 price indicators
  synthetic = 0.5 × RSI14 + 0.5 × position_in_13w_range (0–100)
  Calibrated so COVID crash (Mar 2020) maps to 10–20 (Extreme Fear).
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone

import pandas as pd


FNG_URL = "https://api.alternative.me/fng/?limit=2200&format=json"

THRESHOLDS = {
    "extreme_fear":  (0,  25),
    "fear":          (25, 46),
    "neutral":       (46, 55),
    "greed":         (55, 76),
    "extreme_greed": (76, 101),
}


def fetch_fng_raw() -> pd.DataFrame:
    req = urllib.request.Request(FNG_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    records = data["data"]
    rows = []
    for rec in records:
        ts = datetime.fromtimestamp(int(rec["timestamp"]), tz=timezone.utc)
        rows.append({"date": ts.date(), "fng": int(rec["value"]),
                     "fng_label": rec["value_classification"],
                     "source": "alternative_me"})
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], utc=True)
    return df.sort_values("date").reset_index(drop=True)


def synthetic_fng(df_d1: pd.DataFrame) -> pd.DataFrame:
    """Build synthetic FNG from RSI14 + 13-week range position."""
    from tools.strategy.dca_cfd_short.indicators import rsi as compute_rsi
    rsi_s = compute_rsi(df_d1["close"], 14)
    high13 = df_d1["high"].rolling(65, min_periods=10).max()
    low13  = df_d1["low"].rolling(65,  min_periods=10).min()
    rng    = (high13 - low13).replace(0, float("nan"))
    pos    = ((df_d1["close"] - low13) / rng * 100).clip(0, 100)
    synth  = (0.5 * rsi_s + 0.5 * pos).clip(0, 100).round(0).astype("Int64")

    rows = []
    for ts, val in synth.items():
        if pd.isna(val):
            continue
        label = classify(int(val))
        rows.append({"date": ts, "fng": int(val), "fng_label": label,
                     "source": "synthetic_price"})
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def classify(val: int) -> str:
    for label, (lo, hi) in THRESHOLDS.items():
        if lo <= val < hi:
            return label.replace("_", " ").title()
    return "Neutral"


def load_fng(df_d1: pd.DataFrame) -> pd.DataFrame:
    """Return daily FNG series aligned to df_d1 index.
    Alternative.me for 2020-05-12+, synthetic price-based before.
    """
    real = fetch_fng_raw()
    synth = synthetic_fng(df_d1)

    cutoff = real["date"].min()
    pre = synth[synth["date"] < cutoff].copy()

    combined = pd.concat([pre, real], ignore_index=True)
    combined = combined.sort_values("date").drop_duplicates("date")
    combined = combined.set_index("date")
    combined.index = pd.to_datetime(combined.index, utc=True)

    # Align to D1 index
    df_d1_dates = df_d1.index.normalize()
    aligned = combined.reindex(df_d1_dates, method="ffill")
    aligned.index = df_d1.index
    return aligned[["fng", "fng_label", "source"]]
