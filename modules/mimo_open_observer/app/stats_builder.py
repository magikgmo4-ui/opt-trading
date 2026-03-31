from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .event_journal import ensure_parent_dir


ACTIVE_WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]


def _safe_avg(values: list[float]) -> Optional[float]:
    if not values:
        return None
    return round(sum(values) / len(values), 4)


def _safe_rate(numerator: int, denominator: int) -> Optional[float]:
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)


def _wins_deltas(
    events: list[dict], horizon: str
) -> tuple[int, int, list[float]]:
    """Return (wins, total_with_outcome, deltas)."""
    wins = 0
    total = 0
    deltas = []
    for e in events:
        outcome = e.get(f"outcome_{horizon}")
        delta = e.get(f"delta_{horizon}")
        if outcome is None:
            continue
        total += 1
        if outcome == "win":
            wins += 1
        if delta is not None:
            deltas.append(delta)
    return wins, total, deltas


def build_stats(enriched_events: list[dict]) -> dict:
    total_windows = len(enriched_events)
    signals = [e for e in enriched_events if e.get("fvg_detected")]
    no_events = [e for e in enriched_events if not e.get("fvg_detected")]
    total_signals = len(signals)
    total_no_event = len(no_events)

    # --- summary ---
    w30, t30, d30 = _wins_deltas(signals, "30m")
    w60, t60, d60 = _wins_deltas(signals, "60m")

    summary = {
        "total_windows": total_windows,
        "total_signals": total_signals,
        "total_no_event": total_no_event,
        "signal_rate": _safe_rate(total_signals, total_windows),
        "winrate_30m": _safe_rate(w30, t30),
        "winrate_60m": _safe_rate(w60, t60),
        "avg_delta_30m": _safe_avg(d30),
        "avg_delta_60m": _safe_avg(d60),
    }

    # --- by_direction ---
    by_direction = {}
    for direction in ("bullish", "bearish"):
        group = [e for e in signals if e.get("fvg_direction") == direction]
        w30, t30, d30 = _wins_deltas(group, "30m")
        w60, t60, d60 = _wins_deltas(group, "60m")
        by_direction[direction] = {
            "count": len(group),
            "winrate_30m": _safe_rate(w30, t30),
            "winrate_60m": _safe_rate(w60, t60),
            "avg_delta_30m": _safe_avg(d30),
            "avg_delta_60m": _safe_avg(d60),
        }

    # --- by_sweep ---
    by_sweep = {}
    for label, value in [("sweep_true", True), ("sweep_false", False)]:
        group = [e for e in signals if e.get("sweep") == value]
        w30, t30, _ = _wins_deltas(group, "30m")
        w60, t60, _ = _wins_deltas(group, "60m")
        by_sweep[label] = {
            "count": len(group),
            "winrate_30m": _safe_rate(w30, t30),
            "winrate_60m": _safe_rate(w60, t60),
        }

    # --- by_weekday ---
    by_weekday = {}
    for day in ACTIVE_WEEKDAYS:
        group = [e for e in signals if e.get("weekday") == day]
        w30, t30, _ = _wins_deltas(group, "30m")
        w60, t60, _ = _wins_deltas(group, "60m")
        by_weekday[day] = {
            "count": len(group),
            "winrate_30m": _safe_rate(w30, t30),
            "winrate_60m": _safe_rate(w60, t60),
        }

    return {
        "summary": summary,
        "by_direction": by_direction,
        "by_sweep": by_sweep,
        "by_weekday": by_weekday,
    }


def write_reports(stats: dict, reports_dir: str | Path) -> None:
    reports_dir = Path(reports_dir)
    ensure_parent_dir(reports_dir / "placeholder")

    mapping = {
        "stats_summary.json": stats.get("summary", {}),
        "stats_by_direction.json": stats.get("by_direction", {}),
        "stats_by_sweep.json": stats.get("by_sweep", {}),
        "stats_by_weekday.json": stats.get("by_weekday", {}),
    }

    for filename, data in mapping.items():
        path = reports_dir / filename
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
