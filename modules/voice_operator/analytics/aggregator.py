"""
Voice Operator Analytics — Aggregator
GO_VOICE_OPERATOR_USAGE_ANALYTICS_01

Computes usage statistics from voice_events.jsonl.
Returns dicts ready for dashboard display.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter
from statistics import mean, median

REPO_ROOT = Path(__file__).resolve().parents[3]
EVENTS_PATH = REPO_ROOT / "data" / "logs" / "voice_events.jsonl"


def _read_events() -> list[dict]:
    if not EVENTS_PATH.exists():
        return []
    events = []
    with open(EVENTS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return events


def compute_stats(days: int = 7) -> dict:
    """Compute voice operator usage statistics.

    Args:
        days: Lookback window in days (0 = all time)

    Returns:
        Dict with counts, tops, latencies, errors, sources, tts.
    """
    from datetime import datetime, timezone, timedelta

    events = _read_events()
    if not events:
        return _empty_stats()

    # Filter by time window
    if days > 0:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        events = [e for e in events if _parse_ts(e.get("ts", "")) >= cutoff]

    if not events:
        return _empty_stats()

    # Counts
    commands = [e for e in events if e.get("event") == "voice_command"]
    responses = [e for e in events if e.get("event") == "voice_response"]
    errors = [e for e in events if e.get("event") == "voice_error"]
    tts_events = [e for e in events if e.get("event") == "tts_play"]
    profiles = [e for e in events if e.get("event") == "profile_switch"]

    total_commands = len(commands)
    total_errors = len(errors)
    total_tts = len(tts_events)

    # Top commands
    cmd_counter = Counter(e.get("command", "?") for e in commands)
    top_commands = [{"command": c, "count": n} for c, n in cmd_counter.most_common(10)]

    # Top intents
    intent_counter = Counter(e.get("intent", "?") for e in commands)
    top_intents = [{"intent": i, "count": n} for i, n in intent_counter.most_common(8)]

    # Top profiles
    profile_counter = Counter(e.get("profile", "default") for e in profiles)
    top_profiles = [{"profile": p, "count": n} for p, n in profile_counter.most_common(7)]

    # Latencies
    latencies = [e.get("latency_ms", 0) for e in responses if e.get("latency_ms")]
    avg_latency = int(mean(latencies)) if latencies else 0
    med_latency = int(median(latencies)) if latencies else 0
    max_latency = max(latencies) if latencies else 0
    p95_latency = _percentile(latencies, 95) if latencies else 0

    # Source health
    source_counter = Counter(e.get("source", "?") for e in responses)
    source_health = {}
    for src, count in source_counter.most_common():
        err_count = len([e for e in errors if e.get("intent") in [r.get("intent") for r in responses if r.get("source") == src]])
        source_health[src] = {"responses": count, "errors": err_count}

    # TTS ratio
    tts_ratio = round(total_tts / total_commands * 100, 1) if total_commands else 0

    # Errors by type
    error_types = Counter(e.get("error", "?")[:50] for e in errors)

    return {
        "window_days": days,
        "total_commands": total_commands,
        "total_errors": total_errors,
        "error_rate_pct": round(total_errors / (total_commands + total_errors) * 100, 1) if (total_commands + total_errors) else 0,
        "total_tts": total_tts,
        "tts_ratio_pct": tts_ratio,
        "top_commands": top_commands,
        "top_intents": top_intents,
        "top_profiles": top_profiles if top_profiles else [{"profile": "default", "count": total_commands}],
        "latency": {
            "avg_ms": avg_latency,
            "median_ms": med_latency,
            "max_ms": max_latency,
            "p95_ms": p95_latency,
        },
        "source_health": source_health,
        "top_errors": [{"error": e, "count": n} for e, n in error_types.most_common(5)],
    }


def _empty_stats() -> dict:
    return {
        "window_days": 0,
        "total_commands": 0,
        "total_errors": 0,
        "error_rate_pct": 0,
        "total_tts": 0,
        "tts_ratio_pct": 0,
        "top_commands": [],
        "top_intents": [],
        "top_profiles": [],
        "latency": {"avg_ms": 0, "median_ms": 0, "max_ms": 0, "p95_ms": 0},
        "source_health": {},
        "top_errors": [],
    }


def _parse_ts(ts: str):
    from datetime import datetime, timezone
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)


def _percentile(data: list, p: float) -> float:
    if not data:
        return 0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * p / 100.0
    f = int(k)
    c = k - f
    if f + 1 < len(sorted_data):
        return sorted_data[f] + c * (sorted_data[f + 1] - sorted_data[f])
    return sorted_data[f]
