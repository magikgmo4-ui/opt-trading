#!/usr/bin/env python3
"""run_v2_grid.py — Grid search: tiered-fear DCA + greed sell + CFD long recovery.

Strategies tested (900 valid combos):
  - moderate_fear_thresh : [35, 40, 45]
  - moderate_fear_extra  : [0.75%, 1.0%, 1.25%, 1.5%, 2.0%]  extra on top of 0.2% base
  - extreme_fear_thresh  : [15, 20, 25]
  - extreme_fear_extra   : [10%, 12.5%, 15%, 17.5%, 20%]     extra on top of 0.2% base
  - cfd_entry_thresh     : [20, 25, 30, 35, 40]  (FNG recovery level; must > extreme_thresh)

Fixed:
  - base_weekly_pct  = 0.2%
  - annual_injection = $2,000 / year  (initial capital also $2,000)
  - sell_pct         = 5% of oz on extreme greed (FNG ≥ 76)
  - cfd_lot_oz       = 3 oz (0.03 lots), cfd_sl_atr=1.0, cfd_tp_atr=2.0
  - CFD initial capital = $1,000

Usage:
    python tools/strategy/dca_capital/run_v2_grid.py \\
        --d1-2020 data/market/xauusd_d1_2020_2023.csv \\
        --m5-2024 data/market/xauusd_m5_canonical.csv \\
        --out artifacts/results
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.strategy.dca_capital.fetch_fng import load_fng
from tools.strategy.dca_capital.simulator_v2 import V2Params, V2Result, simulate_v2
from tools.strategy.dca_cfd_short.indicators import add_indicators
from tools.strategy.dca_spot.load_data import load_d1_canonical, load_m5_canonical, resample_to_d1

# ── Grid axes ──────────────────────────────────────────────────────────────
MODERATE_THRESH   = [35, 40, 45]
MODERATE_EXTRA    = [0.0075, 0.010, 0.0125, 0.015, 0.020]   # 0.75%–2.0%
EXTREME_THRESH    = [15, 20, 25]
EXTREME_EXTRA     = [0.10, 0.125, 0.15, 0.175, 0.20]         # 10%–20%
CFD_ENTRY_THRESH  = [20, 25, 30, 35, 40]


def load_data(d1_path: str, m5_path: str) -> pd.DataFrame:
    frames = []
    df_d1 = load_d1_canonical(d1_path)[["open", "high", "low", "close", "volume"]]
    frames.append(df_d1)
    df_m5 = load_m5_canonical(m5_path)
    df_d1b = resample_to_d1(df_m5)[["open", "high", "low", "close", "volume"]]
    frames.append(df_d1b)
    combined = pd.concat(frames).sort_index()
    combined = combined[~combined.index.duplicated(keep="first")]
    return add_indicators(combined)


def baseline(df: pd.DataFrame, fng: pd.DataFrame, last_price: float) -> dict:
    """0.2%/week, no fear extra, no sell, no CFD — pure flat DCA."""
    p = V2Params(
        moderate_fear_extra_pct=0.0,
        extreme_fear_extra_pct=0.0,
        use_cfd=False,
    )
    r = simulate_v2(df, fng, p, label="baseline_0.2pct_weekly")
    return r.summary(last_price)


def run_grid(df: pd.DataFrame, fng: pd.DataFrame, last_price: float) -> pd.DataFrame:
    results = []
    combos = list(itertools.product(
        MODERATE_THRESH, MODERATE_EXTRA,
        EXTREME_THRESH, EXTREME_EXTRA,
        CFD_ENTRY_THRESH,
    ))
    skipped = 0
    for mf_t, mf_p, ef_t, ef_p, cfd_t in combos:
        if cfd_t <= ef_t:          # recovery must be above extreme fear
            skipped += 1
            continue
        p = V2Params(
            moderate_fear_thresh=mf_t,
            moderate_fear_extra_pct=mf_p,
            extreme_fear_thresh=ef_t,
            extreme_fear_extra_pct=ef_p,
            cfd_entry_thresh=cfd_t,
        )
        r = simulate_v2(df, fng, p)
        results.append(r.summary(last_price))

    print(f"  ran {len(results)} combos  ({skipped} skipped — cfd_thresh ≤ ef_thresh)")
    return pd.DataFrame(results).sort_values("return_pct", ascending=False).reset_index(drop=True)


def marginal_effects(df_grid: pd.DataFrame) -> None:
    print("\n── MARGINAL EFFECTS ─────────────────────────────────────────────────")
    for col, name in [
        ("mf_thresh",       "moderate_fear_thresh"),
        ("ef_thresh",       "extreme_fear_thresh"),
        ("mf_extra_pct",    "moderate_fear_extra_pct"),
        ("ef_extra_pct",    "extreme_fear_extra_pct"),
        ("cfd_entry_thresh","cfd_entry_thresh"),
    ]:
        grp = df_grid.groupby(col)["return_pct"].mean().round(2)
        print(f"  {name}:")
        for val, ret in grp.items():
            print(f"    {val:>6} → avg return {ret:+.2f}%")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--d1-2020", required=True)
    parser.add_argument("--m5-2024", required=True)
    parser.add_argument("--out",     required=True)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[load data]")
    df = load_data(args.d1_2020, args.m5_2024)
    last_price = float(df["close"].iloc[-1])
    print(f"  {len(df)} bars  {df.index[0].date()} → {df.index[-1].date()}")
    print(f"  last_price: {last_price:.2f}")

    print("[fetch F&G]")
    fng = load_fng(df)
    print(f"  {fng['source'].value_counts().to_dict()}")

    print("[baseline]")
    bs = baseline(df, fng, last_price)
    print(f"  {bs['label']}: return={bs['return_pct']}%  "
          f"total_return=${bs['total_return_usd']:,.0f}  "
          f"injected=${bs['total_injected_usd']:,.0f}  "
          f"oz={bs['final_oz']}")

    print("[grid search — 900 combos]")
    df_grid = run_grid(df, fng, last_price)

    # ── Top 20 ────────────────────────────────────────────────────────────
    DISPLAY_COLS = [
        "label", "return_pct", "total_return_usd", "total_injected_usd",
        "final_oz", "avg_cost_usd", "gold_value_usd",
        "n_ext_fear_buys", "n_mod_fear_buys", "n_sells",
        "cfd_n_trades", "cfd_win_rate_pct", "cfd_pnl_usd",
    ]
    print(f"\n── TOP 20 COMBOS  (last_price={last_price:.0f}) ─────────────────────────")
    print(df_grid[DISPLAY_COLS].head(20).to_string(index=False))

    # ── Bottom 5 ──────────────────────────────────────────────────────────
    print(f"\n── BOTTOM 5 ─────────────────────────────────────────────────────────")
    print(df_grid[DISPLAY_COLS].tail(5).to_string(index=False))

    # ── Best by sub-group ─────────────────────────────────────────────────
    print(f"\n── BEST PER EXTREME_FEAR_THRESH ─────────────────────────────────────")
    for ef_t in EXTREME_THRESH:
        sub = df_grid[df_grid["ef_thresh"] == ef_t]
        if sub.empty:
            continue
        row = sub.iloc[0]
        print(f"  ef_thresh={ef_t:>2}: return={row['return_pct']:+.2f}%  "
              f"mf={row['mf_thresh']} ef_extra={row['ef_extra_pct']:.1f}%  "
              f"mf_extra={row['mf_extra_pct']:.3f}%  cfd_entry={row['cfd_entry_thresh']}")

    print(f"\n── BEST PER CFD_ENTRY_THRESH ────────────────────────────────────────")
    for cfd_t in CFD_ENTRY_THRESH:
        sub = df_grid[df_grid["cfd_entry_thresh"] == cfd_t]
        if sub.empty:
            continue
        row = sub.iloc[0]
        print(f"  cfd_entry={cfd_t:>2}: return={row['return_pct']:+.2f}%  "
              f"cfd_trades={row['cfd_n_trades']}  wr={row['cfd_win_rate_pct']}%  "
              f"pnl=${row['cfd_pnl_usd']:.0f}")

    # ── Marginal effects ──────────────────────────────────────────────────
    marginal_effects(df_grid)

    # ── Baseline comparison ───────────────────────────────────────────────
    best = df_grid.iloc[0]
    print(f"\n── BASELINE vs BEST ─────────────────────────────────────────────────")
    print(f"  baseline  : return={bs['return_pct']:+.2f}%  "
          f"total_return=${bs['total_return_usd']:,.0f}  oz={bs['final_oz']}")
    print(f"  best_combo: return={best['return_pct']:+.2f}%  "
          f"total_return=${best['total_return_usd']:,.0f}  oz={best['final_oz']}")
    print(f"  delta     : {best['return_pct'] - bs['return_pct']:+.2f}%  "
          f"${best['total_return_usd'] - bs['total_return_usd']:+,.0f}")

    # ── Save ──────────────────────────────────────────────────────────────
    df_grid.to_csv(out_dir / "dca_v2_grid.csv", index=False)
    df_grid.head(50).to_csv(out_dir / "dca_v2_top50.csv", index=False)
    pd.DataFrame([bs]).to_csv(out_dir / "dca_v2_baseline.csv", index=False)
    print(f"\n[out] {out_dir}/dca_v2_grid.csv  ({len(df_grid)} rows)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
