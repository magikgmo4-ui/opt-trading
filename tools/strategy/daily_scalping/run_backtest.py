#!/usr/bin/env python3
"""
run_backtest.py — Orchestrateur backtest SMC_ORB_VWAP_SCALP_A_PLUS.

Usage:
    python tools/strategy/daily_scalping/run_backtest.py \
        --symbol XAUUSD \
        --timeframe M5 \
        --context-timeframe M15 \
        --input data/market/xauusd_m5.csv \
        --context-input data/market/xauusd_m15.csv \
        --out artifacts/backtests/daily_scalping
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.strategy.daily_scalping.load_data import load_ohlcv, merge_timeframes
from tools.strategy.daily_scalping.indicators import add_all
from tools.strategy.daily_scalping.detectors import detect_all
from tools.strategy.daily_scalping.scorer import score_setup
from tools.strategy.daily_scalping.simulator import simulate_all
from tools.strategy.daily_scalping import report as rpt


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily scalping backtest runner")
    parser.add_argument("--symbol", default="XAUUSD")
    parser.add_argument("--timeframe", default="M5")
    parser.add_argument("--context-timeframe", default="M15")
    parser.add_argument("--input", required=True, help="M5 OHLCV CSV")
    parser.add_argument("--context-input", required=True, help="M15 OHLCV CSV")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument("--min-score", type=int, default=7)
    parser.add_argument(
        "--variants",
        default="ORB_ONLY,VWAP_PULLBACK_ONLY,SMC_SWEEP_ONLY,COMBINED_SMC_ORB_VWAP",
    )
    parser.add_argument("--verdict-out", default="", help="Path for verdict markdown")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    variants = [v.strip() for v in args.variants.split(",")]

    print(f"[load] {args.input}")
    df_exec = load_ohlcv(args.input)
    print(f"[load] {args.context_input}")
    df_ctx = load_ohlcv(args.context_input)

    print("[merge] M5 + M15 context")
    df = merge_timeframes(df_exec, df_ctx)

    print("[indicators] VWAP, ATR, ORB, swings")
    df = add_all(df)

    print(f"[detect] variants={variants}")
    setups = detect_all(df, variants)
    print(f"  → {len(setups)} setups detected")

    print("[score]")
    scores = [score_setup(s) for s in setups]

    print("[simulate]")
    results = simulate_all(setups, scores, df, min_score=args.min_score)
    print(f"  → {len(results)} trades simulated")

    print("[report] journal CSV")
    journal_df = rpt.results_to_journal_df(results)
    journal_path = rpt.write_journal_csv(journal_df, out_dir)
    print(f"  → {journal_path}")

    print("[report] results by variant CSV")
    metrics = rpt.compute_variant_metrics(journal_df)
    results_path = rpt.write_results_csv(metrics, out_dir)
    print(f"  → {results_path}")

    verdict_path = Path(args.verdict_out) if args.verdict_out else out_dir / "xauusd_m5_verdict.md"
    print(f"[report] verdict markdown → {verdict_path}")
    rpt.write_verdict_markdown(metrics, verdict_path)

    print("\n[summary]")
    for variant, m in metrics.items():
        print(
            f"  {variant:30s} trades={m.get('trades_count',0):4d} "
            f"exp={m.get('expectancy_R','—'):>7} "
            f"pf={m.get('profit_factor','—'):>6} "
            f"→ {m.get('verdict','—')}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
