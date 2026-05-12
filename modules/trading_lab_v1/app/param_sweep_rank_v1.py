#!/usr/bin/env python3
"""BTC COIN-M sweep ranker."""
from __future__ import annotations

from typing import Any


def rank_runs(runs: list[dict[str, Any]], mode: str = "raw_best") -> list[dict[str, Any]]:
    """Sort and filter runs by the given ranking mode."""
    filtered = _filter_population(runs, mode)
    return _sort_runs(filtered, mode)


def _filter_population(runs: list[dict[str, Any]], mode: str) -> list[dict[str, Any]]:
    if mode in ("raw_best", "raw_worst"):
        return [r for r in runs
                if r.get("math_valid") and r.get("data_valid")]
    if mode == "realistic_best":
        return [r for r in runs
                if r.get("classification_primary") == "REALISTIC"]
    if mode == "feasible_best":
        return [r for r in runs
                if r.get("classification_primary") in ("REALISTIC", "PAPER_ONLY")]
    if mode == "non_liquidated_best":
        return [r for r in runs
                if r.get("liquidation_count", 0) == 0
                and r.get("math_valid")
                and r.get("data_valid")]
    return runs


def _sort_runs(runs: list[dict[str, Any]], mode: str) -> list[dict[str, Any]]:
    reverse = "worst" not in mode
    sorted_runs = sorted(runs, key=_sort_key, reverse=reverse)
    for i, run in enumerate(sorted_runs):
        run["_rank"] = i + 1
    return sorted_runs


def _sort_key(run: dict[str, Any]) -> tuple:
    delta = run.get("delta_btc_net", 0.0)
    liq = run.get("liquidation_count", 0)
    dd = run.get("max_drawdown_btc", 0.0)
    funding = run.get("funding_paid_btc", 0.0)
    fees = run.get("fees_btc", 0.0)
    cost = funding + fees
    overfit = run.get("overfit_score", 0.0)
    cfg_hash = run.get("config_hash", "")
    return (delta, -liq, -dd, -cost, -overfit, cfg_hash)


def format_top_markdown(runs: list[dict[str, Any]], top_n: int = 100,
                        title: str = "Top Results") -> str:
    lines = [f"# {title}", ""]
    runs = runs[:top_n]

    header = ("| Rank | Run ID | Config Hash | Δ BTC | Δ % | "
              "Final BTC | Liq | DD BTC | Funding Paid | Fees | Class |")
    sep = "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"
    lines.append(header)
    lines.append(sep)

    for r in runs:
        rank = r.get("_rank", "?")
        rid = str(r.get("run_id", ""))[:8]
        cfg = str(r.get("config_hash", ""))[:8]
        delta = r.get("delta_btc_net", 0)
        delta_pct = r.get("delta_btc_pct", 0)
        final = r.get("net_btc_final", 0)
        liq = r.get("liquidation_count", 0)
        dd = r.get("max_drawdown_btc", 0)
        fp = r.get("funding_paid_btc", 0)
        fees = r.get("fees_btc", 0)
        cls = r.get("classification_primary", "")
        lines.append(
            f"| {rank} | {rid} | {cfg} | {delta:+.8f} | {delta_pct:+.2f}% | "
            f"{final:.8f} | {liq} | {dd:.6f} | {fp:.8f} | {fees:.8f} | {cls} |"
        )

    return "\n".join(lines) + "\n"
