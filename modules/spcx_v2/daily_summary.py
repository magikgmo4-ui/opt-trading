"""SPCX V2 — Daily summary: markdown report aggregator."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from modules.spcx_v2.paper_logger import list_candidates, get_summary
from modules.spcx_v2.config import PROJECT_ROOT


def generate_daily_summary(date_str: Optional[str] = None) -> dict:
    if date_str is None:
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")

    summary = get_summary()
    candidates = list_candidates()

    grade_buckets = {}
    for c in candidates:
        g = c.grade
        grade_buckets.setdefault(g, []).append({
            "setup_type": c.setup_type,
            "ts": c.ts,
            "scores": {
                "trade_ready": c.scores.trade_ready,
                "liquidity": c.scores.liquidity,
                "risk": c.scores.risk,
                "smart_money": c.scores.smart_money,
                "catalyst": c.scores.catalyst,
            },
            "r_multiple": c.r_multiple,
        })

    setup_buckets = {}
    for c in candidates:
        st = c.setup_type
        setup_buckets.setdefault(st, 0)
        setup_buckets[st] += 1

    return {
        "date": date_str,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "totals": {
            "candidates": summary.get("total_candidates", 0),
            "rejects": summary.get("total_rejects", 0),
        },
        "by_grade": summary.get("by_grade", {}),
        "by_setup_type": setup_buckets,
        "winrate": summary.get("winrate", 0),
        "expectancy_R": summary.get("expectancy_R", 0),
        "profit_factor": summary.get("profit_factor"),
        "total_results": summary.get("total_results", 0),
    }


def write_daily_markdown(date_str: Optional[str] = None) -> Path:
    if date_str is None:
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")

    data = generate_daily_summary(date_str)

    lines = [
        f"# SPCX V2 — Daily Paper Summary {date_str}",
        "",
        f"Generated: {data['generated_at']}",
        "",
        "## Totals",
        "",
        f"- Setups detected: {data['totals']['candidates']}",
        f"- Rejects: {data['totals']['rejects']}",
        "",
        "## By Grade",
        "",
        *[f"- {g}: {c}" for g, c in sorted(data.get("by_grade", {}).items())],
        "",
        "## By Setup Type",
        "",
        *[f"- {st}: {c}" for st, c in sorted(data.get("by_setup_type", {}).items())],
        "",
        "## Performance",
        "",
        f"- Winrate: {data['winrate']}%",
        f"- Expectancy: {data['expectancy_R']}R",
        f"- Profit Factor: {data['profit_factor'] if data['profit_factor'] is not None else 'N/A'}",
        f"- Total results: {data['total_results']}",
        "",
        "---",
        "",
        "<i>Paper-only. No execution. Monitor-only.</i>",
    ]

    out = PROJECT_ROOT / "reports" / "ipo" / "spacex" / f"spcx_v2_daily_{date_str}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out
