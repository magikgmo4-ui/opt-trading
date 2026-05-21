"""report.py — CSV journal + results by variant + markdown verdict."""
from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List

import pandas as pd

from .simulator import TradeResult


_VARIANTS = ["ORB_ONLY", "VWAP_PULLBACK_ONLY", "SMC_SWEEP_ONLY", "COMBINED_SMC_ORB_VWAP"]


def results_to_journal_df(results: List[TradeResult]) -> pd.DataFrame:
    rows = []
    for i, r in enumerate(results):
        rows.append({
            "trade_id": i + 1,
            "date": r.setup.index.isoformat(),
            "symbol": "XAUUSD",
            "session": r.setup.session,
            "timeframe": "M5",
            "variant": r.setup.variant,
            "direction": r.setup.direction,
            "setup_type": r.setup.setup_type,
            "setup_score": r.score,
            "entry_price": r.entry_price,
            "stop_loss": r.sl,
            "tp1": r.tp1,
            "tp2": r.tp2,
            "rr_planned": round(abs(r.tp1 - r.entry_price) / max(abs(r.entry_price - r.sl), 1e-9), 2),
            "result_R": r.result_R,
            "mae_R": r.mae_R,
            "mfe_R": r.mfe_R,
            "time_in_trade_bars": r.time_in_trade_bars,
            "exit_reason": r.exit_reason,
            "followed_plan": r.followed_plan,
            "orb_state": r.setup.orb_state,
            "vwap_state": r.setup.vwap_state,
            "liquidity_state": r.setup.liquidity_state,
            "structure_state": r.setup.structure_state,
        })
    return pd.DataFrame(rows)


def compute_variant_metrics(df: pd.DataFrame) -> Dict[str, dict]:
    metrics = {}
    if df.empty or "variant" not in df.columns:
        for variant in _VARIANTS:
            metrics[variant] = {"trades_count": 0, "verdict": "NO_DATA"}
        return metrics
    for variant in _VARIANTS:
        sub = df[df["variant"] == variant]
        if sub.empty:
            metrics[variant] = {"trades_count": 0, "verdict": "NO_DATA"}
            continue

        n = len(sub)
        wins = sub[sub["result_R"] > 0]
        losses = sub[sub["result_R"] <= 0]
        winrate = len(wins) / n if n > 0 else 0.0
        avg_win = wins["result_R"].mean() if len(wins) else 0.0
        avg_loss = abs(losses["result_R"].mean()) if len(losses) else 0.0
        expectancy = winrate * avg_win - (1 - winrate) * avg_loss
        total_win = wins["result_R"].sum()
        total_loss = abs(losses["result_R"].sum())
        pf = total_win / total_loss if total_loss > 0 else float("inf")

        # Max drawdown (running)
        cumulative = sub["result_R"].cumsum()
        peak = cumulative.cummax()
        dd = (cumulative - peak)
        max_dd = dd.min()

        # Max losing streak
        streaks, cur = 0, 0
        for r in sub["result_R"]:
            cur = cur + 1 if r <= 0 else 0
            streaks = max(streaks, cur)

        # Score bucket performance
        hi = sub[sub["setup_score"] >= 7]
        lo = sub[sub["setup_score"] < 7]
        hi_wr = len(hi[hi["result_R"] > 0]) / len(hi) if len(hi) else None
        lo_wr = len(lo[lo["result_R"] > 0]) / len(lo) if len(lo) else None
        score_ok = (hi_wr is not None and lo_wr is not None and hi_wr > lo_wr)

        # Verdict
        if n < 100:
            verdict = "NEED_MORE_DATA"
        elif expectancy <= 0:
            verdict = "REJECT_VARIANT"
        elif expectancy > 0.15 and pf > 1.25 and score_ok:
            verdict = "PROMOTE_TO_PAPER_FORWARD"
        else:
            verdict = "REWORK_RULESET"

        metrics[variant] = {
            "trades_count": n,
            "winrate": round(winrate, 3),
            "avg_win_R": round(avg_win, 3),
            "avg_loss_R": round(avg_loss, 3),
            "expectancy_R": round(expectancy, 4),
            "profit_factor": round(pf, 3) if not math.isinf(pf) else 999.0,
            "max_drawdown_R": round(max_dd, 3),
            "max_losing_streak": streaks,
            "avg_time_in_trade_bars": round(sub["time_in_trade_bars"].mean(), 1),
            "score_7plus_winrate": round(hi_wr, 3) if hi_wr is not None else None,
            "score_lt7_winrate": round(lo_wr, 3) if lo_wr is not None else None,
            "verdict": verdict,
        }
    return metrics


def write_journal_csv(df: pd.DataFrame, out_dir: Path) -> Path:
    path = out_dir / "xauusd_m5_journal.csv"
    df.to_csv(path, index=False)
    return path


def write_results_csv(metrics: Dict[str, dict], out_dir: Path) -> Path:
    path = out_dir / "xauusd_m5_results_by_variant.csv"
    pd.DataFrame(metrics).T.to_csv(path)
    return path


def write_verdict_markdown(metrics: Dict[str, dict], out_path: Path) -> None:
    rows = []
    for variant, m in metrics.items():
        rows.append(
            f"| {variant} | {m.get('trades_count', 0)} "
            f"| {m.get('winrate', '—')} "
            f"| {m.get('expectancy_R', '—')} "
            f"| {m.get('profit_factor', '—')} "
            f"| {m.get('max_drawdown_R', '—')} "
            f"| **{m.get('verdict', '—')}** |"
        )

    best = max(
        ((v, m) for v, m in metrics.items() if m.get("trades_count", 0) >= 100),
        key=lambda x: x[1].get("expectancy_R", -999),
        default=(None, {}),
    )
    best_variant = best[0] or "—"
    best_m = best[1]
    final_verdict = best_m.get("verdict", "NEED_MORE_DATA") if best_variant != "—" else "NEED_MORE_DATA"

    next_go = (
        "GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PAPER_FORWARD_01"
        if "PROMOTE" in final_verdict
        else "Rework strategy rules before paper forward"
    )

    md = f"""# BACKTEST_VERDICT_01

**Symbol:** XAUUSD  **Timeframe:** M5/M15

## Résultats par variant

| Variant | Trades | Winrate | Expectancy R | PF | Max DD R | Verdict |
|---|---:|---:|---:|---:|---:|---|
{chr(10).join(rows)}

## Variant retenu

**{best_variant}** — Expectancy: {best_m.get('expectancy_R', '—')}R — PF: {best_m.get('profit_factor', '—')}

## Décision finale

**{final_verdict}**

## Prochaine étape

→ {next_go}
"""
    out_path.write_text(md, encoding="utf-8")
