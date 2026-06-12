from __future__ import annotations
from typing import Any
from statistics import mean

from .io import utc_now


SOURCE_HEALTH_BASELINE: dict[str, dict[str, Any]] = {
    "yahoo_chart": {"max_staleness_s": 300, "min_events_per_cycle": 1, "critical": True},
    "sec_edgar": {"max_staleness_s": 86400, "min_events_per_cycle": 1, "critical": False},
    "yahoo_news_rss": {"max_staleness_s": 3600, "min_events_per_cycle": 1, "critical": False},
    "tradingview_webhook": {"max_staleness_s": 600, "min_events_per_cycle": 1, "critical": True},
    "bot_vision_adapter": {"max_staleness_s": 1200, "min_events_per_cycle": 1, "critical": False},
}


def audit_sources(events: list[dict[str, Any]]) -> dict[str, Any]:
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    results = {}
    alerts = []

    for src, baseline in SOURCE_HEALTH_BASELINE.items():
        src_events = [e for e in events if e.get("source") == src]
        ok_events = [e for e in src_events if e.get("ok")]

        latest_ct = None
        for e in src_events:
            ct = e.get("collected_at")
            if ct:
                latest_ct = ct

        age_s = None
        is_stale = False
        if latest_ct:
            try:
                age_s = (now - datetime.fromisoformat(latest_ct.replace("Z", "+00:00"))).total_seconds()
                is_stale = age_s > baseline["max_staleness_s"]
            except (ValueError, TypeError):
                pass

        status = "OK"
        if not src_events:
            status = "MISSING"
            if baseline["critical"]:
                alerts.append(f"CRITICAL: {src} has no events at all")
        elif is_stale:
            status = "STALE"
            if baseline["critical"]:
                alerts.append(f"WARNING: {src} is stale ({age_s:.0f}s > {baseline['max_staleness_s']}s limit)")
        elif sum(1 for e in src_events if not e.get("ok")) > len(src_events) * 0.5:
            status = "DEGRADED"
            alerts.append(f"WARNING: {src} error rate > 50%")

        results[src] = {
            "status": status,
            "events_total": len(src_events),
            "events_ok": len(ok_events),
            "error_rate_pct": round((1 - len(ok_events) / max(1, len(src_events))) * 100, 1),
            "latest_collected_at": latest_ct,
            "age_seconds": round(age_s, 1) if age_s else None,
            "is_stale": is_stale,
            "is_critical": baseline["critical"],
        }

    critical_failures = sum(1 for r in results.values() if r["status"] == "MISSING" and r["is_critical"])
    stale_critical = sum(1 for r in results.values() if r["status"] == "STALE" and r["is_critical"])

    return {
        "audited_at": utc_now(),
        "sources": results,
        "total_sources": len(results),
        "healthy_sources": sum(1 for r in results.values() if r["status"] == "OK"),
        "degraded_sources": sum(1 for r in results.values() if r["status"] in ("DEGRADED", "STALE")),
        "missing_sources": sum(1 for r in results.values() if r["status"] == "MISSING"),
        "critical_failures": critical_failures,
        "stale_critical_sources": stale_critical,
        "alerts": alerts,
        "pipeline_healthy": critical_failures == 0 and stale_critical == 0,
    }


def audit_features(enriched_snapshots: list[dict[str, Any]], window: int = 10) -> dict[str, Any]:
    if not enriched_snapshots:
        return {"ok": False, "error": "no enriched data"}

    recent = enriched_snapshots[-window:]
    indicators_sample = recent[0].get("indicators", {}) if recent else {}
    smart_money_sample = recent[0].get("smart_money", {}) if recent else {}

    drift_report = {}
    all_keys = {**indicators_sample, **smart_money_sample}

    for key in all_keys:
        values = []
        for snap in recent:
            for domain in ["indicators", "smart_money"]:
                val = (snap.get(domain) or {}).get(key)
                if val is not None:
                    if isinstance(val, bool):
                        values.append(1.0 if val else 0.0)
                    elif isinstance(val, (int, float)):
                        values.append(float(val))
                    break

        if not values:
            drift_report[key] = {"status": "DEAD", "missing_rate": 1.0}
            continue

        missing_rate = 1.0 - len(values) / len(recent)

        if missing_rate > 0.8:
            status = "DEAD"
        elif missing_rate > 0.3:
            status = "SPARSE"
        elif len(values) >= 3 and max(values) - min(values) == 0:
            status = "STUCK"
        else:
            status = "ACTIVE"

        drift_report[key] = {
            "status": status,
            "missing_rate": round(missing_rate, 3),
            "sample_count": len(values),
            "avg_value": round(mean(values), 4) if values else None,
        }

    dead = [k for k, v in drift_report.items() if v["status"] == "DEAD"]
    stuck = [k for k, v in drift_report.items() if v["status"] == "STUCK"]
    sparse = [k for k, v in drift_report.items() if v["status"] == "SPARSE"]

    return {
        "audited_at": utc_now(),
        "total_features": len(drift_report),
        "active_features": sum(1 for v in drift_report.values() if v["status"] == "ACTIVE"),
        "dead_features": len(dead),
        "dead_list": dead,
        "stuck_features": len(stuck),
        "stuck_list": stuck,
        "sparse_features": len(sparse),
        "sparse_list": sparse,
        "features": drift_report,
    }
