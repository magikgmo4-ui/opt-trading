"""Stability monitoring collector — samples runtime state every 15 minutes.

Phases S1-S6:
  S1: Uptime — are services/collectors reachable?
  S2: Freshness — dataset ages
  S3: Score Drift — true_value variations
  S4: Collectors — runs, success, errors, latency
  S5: Alerts — generated, delivered, rejected
  S6: Governance — schema, fields, confidence, stale

Output: outputs/stock_true_value/stability/YYYY-MM-DD_HHMM_snapshot.json
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
STABILITY_DIR = PROJECT_ROOT / "outputs" / "stock_true_value" / "stability"
SCORES_PATH = PROJECT_ROOT / "outputs" / "stock_true_value" / "latest" / "scores.json"
DATA_DIR = PROJECT_ROOT / "data" / "data_center" / "views"


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _age_minutes(path: Path) -> float:
    if not path.exists():
        return -1
    return (time.time() - path.stat().st_mtime) / 60


# ── S1: Uptime ────────────────────────────────────────────────────────

def sample_uptime() -> dict:
    import urllib.request
    checks = {}

    # LocalCMS
    t0 = time.time()
    try:
        req = urllib.request.Request("http://127.0.0.1:8700/health")
        with urllib.request.urlopen(req, timeout=5) as resp:
            checks["localcms"] = {"ok": resp.status == 200, "latency_ms": round((time.time() - t0) * 1000)}
    except Exception as e:
        checks["localcms"] = {"ok": False, "error": str(e)[:80]}

    # True Value route
    t0 = time.time()
    try:
        req = urllib.request.Request("http://127.0.0.1:8700/true-value/json")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            checks["true_value_api"] = {"ok": True, "items": len(data.get("items", [])),
                                        "latency_ms": round((time.time() - t0) * 1000)}
    except Exception as e:
        checks["true_value_api"] = {"ok": False, "error": str(e)[:80]}

    # Scores file
    checks["scores_file"] = {"ok": SCORES_PATH.exists(), "path": str(SCORES_PATH)}

    # Collectors
    from modules.stock_true_value.live_collector import COLLECTOR_STATUS
    checks["collector_status"] = dict(COLLECTOR_STATUS)

    return checks


# ── S2: Freshness ──────────────────────────────────────────────────────

def sample_freshness() -> dict:
    datasets = {}

    # True Value scores
    datasets["true_value_scores"] = {"age_min": round(_age_minutes(SCORES_PATH), 1)}

    # Data Center views
    for view_dir in DATA_DIR.iterdir() if DATA_DIR.exists() else []:
        latest = view_dir / "latest.json"
        if latest.exists():
            age = _age_minutes(latest)
            datasets[f"data_center.{view_dir.name}"] = {"age_min": round(age, 1)}

    # Per-symbol vision analysis
    vis_dir = DATA_DIR / "vision_analysis" / "by_symbol"
    if vis_dir.exists():
        for f in vis_dir.glob("*.json"):
            age = _age_minutes(f)
            datasets[f"vision.{f.stem}"] = {"age_min": round(age, 1)}

    # Classification
    fresh = sum(1 for v in datasets.values() if 0 <= v["age_min"] < 30)
    acceptable = sum(1 for v in datasets.values() if 30 <= v["age_min"] < 360)
    stale = sum(1 for v in datasets.values() if 360 <= v["age_min"] < 1440)
    dead = sum(1 for v in datasets.values() if v["age_min"] >= 1440 or v["age_min"] == -1)
    total = len(datasets)

    return {
        "total": total,
        "fresh": fresh,
        "acceptable": acceptable,
        "stale": stale,
        "dead": dead,
        "freshness_pct": round(fresh / total * 100, 1) if total else 0,
        "datasets": datasets,
    }


# ── S3: Score Drift ────────────────────────────────────────────────────

def sample_score_drift() -> dict:
    if not SCORES_PATH.exists():
        return {"ok": False, "reason": "no scores"}

    data = json.loads(SCORES_PATH.read_text())
    items = data.get("items", [])
    scores = {}
    for it in items:
        ticker = it.get("ticker", "?")
        scores[ticker] = {
            "grade": it.get("final_grade"),
            "true_value": it.get("true_value_score"),
            "hype": it.get("hype_score"),
            "risk": it.get("risk_score"),
            "confidence": it.get("confidence_score"),
        }

    # Load previous snapshot for drift comparison
    prev_files = sorted(STABILITY_DIR.glob("*_snapshot.json"))
    drift = {}
    if len(prev_files) >= 1:
        prev = json.loads(prev_files[-1].read_text())
        prev_scores = prev.get("scores", {}).get("ticker_scores", {})
        for ticker, curr in scores.items():
            prev_val = prev_scores.get(ticker, {}).get("true_value", 0)
            if prev_val and curr["true_value"]:
                drift[ticker] = round(curr["true_value"] - prev_val, 2)

    return {
        "ok": True,
        "ticker_scores": scores,
        "drift_vs_previous": drift,
    }


# ── S4: Collectors ─────────────────────────────────────────────────────

def sample_collectors() -> dict:
    collectors = {}

    # Yahoo Finance
    t0 = time.time()
    try:
        from modules.ipo_tracking.collectors.yahoo_public import collect_yahoo_quote
        r = collect_yahoo_quote("SPCX", timeout=10)
        collectors["yahoo_finance"] = {
            "ok": r.get("ok", False),
            "latency_ms": round((time.time() - t0) * 1000),
            "price": r.get("regular_market_price"),
            "error": r.get("error"),
        }
    except Exception as e:
        collectors["yahoo_finance"] = {"ok": False, "error": str(e)[:80]}

    # SEC EDGAR
    t0 = time.time()
    try:
        from modules.stock_true_value.live_collector import _sec_edgar_filings
        r = _sec_edgar_filings()
        collectors["sec_edgar"] = {
            "ok": r.get("ok", False),
            "latency_ms": round((time.time() - t0) * 1000),
            "filing_count": r.get("filing_count", 0),
            "error": r.get("error"),
        }
    except Exception as e:
        collectors["sec_edgar"] = {"ok": False, "error": str(e)[:80]}

    # Summarize
    active_ok = sum(1 for v in collectors.values() if v.get("ok"))
    active_total = len(collectors)
    return {
        "active_total": active_total,
        "active_ok": active_ok,
        "health_pct": round(active_ok / active_total * 100) if active_total else 0,
        "collectors": collectors,
    }


# ── S5: Alerts ─────────────────────────────────────────────────────────

def sample_alerts() -> dict:
    try:
        from modules.stock_true_value.telegram_alerter import _load_scores, _check_alerts
        data = _load_scores()
        alerts = _check_alerts(data.get("items", []))
    except Exception as e:
        return {"ok": False, "error": str(e), "alerts_generated": 0}

    return {
        "ok": True,
        "alerts_generated": len(alerts),
        "alerts": alerts[:5],
    }


# ── S6: Governance ─────────────────────────────────────────────────────

def sample_governance() -> dict:
    try:
        from modules.stock_true_value.governance import (
            check_schema_drift, check_source_drift, check_collector_health,
            check_confidence_degradation, check_score_stability,
        )
        results = {
            "schema_drift": check_schema_drift(),
            "source_drift": check_source_drift(),
            "collector_health": check_collector_health(),
            "confidence": check_confidence_degradation(),
            "stability": check_score_stability(),
        }
        passed = sum(1 for v in results.values() if v.get("pass"))
        return {"checks_passed": passed, "checks_total": len(results), "results": results}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ── Main ───────────────────────────────────────────────────────────────

def collect_snapshot() -> dict:
    """Collect all S1-S6 samples into a single stability snapshot."""
    snapshot = {
        "ts": _utc_now(),
        "day": 0,  # incremented manually or by orchestration
        "s1_uptime": sample_uptime(),
        "s2_freshness": sample_freshness(),
        "s3_score_drift": sample_score_drift(),
        "s4_collectors": sample_collectors(),
        "s5_alerts": sample_alerts(),
        "s6_governance": sample_governance(),
    }
    return snapshot


def compute_health(snapshot: dict) -> dict:
    """Compute operational health score from snapshot."""
    s1 = snapshot.get("s1_uptime", {})
    s2 = snapshot.get("s2_freshness", {})
    s4 = snapshot.get("s4_collectors", {})
    s5 = snapshot.get("s5_alerts", {})
    s6 = snapshot.get("s6_governance", {})

    # S1: Uptime (25%)
    uptime_checks = sum(1 for k, v in s1.items() if isinstance(v, dict) and v.get("ok"))
    uptime_total = sum(1 for k, v in s1.items() if isinstance(v, dict))
    uptime_score = (uptime_checks / uptime_total * 100) if uptime_total else 0

    # S2: Freshness (25%)
    freshness_score = s2.get("freshness_pct", 0)

    # S4: Collectors (20%)
    collector_score = s4.get("health_pct", 0)

    # S5: Alerts (15%) — currently just "are they working"
    alert_score = 100 if s5.get("ok") else 0

    # S6: Governance (15%)
    gov = s6.get("checks_passed", 0)
    gov_total = s6.get("checks_total", 1)
    gov_score = (gov / gov_total * 100) if gov_total else 0

    health = (
        uptime_score * 0.25 +
        freshness_score * 0.25 +
        collector_score * 0.20 +
        alert_score * 0.15 +
        gov_score * 0.15
    )

    grade = "C"
    if health >= 95:
        grade = "AAA"
    elif health >= 90:
        grade = "AA"
    elif health >= 80:
        grade = "A"
    elif health >= 70:
        grade = "B"

    return {
        "total": round(health, 1),
        "grade": grade,
        "components": {
            "uptime": round(uptime_score, 1),
            "freshness": round(freshness_score, 1),
            "collectors": round(collector_score, 1),
            "alerts": round(alert_score, 1),
            "governance": round(gov_score, 1),
        },
    }


if __name__ == "__main__":
    print("Collecting stability snapshot...")
    snap = collect_snapshot()

    # Assign day number from existing snapshots
    existing = sorted(STABILITY_DIR.glob("*_snapshot.json")) if STABILITY_DIR.exists() else []
    snap["day"] = len(existing) + 1

    health = compute_health(snap)
    snap["health"] = health

    STABILITY_DIR.mkdir(parents=True, exist_ok=True)
    ts = snap["ts"].replace(":", "").replace("T", "_")[:15]
    path = STABILITY_DIR / f"{ts}_snapshot.json"
    path.write_text(json.dumps(snap, indent=2))

    print(f"Day {snap['day']} — Health: {health['total']:.1f}% ({health['grade']})")
    print(f"  Uptime: {health['components']['uptime']:.0f}% | Freshness: {health['components']['freshness']:.0f}% | Collectors: {health['components']['collectors']:.0f}%")
    print(f"  Alerts: {health['components']['alerts']:.0f}% | Governance: {health['components']['governance']:.0f}%")
    print(f"  Saved: {path}")
