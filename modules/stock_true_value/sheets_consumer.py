"""Google Sheets consumer for stock_true_value scores — 1x/day, dry-run by default."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCORES_PATH = PROJECT_ROOT / "outputs" / "stock_true_value" / "latest" / "scores.json"


@dataclass
class ConsumerResult:
    ok: bool
    rows_written: int
    tab: str
    mode: str
    error: str | None = None


def read_scores() -> dict:
    if not SCORES_PATH.exists():
        return {}
    return json.loads(SCORES_PATH.read_text())


def map_scores_to_rows(scores: dict) -> list[dict]:
    as_of_raw = scores.get("asof", "")
    # Normalize to ISO UTC Z (validator requires Z suffix)
    if as_of_raw and not as_of_raw.endswith("Z"):
        from datetime import datetime, timezone, timedelta
        try:
            dt = datetime.fromisoformat(as_of_raw)
        except ValueError:
            as_of = as_of_raw
        else:
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            as_of = dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        as_of = as_of_raw
    items = scores.get("items", [])
    rows = []
    for it in items:
        rows.append({
            "as_of": as_of,
            "ticker": it.get("ticker", "?"),
            "grade": it.get("final_grade", "?"),
            "true_value_score": it.get("true_value_score", 0) or 0,
            "hype_score": it.get("hype_score", 0) or 0,
            "risk_score": it.get("risk_score", 0) or 0,
            "confidence_score": it.get("confidence_score", 0) or 0,
            "action_bias": it.get("action_bias", ""),
            "flags": ", ".join(it.get("flags", [])),
            "source_ref": "spacex_true_value.v1",
        })
    return rows


def write_true_value_to_sheets(dry_run: bool = True) -> ConsumerResult:
    try:
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter
    except ImportError:
        return ConsumerResult(ok=False, rows_written=0, tab="spacex_true_value", mode="unavailable", error="sheets_writer not available")

    scores = read_scores()
    if not scores:
        return ConsumerResult(ok=False, rows_written=0, tab="spacex_true_value", mode="dry_run", error="no scores available")

    rows = map_scores_to_rows(scores)
    writer = SheetsWriter(dry_run=dry_run)
    result = writer.clear_and_write("spacex_true_value", rows, validate=True)

    return ConsumerResult(
        ok=result.ok,
        rows_written=result.rows_written,
        tab="spacex_true_value",
        mode=result.mode,
        error=result.error,
    )


if __name__ == "__main__":
    controlled = "--controlled-write" in sys.argv
    dry = not controlled
    result = write_true_value_to_sheets(dry_run=dry)
    print(f"Tab: {result.tab} | Mode: {result.mode} | Rows: {result.rows_written} | OK: {result.ok}")
    if result.error:
        print(f"Error: {result.error}")
