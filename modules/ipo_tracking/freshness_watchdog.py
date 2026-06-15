"""
SPCX Freshness Watchdog
GO_SPACEX_OPS_READINESS_LIVE_01

Monitors data freshness across all SPCX pipeline components.
If any critical source is stale beyond threshold, triggers degraded mode
which caps trade_ready and can send Telegram warnings.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]

# Staleness thresholds (seconds)
DEFAULT_THRESHOLDS = {
    "snapshot": 600,        # 10 min
    "orderflow_bucket": 600, # 10 min
    "webhook_event": 1800,  # 30 min
    "price": 300,           # 5 min
    "ownership": 86400,     # 24h (SEC data is slow)
}


def check_freshness(
    snapshot_path: str | None = None,
    bucket_path: str | None = None,
    events_path: str | None = None,
) -> dict[str, Any]:
    """Check freshness of all pipeline data sources.

    Returns dict with per-source age + degraded flag for downstream consumers.
    """
    now = datetime.now(timezone.utc)
    result = {
        "checked_at": now.isoformat(),
        "pipeline_state": "healthy",
        "degraded": False,
        "stale_sources": [],
        "ages": {},
        "warnings": [],
    }

    # --- Snapshot freshness ---
    sp = Path(snapshot_path) if snapshot_path else REPO_ROOT / "data" / "ipo" / "spacex" / "scored" / "latest_snapshot.json"
    if sp.exists():
        age = (now - datetime.fromtimestamp(sp.stat().st_mtime, tz=timezone.utc)).total_seconds()
        result["ages"]["snapshot"] = age
        if age > DEFAULT_THRESHOLDS["snapshot"]:
            result["stale_sources"].append("snapshot")
            result["warnings"].append(f"snapshot_stale_{int(age)}s")
    else:
        result["stale_sources"].append("snapshot")
        result["warnings"].append("snapshot_missing")

    # --- Orderflow bucket freshness ---
    bp = Path(bucket_path) if bucket_path else REPO_ROOT / "state" / "ipo" / "spacex" / "orderflow_buckets" / "latest.json"
    if bp.exists():
        age = (now - datetime.fromtimestamp(bp.stat().st_mtime, tz=timezone.utc)).total_seconds()
        result["ages"]["orderflow_bucket"] = age
        if age > DEFAULT_THRESHOLDS["orderflow_bucket"]:
            result["stale_sources"].append("orderflow_bucket")
            result["warnings"].append(f"orderflow_bucket_stale_{int(age)}s")
    else:
        result["stale_sources"].append("orderflow_bucket")
        result["warnings"].append("orderflow_bucket_missing")

    # --- Webhook events freshness ---
    ep = Path(events_path) if events_path else REPO_ROOT / "state" / "events.jsonl"
    if ep.exists():
        age = (now - datetime.fromtimestamp(ep.stat().st_mtime, tz=timezone.utc)).total_seconds()
        result["ages"]["webhook_event"] = age
        if age > DEFAULT_THRESHOLDS["webhook_event"]:
            result["stale_sources"].append("webhook_event")
            result["warnings"].append(f"webhook_event_stale_{int(age)}s")
    else:
        result["stale_sources"].append("webhook_event")
        result["warnings"].append("webhook_event_missing")

    # --- Determine pipeline state ---
    critical_stale = [s for s in result["stale_sources"] if s in ("snapshot", "orderflow_bucket")]
    if len(critical_stale) >= 2:
        result["pipeline_state"] = "degraded"
        result["degraded"] = True
    elif len(result["stale_sources"]) >= 2:
        result["pipeline_state"] = "degraded"
        result["degraded"] = True
    elif result["stale_sources"]:
        result["pipeline_state"] = "warning"

    return result


def apply_degraded_caps(
    scores: dict[str, Any],
    freshness: dict[str, Any],
    max_trade_ready_degraded: float = 40.0,
) -> dict[str, Any]:
    """Apply trade_ready caps if pipeline is degraded.

    In degraded mode, trade_ready is capped at max_trade_ready_degraded
    to prevent false A/A+ signals on stale/incomplete data.
    """
    if not freshness.get("degraded"):
        return scores

    if isinstance(scores, dict):
        scores = dict(scores)
        if "trade_ready" in scores:
            original = scores["trade_ready"]
            scores["trade_ready"] = min(float(original), max_trade_ready_degraded)
            scores["trade_ready_capped"] = True
            scores["trade_ready_original"] = original
        scores["degraded_mode"] = True
        scores["stale_sources"] = freshness.get("stale_sources", [])
    return scores
