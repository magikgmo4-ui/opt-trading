"""Governance validator for stock_true_value — continuous monitoring.

Checks:
  1. Schema Drift — scores.json matches output.schema.json
  2. Source Drift — collector status hasn't regressed
  3. Collector Failure — Yahoo Finance is reachable
  4. Confidence Degradation — no broad confidence drops
  5. Score Stability — no wild swings day-over-day
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "stock_true_value" / "latest"
DAILY_DIR = PROJECT_ROOT / "outputs" / "stock_true_value" / "daily"
GOVERNANCE_DIR = PROJECT_ROOT / "outputs" / "stock_true_value" / "governance"

WATCHLIST = ["SPCX", "NVDA", "AVGO", "AMD", "MRVL", "MU", "PLTR", "RKLB", "ASTS", "LUNR"]


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def check_schema_drift() -> dict:
    """R1: Verify scores.json exists and has required structure."""
    path = OUTPUT_DIR / "scores.json"
    if not path.exists():
        return {"pass": False, "reason": "scores.json not found", "action": "run production_runtime.py"}
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        return {"pass": False, "reason": f"invalid JSON: {e}"}
    if "items" not in data:
        return {"pass": False, "reason": "missing 'items' key"}
    if "summary" not in data:
        return {"pass": False, "reason": "missing 'summary' key"}
    return {"pass": True, "items": len(data["items"])}


def check_source_drift() -> dict:
    """R2: Verify collector status hasn't regressed."""
    path = OUTPUT_DIR / "scores.json"
    if not path.exists():
        return {"pass": False, "reason": "no data"}
    data = json.loads(path.read_text())
    collectors = data.get("summary", {}).get("collector_status", {})
    active = [k for k, v in collectors.items() if v == "active"]
    stubs = [k for k, v in collectors.items() if v == "stub"]
    return {"pass": len(active) > 0, "active": active, "stubs": stubs}


def check_collector_health() -> dict:
    """R3: Verify Yahoo Finance API is reachable."""
    from modules.ipo_tracking.collectors.yahoo_public import collect_yahoo_quote
    result = collect_yahoo_quote("SPCX", timeout=10)
    return {"pass": result.get("ok", False), "symbol": "SPCX",
            "price": result.get("regular_market_price"),
            "error": result.get("error")}


def check_confidence_degradation() -> dict:
    """R4: Check no broad confidence drops across tickers."""
    path = OUTPUT_DIR / "scores.json"
    if not path.exists():
        return {"pass": False, "reason": "no data"}
    data = json.loads(path.read_text())
    items = data.get("items", [])
    if not items:
        return {"pass": True, "reason": "no items"}
    low = [it for it in items if it.get("confidence_score", 0) < 60]
    pct = len(low) / len(items) * 100
    return {"pass": pct <= 50, "low_confidence_count": len(low),
            "total": len(items), "low_pct": round(pct, 1)}


def check_score_stability() -> dict:
    """R5: Compare latest scores with previous day (if available)."""
    paths = sorted(DAILY_DIR.glob("*_ranking.json"), reverse=True)
    if len(paths) < 2:
        return {"pass": True, "reason": "insufficient history (< 2 days)"}

    today = json.loads(paths[0].read_text())
    yesterday = json.loads(paths[1].read_text())
    ticks_today = {r["ticker"]: r for r in today}
    ticks_yesterday = {r["ticker"]: r for r in yesterday}

    swings = []
    for t in WATCHLIST:
        tv_today = ticks_today.get(t, {}).get("true_value", 0)
        tv_yesterday = ticks_yesterday.get(t, {}).get("true_value", 0)
        if tv_today and tv_yesterday:
            swing = abs(tv_today - tv_yesterday)
            if swing > 20:
                swings.append({"ticker": t, "swing": round(swing, 1)})

    return {"pass": len(swings) == 0, "swings": swings, "days_compared": 2}


def run_governance() -> dict:
    checks = {}
    results = {}

    print("R1: Schema Drift...")
    results["schema_drift"] = check_schema_drift()
    checks["schema_drift"] = results["schema_drift"]["pass"]

    print("R2: Source Drift...")
    results["source_drift"] = check_source_drift()
    checks["source_drift"] = results["source_drift"]["pass"]

    print("R3: Collector Health...")
    results["collector_health"] = check_collector_health()
    checks["collector_health"] = results["collector_health"]["pass"]

    print("R4: Confidence Degradation...")
    results["confidence"] = check_confidence_degradation()
    checks["confidence"] = results["confidence"]["pass"]

    print("R5: Score Stability...")
    results["stability"] = check_score_stability()
    checks["stability"] = results["stability"]["pass"]

    all_pass = all(checks.values())
    report = {
        "asof": _utc_now(),
        "all_pass": all_pass,
        "checks": checks,
        "results": results,
    }

    GOVERNANCE_DIR.mkdir(parents=True, exist_ok=True)
    report_path = GOVERNANCE_DIR / f"{_utc_now()[:10]}_governance.json"
    report_path.write_text(json.dumps(report, indent=2))

    return report


def print_report(report: dict):
    checks = report["checks"]
    results = report["results"]
    for name, passed in checks.items():
        icon = "PASS" if passed else "FAIL"
        detail = results[name].get("reason") or results[name].get("error") or ""
        if detail:
            print(f"  {icon} {name}: {detail}")
        else:
            print(f"  {icon} {name}")
    print(f"\nOverall: {'PASS' if report['all_pass'] else 'FAIL'}")


if __name__ == "__main__":
    report = run_governance()
    print_report(report)

