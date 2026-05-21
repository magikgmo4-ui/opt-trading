#!/usr/bin/env python3
"""run_optimization.py — Grid search for tiered DCA spot strategy.

216 combinations. Reports only configs clearly beating benchmark.

Usage:
    python tools/strategy/dca_spot/run_optimization.py \
        --input data/market/xauusd_m5_canonical.csv \
        --out artifacts/backtests/dca_spot
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.strategy.dca_spot.load_data import load_m5_canonical, resample_to_d1
from tools.strategy.dca_spot.indicators import add_indicators
from tools.strategy.dca_spot.engine import DCAConfig, run_simulation
from tools.strategy.dca_spot.run_backtest import benchmark_simple_weekly


# ── Grid ──────────────────────────────────────────────────────────────────────
REF_TYPES = ["w2_close", "ma4w"]
CORR_MEDIUM = [-5.0, -8.0, -10.0, -15.0]
CORR_LARGE = [-15.0, -20.0, -30.0]
MULT_MEDIUM = [2.0, 3.0, 5.0]
MULT_LARGE = [5.0, 10.0, 20.0]
SELL_MODES = ["price_only", "price_or_spike"]
SPIKE_KS = [1.5, 2.0, 3.0]


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[load + resample + indicators]", flush=True)
    df_m5 = load_m5_canonical(args.input)
    df_d1 = resample_to_d1(df_m5)
    df_d1 = add_indicators(df_d1)
    last_price = float(df_d1["close"].iloc[-1])
    print(f"  → {len(df_d1)} D1 bars  last={last_price}", flush=True)

    bench = benchmark_simple_weekly(df_d1)
    bench_avg = bench["avg_price"]
    bench_ret = bench["total_return_pct"]
    print(f"  benchmark avg_price={bench_avg}  return={bench_ret}%\n", flush=True)

    rows = []
    total = 0

    for ref, cm, cl, mm, ml, sell, spike_k in itertools.product(
        REF_TYPES, CORR_MEDIUM, CORR_LARGE, MULT_MEDIUM, MULT_LARGE,
        SELL_MODES, SPIKE_KS,
    ):
        # Skip if corr_large not stricter than corr_medium
        if cl >= cm:
            continue
        # spike_k only relevant for price_or_spike
        if sell == "price_only" and spike_k != SPIKE_KS[0]:
            continue

        cfg = DCAConfig(
            ref_type=ref,
            corr_medium_pct=cm,
            corr_large_pct=cl,
            mult_medium=mm,
            mult_large=ml,
            sell_mode=sell,
            spike_k=spike_k,
        )
        _, summary = run_simulation(df_d1, cfg)
        if "error" in summary:
            continue

        avg_all = summary.get("avg_price_all", float("nan"))
        ret = summary.get("total_return_pct", float("nan"))
        rows.append({
            "ref_type": ref,
            "corr_medium_pct": cm,
            "corr_large_pct": cl,
            "mult_medium": mm,
            "mult_large": ml,
            "sell_mode": sell,
            "spike_k": spike_k if sell == "price_or_spike" else "-",
            "n_l1": summary["n_l1_buys"],
            "n_l2": summary["n_l2_buys"],
            "n_l3": summary["n_l3_buys"],
            "n_l1_sells": summary["n_l1_sells"],
            "avg_price_all": avg_all,
            "avg_price_l1": summary.get("avg_price_l1", float("nan")),
            "avg_price_l2": summary.get("avg_price_l2", float("nan")),
            "avg_price_l3": summary.get("avg_price_l3", float("nan")),
            "price_delta_vs_bench": round(avg_all - bench_avg, 2) if avg_all == avg_all else float("nan"),
            "total_return_pct": ret,
            "return_delta_vs_bench": round(ret - bench_ret, 2) if ret == ret else float("nan"),
            "held_s": summary["held_s"],
            "max_simultaneous_s": summary["max_simultaneous_s"],
            "total_injected_s": summary["total_injected_s"],
            "l0_remaining_s": summary["l0_remaining_s"],
        })
        total += 1
        if total % 50 == 0:
            print(f"  {total} done", flush=True)

    df_r = pd.DataFrame(rows)
    # Sort by price_delta (lower = cheaper = better), then by return_delta
    df_r = df_r.sort_values(["price_delta_vs_bench", "return_delta_vs_bench"],
                             ascending=[True, False]).reset_index(drop=True)

    csv_path = out_dir / "dca_spot_optimization.csv"
    df_r.to_csv(csv_path, index=False)
    print(f"\n[out] {csv_path}  ({total} combos)", flush=True)

    # ── Only configs beating benchmark on BOTH avg_price AND return ──────────
    beats_both = df_r[
        (df_r["price_delta_vs_bench"] < 0) &
        (df_r["return_delta_vs_bench"] > 0)
    ]
    print(f"\n── BEATS BENCHMARK ON BOTH METRICS : {len(beats_both)} configs ────────")
    disp_cols = ["ref_type", "corr_medium_pct", "corr_large_pct", "mult_medium",
                 "mult_large", "sell_mode", "spike_k",
                 "n_l1", "n_l2", "n_l3", "avg_price_all",
                 "price_delta_vs_bench", "total_return_pct", "return_delta_vs_bench",
                 "max_simultaneous_s"]
    print(beats_both[disp_cols].head(20).to_string(index=True))

    print("\n── TOP 10 BY AVG PRICE (cheapest accumulation) ──────────────────────")
    print(df_r[disp_cols].head(10).to_string(index=True))

    print("\n── TOP 10 BY RETURN DELTA ───────────────────────────────────────────")
    best_ret = df_r.sort_values("return_delta_vs_bench", ascending=False)
    print(best_ret[disp_cols].head(10).to_string(index=True))

    print("\n── MARGINAL EFFECTS ─────────────────────────────────────────────────")
    for col in ["ref_type", "corr_medium_pct", "corr_large_pct",
                "mult_medium", "mult_large", "sell_mode"]:
        print(f"\n  {col}:")
        g = df_r.groupby(col)[["price_delta_vs_bench", "return_delta_vs_bench",
                                "n_l2", "n_l3"]].mean().round(3)
        print(g.to_string())

    # Benchmark line for reference
    print(f"\n── BENCHMARK ────────────────────────────────────────────────────────")
    print(f"  avg_price={bench_avg}  total_return={bench_ret}%  n_buys={bench['n_buys']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
