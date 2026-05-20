"""detectors.py — ORB, sweep, BOS/CHOCH proxy, VWAP retest setup detection."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

import pandas as pd


@dataclass
class Setup:
    index: pd.Timestamp
    variant: str
    direction: str          # "long" | "short"
    setup_type: str
    entry_bar: int
    orb_state: str = ""
    vwap_state: str = ""
    liquidity_state: str = ""
    structure_state: str = ""
    entry_price: float = 0.0
    atr: float = 0.0
    vwap: float = 0.0
    orb_high: float = float("nan")
    orb_low: float = float("nan")
    session: str = ""
    extra: dict = field(default_factory=dict)


def _last_swing_low(df: pd.DataFrame, before: int, lookback: int = 20) -> Optional[float]:
    start = max(0, before - lookback)
    sub = df.iloc[start:before]
    lows = sub.loc[sub["swing_low"], "low"]
    return float(lows.iloc[-1]) if len(lows) else None


def _last_swing_high(df: pd.DataFrame, before: int, lookback: int = 20) -> Optional[float]:
    start = max(0, before - lookback)
    sub = df.iloc[start:before]
    highs = sub.loc[sub["swing_high"], "high"]
    return float(highs.iloc[-1]) if len(highs) else None


def detect_orb_only(df: pd.DataFrame) -> List[Setup]:
    setups = []
    for i in range(1, len(df)):
        row = df.iloc[i]
        if not row.get("orb_complete", False):
            continue
        orb_h, orb_l = row["orb_high"], row["orb_low"]
        prev = df.iloc[i - 1]
        # Breakout long: close crosses above ORB high
        if prev["close"] <= orb_h and row["close"] > orb_h:
            setups.append(Setup(
                index=df.index[i], variant="ORB_ONLY", direction="long",
                setup_type="ORB_BREAKOUT", entry_bar=i,
                orb_state="breakout_long", session=row["session"],
                entry_price=row["close"], atr=row.get("atr", 0.0),
                orb_high=orb_h, orb_low=orb_l,
            ))
        # Breakout short: close crosses below ORB low
        elif prev["close"] >= orb_l and row["close"] < orb_l:
            setups.append(Setup(
                index=df.index[i], variant="ORB_ONLY", direction="short",
                setup_type="ORB_BREAKOUT", entry_bar=i,
                orb_state="breakout_short", session=row["session"],
                entry_price=row["close"], atr=row.get("atr", 0.0),
                orb_high=orb_h, orb_low=orb_l,
            ))
    return setups


def detect_vwap_pullback_only(df: pd.DataFrame) -> List[Setup]:
    setups = []
    for i in range(2, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]
        vwap = row.get("vwap", float("nan"))
        if pd.isna(vwap):
            continue
        # VWAP pullback long: price above VWAP, dipped to VWAP, closed back above
        if prev["low"] <= vwap and row["close"] > vwap and df.iloc[i - 2]["close"] > vwap:
            setups.append(Setup(
                index=df.index[i], variant="VWAP_PULLBACK_ONLY", direction="long",
                setup_type="VWAP_RETEST", entry_bar=i,
                vwap_state="retest_long", session=row["session"],
                entry_price=row["close"], atr=row.get("atr", 0.0), vwap=vwap,
            ))
        # VWAP pullback short: price below VWAP, rallied to VWAP, closed back below
        elif prev["high"] >= vwap and row["close"] < vwap and df.iloc[i - 2]["close"] < vwap:
            setups.append(Setup(
                index=df.index[i], variant="VWAP_PULLBACK_ONLY", direction="short",
                setup_type="VWAP_RETEST", entry_bar=i,
                vwap_state="retest_short", session=row["session"],
                entry_price=row["close"], atr=row.get("atr", 0.0), vwap=vwap,
            ))
    return setups


def detect_smc_sweep_only(df: pd.DataFrame, lookback: int = 20) -> List[Setup]:
    setups = []
    for i in range(lookback + 2, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]
        # Sweep low + CHOCH long proxy
        swing_l = _last_swing_low(df, i, lookback)
        swing_h = _last_swing_high(df, i, lookback)
        if swing_l is not None:
            swept = prev["low"] < swing_l and row["close"] > swing_l
            if swept and swing_h is not None and row["close"] > swing_h:
                setups.append(Setup(
                    index=df.index[i], variant="SMC_SWEEP_ONLY", direction="long",
                    setup_type="SWEEP_CHOCH", entry_bar=i,
                    liquidity_state="sweep_low", structure_state="choch_long",
                    session=row["session"], entry_price=row["close"],
                    atr=row.get("atr", 0.0),
                ))
        # Sweep high + CHOCH short proxy
        if swing_h is not None:
            swept = prev["high"] > swing_h and row["close"] < swing_h
            if swept and swing_l is not None and row["close"] < swing_l:
                setups.append(Setup(
                    index=df.index[i], variant="SMC_SWEEP_ONLY", direction="short",
                    setup_type="SWEEP_CHOCH", entry_bar=i,
                    liquidity_state="sweep_high", structure_state="choch_short",
                    session=row["session"], entry_price=row["close"],
                    atr=row.get("atr", 0.0),
                ))
    return setups


def detect_combined(df: pd.DataFrame, lookback: int = 20) -> List[Setup]:
    """COMBINED: requires ORB + VWAP alignment + SMC sweep/CHOCH."""
    setups = []
    for i in range(lookback + 2, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]
        vwap = row.get("vwap", float("nan"))
        orb_h = row.get("orb_high", float("nan"))
        orb_l = row.get("orb_low", float("nan"))
        if pd.isna(vwap) or not row.get("orb_complete", False):
            continue
        swing_l = _last_swing_low(df, i, lookback)
        swing_h = _last_swing_high(df, i, lookback)

        # Combined long: sweep low + CHOCH + ORB support + VWAP bull
        if swing_l is not None and swing_h is not None:
            sweep_long = prev["low"] < swing_l and row["close"] > swing_l
            choch_long = row["close"] > swing_h
            vwap_bull = row["close"] > vwap
            orb_support = not pd.isna(orb_l) and row["close"] > orb_l
            if sweep_long and choch_long and vwap_bull and orb_support:
                setups.append(Setup(
                    index=df.index[i], variant="COMBINED_SMC_ORB_VWAP", direction="long",
                    setup_type="COMBINED_LONG", entry_bar=i,
                    liquidity_state="sweep_low", structure_state="choch_long",
                    vwap_state="bull", orb_state="above_orb_low",
                    session=row["session"], entry_price=row["close"],
                    atr=row.get("atr", 0.0), vwap=vwap,
                    orb_high=orb_h, orb_low=orb_l,
                ))

        # Combined short: sweep high + CHOCH + ORB resistance + VWAP bear
        if swing_h is not None and swing_l is not None:
            sweep_short = prev["high"] > swing_h and row["close"] < swing_h
            choch_short = row["close"] < swing_l
            vwap_bear = row["close"] < vwap
            orb_resist = not pd.isna(orb_h) and row["close"] < orb_h
            if sweep_short and choch_short and vwap_bear and orb_resist:
                setups.append(Setup(
                    index=df.index[i], variant="COMBINED_SMC_ORB_VWAP", direction="short",
                    setup_type="COMBINED_SHORT", entry_bar=i,
                    liquidity_state="sweep_high", structure_state="choch_short",
                    vwap_state="bear", orb_state="below_orb_high",
                    session=row["session"], entry_price=row["close"],
                    atr=row.get("atr", 0.0), vwap=vwap,
                    orb_high=orb_h, orb_low=orb_l,
                ))
    return setups


_VARIANT_DETECTORS = {
    "ORB_ONLY": detect_orb_only,
    "VWAP_PULLBACK_ONLY": detect_vwap_pullback_only,
    "SMC_SWEEP_ONLY": detect_smc_sweep_only,
    "COMBINED_SMC_ORB_VWAP": detect_combined,
}


def detect_all(df: pd.DataFrame, variants: List[str]) -> List[Setup]:
    all_setups = []
    for variant in variants:
        fn = _VARIANT_DETECTORS.get(variant)
        if fn:
            all_setups.extend(fn(df))
    return all_setups
