#!/usr/bin/env python3
"""
SPCX Day-1 Replay — MFE/MAE/R calculator + dedup + verdict
GO_SPACEX_DAY1_REPLAY_SCORING_FIX_01

Reads: paper_log candidates + Yahoo bars
Output: replay verdict per setup cluster
"""
from __future__ import annotations
import json, sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]

def load_bars() -> list[dict]:
    from modules.ipo_tracking.collectors.yahoo_public import collect_yahoo_quote
    result = collect_yahoo_quote("SPCX")
    return [b for b in result.get("bars", []) if b.get("volume") and b["volume"] > 0]

def load_candidates() -> list[dict]:
    path = REPO_ROOT / "data" / "ipo" / "spacex" / "paper_log" / "candidates.jsonl"
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]

def load_rejects() -> list[dict]:
    path = REPO_ROOT / "data" / "ipo" / "spacex" / "paper_log" / "rejects.jsonl"
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]

def replay_trade(entry_price: float, bars: list[dict], tp1_pct: float = 3.0, tp2_pct: float = 5.0, sl_pct: float = -2.0) -> dict:
    """Replay a trade against real bars. Returns MFE, MAE, R multiples."""
    tp1 = entry_price * (1 + tp1_pct / 100)
    tp2 = entry_price * (1 + tp2_pct / 100)
    sl = entry_price * (1 + sl_pct / 100)

    mfe = 0.0  # Maximum Favorable Excursion (%)
    mae = 0.0  # Maximum Adverse Excursion (%)
    hit_tp1 = False
    hit_tp2 = False
    hit_sl = False
    bars_held = 0
    exit_price = entry_price

    for b in bars:
        high = b.get("high", 0)
        low = b.get("low", 0)
        close = b.get("close", 0)
        if not high or not low:
            continue

        bars_held += 1
        current_ret = (close - entry_price) / entry_price * 100
        mfe = max(mfe, (high - entry_price) / entry_price * 100)
        mae = min(mae, (low - entry_price) / entry_price * 100)

        if high >= tp2:
            hit_tp2 = True
            exit_price = tp2
            break
        if high >= tp1:
            hit_tp1 = True
        if low <= sl:
            hit_sl = True
            exit_price = sl
            break

    r_multiple = (exit_price - entry_price) / entry_price * 100 / abs(sl_pct)
    return {
        "entry": round(entry_price, 2),
        "exit": round(exit_price, 2),
        "mfe_pct": round(mfe, 2),
        "mae_pct": round(mae, 2),
        "r_multiple": round(r_multiple, 2),
        "hit_tp1": hit_tp1,
        "hit_tp2": hit_tp2,
        "hit_sl": hit_sl,
        "bars_held": bars_held,
        "verdict": "WIN" if hit_tp1 or hit_tp2 else ("LOSS" if hit_sl else "OPEN"),
    }

def dedup_candidates(candidates: list[dict]) -> list[dict]:
    """Merge identical setups within same session into clusters."""
    clusters = {}
    for c in candidates:
        key = c.get("setup_type", "UNKNOWN")
        if key not in clusters:
            clusters[key] = {
                "setup_type": key,
                "grade": c.get("grade"),
                "raw_count": 0,
                "scores": c.get("scores", {}),
                "entries": [],
            }
        clusters[key]["raw_count"] += 1
        clusters[key]["entries"].append(c)

    return list(clusters.values())

def generate_report(bars: list[dict], candidates: list[dict], rejects: list[dict]) -> str:
    clusters = dedup_candidates(candidates)
    lines = []
    lines.append("# SPCX Day-1 Replay Report")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")

    # Price path
    first = bars[0] if bars else {}
    last = bars[-1] if bars else {}
    highs = [b["high"] for b in bars]
    lows = [b["low"] for b in bars]
    volumes = [b["volume"] for b in bars]
    lines.append("## Price Path")
    lines.append(f"- Open: ${first.get('open', '?')}")
    lines.append(f"- High: ${max(highs):.2f}")
    lines.append(f"- Low: ${min(lows):.2f}")
    lines.append(f"- Close: ${last.get('close', '?')}")
    lines.append(f"- Range: ${max(highs) - min(lows):.2f}")
    lines.append(f"- Avg Volume: {sum(volumes)/len(volumes):,.0f}")
    lines.append(f"- Total Bars: {len(bars)}")
    lines.append("")

    # Candidates
    lines.append("## Trade Candidates")
    lines.append(f"- Raw candidates: {len(candidates)}")
    lines.append(f"- After dedup: {len(clusters)} clusters")
    lines.append(f"- Rejects: {len(rejects)}")
    lines.append("")

    for cl in clusters:
        lines.append(f"### {cl['setup_type']} (grade {cl['grade']}, {cl['raw_count']} raw)")
        # Use last entry price from candidates
        entry_price = last.get("close", 0)
        replay = replay_trade(entry_price, bars)

        lines.append(f"- Entry (est): ${replay['entry']}")
        lines.append(f"- MFE: +{replay['mfe_pct']}% | MAE: {replay['mae_pct']}%")
        lines.append(f"- R: {replay['r_multiple']} | TP1: {replay['hit_tp1']} | TP2: {replay['hit_tp2']} | SL: {replay['hit_sl']}")
        lines.append(f"- Verdict: {replay['verdict']}")
        lines.append("")

    # Rejects
    if rejects:
        lines.append("## Rejects")
        for r in rejects:
            reasons = r.get("reason_codes", [])
            lines.append(f"- {r.get('setup_type', 'NONE')}: {', '.join(reasons)}")
        lines.append("")

    # Verdict
    lines.append("## Final Verdict")
    wins = sum(1 for cl in clusters
               if replay_trade(last.get("close", 0), bars)["verdict"] == "WIN")
    lines.append(f"- Validated setups: {wins}/{len(clusters)}")
    lines.append(f"- Monitor-only: no real orders")
    lines.append(f"- Next session: re-evaluate after market open")

    return "\n".join(lines)

def main():
    bars = load_bars()
    candidates = load_candidates()
    rejects = load_rejects()

    if not bars:
        print("No bars available — market closed")
        return 1

    report = generate_report(bars, candidates, rejects)
    report_path = REPO_ROOT / "reports" / "ipo" / "spacex" / "spacex_day1_replay_20260612.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    print(report)
    print(f"\nReport: {report_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
