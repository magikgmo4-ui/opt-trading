#!/usr/bin/env python3
"""run_backtest.py — DCA spot tiered backtest vs simple weekly benchmark.

Usage:
    python tools/strategy/dca_spot/run_backtest.py \
        --input data/market/xauusd_m5_canonical.csv \
        --out artifacts/backtests/dca_spot
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.strategy.dca_spot.load_data import load_m5_canonical, load_d1_canonical, resample_to_d1
from tools.strategy.dca_spot.indicators import add_indicators
from tools.strategy.dca_spot.engine import DCAConfig, run_simulation


def benchmark_simple_weekly(df: pd.DataFrame) -> dict:
    """Baseline: buy 1S every week at Monday (first D1 bar) open."""
    iso = df.index.isocalendar()
    df2 = df.assign(
        _wk=(iso["year"].astype(str) + "_" + iso["week"].astype(str).str.zfill(2)).values
    )
    buys = []
    for _, group in df2.groupby("_wk", sort=True):
        bar = group.iloc[0]
        buys.append(bar["open"])

    if not buys:
        return {}
    avg = sum(buys) / len(buys)
    last = float(df["close"].iloc[-1])
    return {
        "n_buys": len(buys),
        "avg_price": round(avg, 2),
        "total_return_pct": round((last - avg) / avg * 100, 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="M5 canonical CSV or D1 canonical CSV (--d1 flag)")
    parser.add_argument("--d1", action="store_true", help="Input is already D1 (skip resample)")
    parser.add_argument("--out", required=True)
    parser.add_argument("--ref-type", default="w2_close")
    parser.add_argument("--corr-medium", type=float, default=-8.0)
    parser.add_argument("--corr-large", type=float, default=-20.0)
    parser.add_argument("--mult-medium", type=float, default=3.0)
    parser.add_argument("--mult-large", type=float, default=10.0)
    parser.add_argument("--sell-mode", default="price_or_spike")
    parser.add_argument("--spike-k", type=float, default=2.0)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[load] {args.input}")
    if args.d1:
        df_d1 = load_d1_canonical(args.input)
        print(f"  → {len(df_d1)} D1 bars  {df_d1.index[0].date()} → {df_d1.index[-1].date()}")
    else:
        df_m5 = load_m5_canonical(args.input)
        print("[resample] M5 → D1")
        df_d1 = resample_to_d1(df_m5)
        print(f"  → {len(df_d1)} D1 bars  {df_d1.index[0].date()} → {df_d1.index[-1].date()}")
    print("[indicators]")
    df_d1 = add_indicators(df_d1)

    cfg = DCAConfig(
        ref_type=args.ref_type,
        corr_medium_pct=args.corr_medium,
        corr_large_pct=args.corr_large,
        mult_medium=args.mult_medium,
        mult_large=args.mult_large,
        sell_mode=args.sell_mode,
        spike_k=args.spike_k,
    )

    print("[simulate] tiered DCA")
    engine, summary = run_simulation(df_d1, cfg)

    print("[simulate] benchmark (simple weekly)")
    bench = benchmark_simple_weekly(df_d1)

    last_price = float(df_d1["close"].iloc[-1])

    print("\n── TIERED DCA ────────────────────────────────────────────────────────")
    for k, v in summary.items():
        print(f"  {k:25s} {v}")

    print("\n── BENCHMARK (simple weekly) ─────────────────────────────────────────")
    for k, v in bench.items():
        print(f"  {k:25s} {v}")

    # Delta
    if "avg_price_all" in summary and "avg_price" in bench:
        delta = summary["avg_price_all"] - bench["avg_price"]
        print(f"\n  avg_price delta (tiered vs bench) : {delta:+.2f} pts"
              f"  ({'cheaper' if delta < 0 else 'more expensive'})")
        ret_delta = summary["total_return_pct"] - bench["total_return_pct"]
        print(f"  total_return delta                : {ret_delta:+.2f}%")

    # Event log CSV
    events_df = pd.DataFrame([
        {
            "date": e.date.date(),
            "type": e.event_type,
            "price": round(e.price, 2),
            "qty_s": e.qty_s,
            "trigger": e.trigger,
            "l0_after": round(e.l0_after, 2),
            "n_l1": e.n_l1, "n_l2": e.n_l2, "n_l3": e.n_l3,
        }
        for e in engine.events
    ])
    log_path = out_dir / "dca_spot_events.csv"
    events_df.to_csv(log_path, index=False)
    print(f"\n[out] {log_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
