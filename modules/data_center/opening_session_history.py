from __future__ import annotations

"""Opening Session history logger — persists opening metrics for calibration.

For every opening event, logs:
    - timestamp (heure)
    - price (prix)
    - event type (événement)
    - scores (risk, continuation, exhaustion)
    - outcome at +5 min, +15 min, +30 min, +1h

Stored as JSONL in state/opening_session_history.jsonl.
Feeds the reliability calibrator (existing infrastructure).

Monitor-only — no broker calls, no order execution.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_DEFAULT_HISTORY_PATH = Path("state/opening_session_history.jsonl")


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat() + "Z"


def log_opening_event(
    event: dict[str, Any],
    opening_metrics: dict[str, Any],
    score_result: dict[str, Any],
    history_path: Path | str | None = None,
) -> dict[str, Any]:
    """Log a single opening session event to the history JSONL file.

    Args:
        event: The signal_event.v1 dict that triggered this log.
        opening_metrics: Output of compute_opening_metrics().
        score_result: Output of score_spcx().
        history_path: Path to history file. Defaults to
            state/opening_session_history.jsonl.

    Returns:
        The logged entry dict (also written to disk).
    """
    path = Path(history_path) if history_path else _DEFAULT_HISTORY_PATH

    entry = {
        "_schema": "opening_session_history.v1",
        "timestamp": _iso_now(),
        "event_time": event.get("_ts", _iso_now()),
        "symbol": str(event.get("symbol", "SPCX")).upper(),
        "event": str(event.get("event", "")),
        "price": _safe_float(event.get("price")),
        "score": score_result.get("score", 0),
        "grade": score_result.get("grade", "C"),
        "setup_state": score_result.get("setup_state", "watch"),
        "opening_gap_pct": opening_metrics.get("opening_gap_pct"),
        "opening_drive": opening_metrics.get("opening_drive"),
        "distance_vwap_pct": opening_metrics.get("distance_vwap_pct"),
        "distance_premarket_high_pct": opening_metrics.get(
            "distance_premarket_high_pct"
        ),
        "distance_orb_pct": opening_metrics.get("distance_orb_pct"),
        "risk_score": opening_metrics.get("risk_score", 0),
        "continuation_score": opening_metrics.get("continuation_score", 0),
        "exhaustion_score": opening_metrics.get("exhaustion_score", 0),
        "dynamic_boost": (
            score_result.get("opening_components", {}).get("dynamic_boost", 0)
        ),
        "triggered_events": score_result.get("events", []),
        "risk_notes": score_result.get("risk_notes", []),
        # Outcome fields — to be filled by reliability calibrator
        "outcome_5m": None,
        "outcome_15m": None,
        "outcome_30m": None,
        "outcome_1h": None,
        "monitor_only": True,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(path), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, default=str) + "\n")

    return entry


def read_opening_history(
    limit: int = 100,
    history_path: Path | str | None = None,
) -> list[dict[str, Any]]:
    """Read recent opening session history entries.

    Args:
        limit: Max entries to return (tail).
        history_path: Path to history file.

    Returns:
        List of opening session history entries, most recent first.
    """
    path = Path(history_path) if history_path else _DEFAULT_HISTORY_PATH
    if not path.exists():
        return []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        out: list[dict[str, Any]] = []
        for line in lines[-limit:]:
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
                if isinstance(parsed, dict):
                    out.append(parsed)
            except json.JSONDecodeError:
                continue
        out.reverse()
        return out
    except Exception:
        return []


def update_outcome(
    entry_timestamp: str,
    outcome_field: str,
    outcome_value: Any,
    history_path: Path | str | None = None,
) -> bool:
    """Update an outcome field in a logged entry (for reliability calibrator).

    Args:
        entry_timestamp: The _ts of the entry to update.
        outcome_field: One of "outcome_5m", "outcome_15m", "outcome_30m", "outcome_1h".
        outcome_value: Value to set (e.g. {"price": 175.0, "direction": "up"}).
        history_path: Path to history file.

    Returns:
        True if the entry was found and updated, False otherwise.
    """
    path = Path(history_path) if history_path else _DEFAULT_HISTORY_PATH
    if not path.exists():
        return False

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        updated = False
        new_lines: list[str] = []
        for line in lines:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if isinstance(entry, dict) and entry.get("timestamp") == entry_timestamp:
                    entry[outcome_field] = outcome_value
                    updated = True
                new_lines.append(json.dumps(entry, default=str))
            except json.JSONDecodeError:
                new_lines.append(line)

        if updated:
            path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return updated
    except Exception:
        return False


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
