"""Production runtime for stock_true_value — daily pipeline at 08:30 Montréal.

Steps:
  1. Live collection (Yahoo Finance + SEC) + scoring
  2. Daily ranking
  3. Daily report (summary.md)
  4. Data Center publish (→ data_center/views/spacex_true_value.v1/)
  5. Telegram summary (optional, --telegram flag)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "stock_true_value" / "latest"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "stock_true_value" / "daily"
WATCHLIST = ["SPCX", "NVDA", "AVGO", "AMD", "MRVL", "MU", "PLTR", "RKLB", "ASTS", "LUNR"]


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _montreal_date() -> str:
    dt = datetime.now(timezone.utc) - timedelta(hours=4)
    return dt.strftime("%Y-%m-%d")


def step_collect() -> dict:
    """Step 1: Run live collector and score all tickers."""
    from modules.stock_true_value.live_collector import collect_and_score
    return collect_and_score(dry_run=False)


def step_ranking(scores: dict) -> list[dict]:
    """Step 2: Generate daily ranking from scores."""
    items = scores.get("items", [])
    ranked = sorted(items, key=lambda x: (x.get("final_score", 0), x.get("true_value_score", 0)), reverse=True)
    return [
        {"rank": i + 1, "ticker": r["ticker"], "grade": r["final_grade"],
         "true_value": r.get("true_value_score", 0), "final_score": r.get("final_score", 0)}
        for i, r in enumerate(ranked)
    ]


def step_report(scores: dict, ranking: list[dict]) -> str:
    """Step 3: Generate daily markdown report."""
    summary = scores.get("summary", {})
    lines = [
        "# Stock / SpaceX True Value — Daily Report",
        f"**Date:** {_montreal_date()} (Montréal)",
        f"**Generated:** {_utc_now()}",
        f"**Model:** {scores.get('model_version', 'v1')}",
        f"**Items:** {summary.get('count', 0)}",
        "",
        "## 📊 Ranking",
        "",
        "| Rank | Ticker | Grade | True Value | Final Score |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in ranking:
        lines.append(f"| {r['rank']} | {r['ticker']} | {r['grade']} | {r['true_value']:.1f} | {r['final_score']:.1f} |")

    lines += [
        "",
        "## 📈 Grade Distribution",
        "",
        "| Grade | Count |",
        "|---|---|",
    ]
    grades = summary.get("grades", {})
    for g, c in sorted(grades.items()):
        lines.append(f"| {g} | {c} |")

    lines += [
        "",
        "## 🔌 Collector Status",
        "",
    ]
    collectors = summary.get("collector_status", {})
    for name, status in sorted(collectors.items()):
        icon = "✅" if status == "active" else "⬜"
        lines.append(f"- {icon} **{name}**: {status}")

    lines += [
        "",
        "## ⚠️ Flags",
        "",
    ]
    items = scores.get("items", [])
    for it in items:
        flags = it.get("flags", [])
        if flags:
            lines.append(f"- **{it['ticker']}**: {', '.join(flags)}")
    if not any(it.get("flags") for it in items):
        lines.append("No flags raised.")

    lines += [
        "",
        "---",
        "Decision Support Only — no trading instruction.",
    ]
    return "\n".join(lines)


def step_telegram(report: str):
    """Step 4: Send telegram summary (only with --telegram flag)."""
    from modules.env.env import load_env
    load_env()
    from shared.telegram_notify import send_telegram
    summary = report[:3000] + ("..." if len(report) > 3000 else "")
    try:
        send_telegram(summary + "\n\nDecision Support Only — no trading instruction.")
        return True
    except Exception as e:
        print(f"Telegram send failed: {e}")
        return False


def run_production(send_telegram_flag: bool = False) -> dict:
    result: dict[str, Any] = {
        "started_at": _utc_now(),
        "steps": {},
    }

    # Step 1: Collect + Score
    print("Step 1/4: Collecting live data...")
    scores = step_collect()
    result["steps"]["collect"] = {"ok": True, "items": scores["summary"]["count"]}

    # Step 2: Ranking
    print("Step 2/4: Computing ranking...")
    ranking = step_ranking(scores)
    result["steps"]["ranking"] = {"ok": True, "tickers_ranked": len(ranking)}

    # Step 3: Report
    print("Step 3/4: Generating daily report...")
    report = step_report(scores, ranking)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{_montreal_date()}_report.md"
    report_path.write_text(report)
    ranking_path = REPORTS_DIR / f"{_montreal_date()}_ranking.json"
    ranking_path.write_text(json.dumps(ranking, indent=2))
    result["steps"]["report"] = {"ok": True, "path": str(report_path), "ranking_path": str(ranking_path)}

    # Step 4: Data Center publish
    print("Step 4/5: Publishing to Data Center...")
    from modules.stock_true_value.dc_publisher import publish_to_data_center
    dc_result = publish_to_data_center()
    result["steps"]["dc_publish"] = dc_result

    # Step 5: Telegram (optional)
    if send_telegram_flag:
        print("Step 5/5: Sending telegram summary...")
        ok = step_telegram(report)
        result["steps"]["telegram"] = {"ok": ok, "sent": ok}
    else:
        result["steps"]["telegram"] = {"ok": True, "sent": False, "reason": "flag not set"}

    result["completed_at"] = _utc_now()
    result["all_ok"] = all(s.get("ok", False) for s in result["steps"].values())
    return result


if __name__ == "__main__":
    telegram = "--telegram" in sys.argv
    result = run_production(send_telegram_flag=telegram)
    print(f"\n{'PASS' if result['all_ok'] else 'FAIL'} — "
          f"Collect={result['steps']['collect']['items']} items, "
          f"Ranked={result['steps']['ranking']['tickers_ranked']}, "
          f"DC={result['steps']['dc_publish'].get('items', 0)} published, "
          f"Telegram={'sent' if result['steps']['telegram'].get('sent') else 'skipped'}")
