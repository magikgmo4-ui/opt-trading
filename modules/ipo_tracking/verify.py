from __future__ import annotations
from typing import Any
from .io import utc_now


REQUIRED_RAW_FIELDS: dict[str, list[str]] = {
    "yahoo_chart": ["source", "symbol", "bars", "ok"],
    "sec_edgar": ["source", "filings", "ok"],
    "yahoo_news_rss": ["source", "articles", "ok"],
    "tradingview_webhook": ["source", "ok"],
    "bot_vision_adapter": ["source", "items", "ok"],
}

REQUIRED_NORMALIZED_FIELDS: dict[str, list[str]] = {
    "market_data": ["event_type", "normalized_at", "symbol", "price", "bars_count", "ok"],
    "filing": ["event_type", "normalized_at", "filings_count", "ok"],
    "news": ["event_type", "normalized_at", "articles_count", "ok"],
    "technical_alert": ["event_type", "normalized_at", "symbol", "ok"],
    "vision_context": ["event_type", "normalized_at", "items_count", "ok"],
}

REQUIRED_SCORED_FIELDS = [
    "input_class", "symbol", "scores", "signals",
]
REQUIRED_SCORE_KEYS = [
    "momentum", "news_velocity", "sec_activity",
    "smart_money", "risk", "trade_ready", "accumulation",
]


def validate_raw_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    issues: list[str] = []
    by_source: dict[str, int] = {}
    for i, e in enumerate(events):
        source = e.get("source", "unknown")
        by_source[source] = by_source.get(source, 0) + 1
        required = REQUIRED_RAW_FIELDS.get(source, ["source", "ok"])
        for field in required:
            if field not in e:
                issues.append(f"raw[{i}] source={source} missing field={field!r}")
    return {
        "stage": "raw",
        "verified_at": utc_now(),
        "ok": len(issues) == 0,
        "events_count": len(events),
        "by_source": by_source,
        "issues": issues,
    }


def validate_normalized_events(normalized: list[dict[str, Any]]) -> dict[str, Any]:
    issues: list[str] = []
    by_type: dict[str, int] = {}
    for i, e in enumerate(normalized):
        etype = e.get("event_type", "unknown")
        by_type[etype] = by_type.get(etype, 0) + 1
        required = REQUIRED_NORMALIZED_FIELDS.get(etype, ["event_type", "ok"])
        for field in required:
            if field not in e:
                issues.append(f"normalized[{i}] type={etype} missing field={field!r}")
        if etype == "unknown":
            issues.append(f"normalized[{i}] could not be typed (source={e.get('source')})")
    return {
        "stage": "normalized",
        "verified_at": utc_now(),
        "ok": len(issues) == 0,
        "events_count": len(normalized),
        "by_type": by_type,
        "issues": issues,
    }


def validate_scored_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    for field in REQUIRED_SCORED_FIELDS:
        if field not in snapshot:
            issues.append(f"scored missing field={field!r}")

    scores = snapshot.get("scores", {})
    for key in REQUIRED_SCORE_KEYS:
        if key not in scores:
            issues.append(f"scored.scores missing key={key!r}")
        elif not isinstance(scores.get(key), (int, float)):
            issues.append(f"scored.scores.{key} not numeric: {scores.get(key)!r}")

    signals = snapshot.get("signals", [])
    if not isinstance(signals, list):
        issues.append("scored.signals is not a list")

    return {
        "stage": "scored",
        "verified_at": utc_now(),
        "ok": len(issues) == 0,
        "symbol": snapshot.get("symbol"),
        "score_keys_present": [k for k in REQUIRED_SCORE_KEYS if k in scores],
        "signals_count": len(signals),
        "issues": issues,
    }


def validate_full_pipeline(
    raw_events: list[dict[str, Any]],
    normalized: list[dict[str, Any]],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    raw_v = validate_raw_events(raw_events)
    norm_v = validate_normalized_events(normalized)
    scored_v = validate_scored_snapshot(snapshot)
    all_ok = raw_v["ok"] and norm_v["ok"] and scored_v["ok"]

    return {
        "pipeline_version": "v1",
        "validated_at": utc_now(),
        "ok": all_ok,
        "stages": {
            "raw": raw_v,
            "normalized": norm_v,
            "scored": scored_v,
        },
        "total_issues": len(raw_v["issues"]) + len(norm_v["issues"]) + len(scored_v["issues"]),
    }
