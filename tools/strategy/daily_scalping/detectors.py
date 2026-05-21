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


def detect_smc_sweep_only(df: pd.DataFrame, lookback: int = 20, confirm_window: int = 5) -> List[Setup]:
    setups = []
    n = len(df)
    for i in range(lookback + 2, n):
        prev = df.iloc[i - 1]
        row = df.iloc[i]
        swing_l = _last_swing_low(df, i, lookback)
        swing_h = _last_swing_high(df, i, lookback)

        # Sweep low: prev bar wicks below swing_l, current bar closes back above
        if swing_l is not None and prev["low"] < swing_l and row["close"] > swing_l:
            if swing_h is not None:
                # CHOCH long: first bar in [i, i+confirm_window] that closes above swing_h
                for k in range(confirm_window + 1):
                    j = i + k
                    if j >= n:
                        break
                    if df.iloc[j]["close"] > swing_h:
                        choch_bar = df.iloc[j]
                        setups.append(Setup(
                            index=df.index[j], variant="SMC_SWEEP_ONLY", direction="long",
                            setup_type="SWEEP_CHOCH", entry_bar=j,
                            liquidity_state="sweep_low", structure_state="choch_long",
                            session=choch_bar["session"], entry_price=choch_bar["close"],
                            atr=choch_bar.get("atr", 0.0),
                            extra={"sweep_extreme": prev["low"]},
                        ))
                        break

        # Sweep high: prev bar wicks above swing_h, current bar closes back below
        if swing_h is not None and prev["high"] > swing_h and row["close"] < swing_h:
            if swing_l is not None:
                # CHOCH short: first bar in [i, i+confirm_window] that closes below swing_l
                for k in range(confirm_window + 1):
                    j = i + k
                    if j >= n:
                        break
                    if df.iloc[j]["close"] < swing_l:
                        choch_bar = df.iloc[j]
                        setups.append(Setup(
                            index=df.index[j], variant="SMC_SWEEP_ONLY", direction="short",
                            setup_type="SWEEP_CHOCH", entry_bar=j,
                            liquidity_state="sweep_high", structure_state="choch_short",
                            session=choch_bar["session"], entry_price=choch_bar["close"],
                            atr=choch_bar.get("atr", 0.0),
                            extra={"sweep_extreme": prev["high"]},
                        ))
                        break

    return setups


def detect_combined(df: pd.DataFrame, lookback: int = 20, confirm_window: int = 5) -> List[Setup]:
    """COMBINED: requires ORB + VWAP alignment + SMC sweep/CHOCH (multi-bar confirmation)."""
    setups = []
    n = len(df)
    for i in range(lookback + 2, n):
        prev = df.iloc[i - 1]
        row = df.iloc[i]
        swing_l = _last_swing_low(df, i, lookback)
        swing_h = _last_swing_high(df, i, lookback)

        # Combined long: sweep low detected, then search for CHOCH + ORB/VWAP confluence
        if swing_l is not None and swing_h is not None:
            if prev["low"] < swing_l and row["close"] > swing_l:
                for k in range(confirm_window + 1):
                    j = i + k
                    if j >= n:
                        break
                    cbar = df.iloc[j]
                    vwap = cbar.get("vwap", float("nan"))
                    orb_h = cbar.get("orb_high", float("nan"))
                    orb_l = cbar.get("orb_low", float("nan"))
                    if pd.isna(vwap) or not cbar.get("orb_complete", False):
                        continue
                    if (cbar["close"] > swing_h
                            and cbar["close"] > vwap
                            and not pd.isna(orb_l) and cbar["close"] > orb_l):
                        setups.append(Setup(
                            index=df.index[j], variant="COMBINED_SMC_ORB_VWAP", direction="long",
                            setup_type="COMBINED_LONG", entry_bar=j,
                            liquidity_state="sweep_low", structure_state="choch_long",
                            vwap_state="bull", orb_state="above_orb_low",
                            session=cbar["session"], entry_price=cbar["close"],
                            atr=cbar.get("atr", 0.0), vwap=vwap,
                            orb_high=orb_h, orb_low=orb_l,
                            extra={"sweep_extreme": prev["low"]},
                        ))
                        break

        # Combined short: sweep high detected, then search for CHOCH + ORB/VWAP confluence
        if swing_h is not None and swing_l is not None:
            if prev["high"] > swing_h and row["close"] < swing_h:
                for k in range(confirm_window + 1):
                    j = i + k
                    if j >= n:
                        break
                    cbar = df.iloc[j]
                    vwap = cbar.get("vwap", float("nan"))
                    orb_h = cbar.get("orb_high", float("nan"))
                    orb_l = cbar.get("orb_low", float("nan"))
                    if pd.isna(vwap) or not cbar.get("orb_complete", False):
                        continue
                    if (cbar["close"] < swing_l
                            and cbar["close"] < vwap
                            and not pd.isna(orb_h) and cbar["close"] < orb_h):
                        setups.append(Setup(
                            index=df.index[j], variant="COMBINED_SMC_ORB_VWAP", direction="short",
                            setup_type="COMBINED_SHORT", entry_bar=j,
                            liquidity_state="sweep_high", structure_state="choch_short",
                            vwap_state="bear", orb_state="below_orb_high",
                            session=cbar["session"], entry_price=cbar["close"],
                            atr=cbar.get("atr", 0.0), vwap=vwap,
                            orb_high=orb_h, orb_low=orb_l,
                            extra={"sweep_extreme": prev["high"]},
                        ))
                        break

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
