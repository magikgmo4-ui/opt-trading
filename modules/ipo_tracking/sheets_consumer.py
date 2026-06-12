from __future__ import annotations
from pathlib import Path
from typing import Any
from dataclasses import dataclass

from modules.ipo_tracking.io import REPO_ROOT, utc_now, read_json


@dataclass
class ConsumerResult:
    ok: bool
    rows_written: int
    tab: str
    mode: str
    error: str | None = None


def read_spacex_snapshot() -> dict[str, Any]:
    spath = REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json"
    return read_json(spath, {})


def map_snapshot_to_rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    as_of = snapshot.get("written_at") or utc_now()
    symbol = snapshot.get("symbol", "SPCX")
    rows = []

    for k, v in (snapshot.get("scores") or {}).items():
        rows.append({
            "as_of": as_of,
            "symbol": symbol,
            "metric_name": k,
            "value": v,
            "source_ref": "spacex_super_desk.v1",
        })

    price = snapshot.get("price")
    if price is not None:
        rows.append({
            "as_of": as_of,
            "symbol": symbol,
            "metric_name": "price",
            "value": price,
            "source_ref": "spacex_super_desk.v1",
        })

    gap = snapshot.get("gap_vs_ipo_pct")
    if gap is not None:
        rows.append({
            "as_of": as_of,
            "symbol": symbol,
            "metric_name": "gap_vs_ipo_pct",
            "value": gap,
            "source_ref": "spacex_super_desk.v1",
        })

    for signal in snapshot.get("signals") or []:
        rows.append({
            "as_of": as_of,
            "symbol": symbol,
            "metric_name": "signal_active",
            "value": signal,
            "source_ref": "spacex_super_desk.v1",
        })

    return rows


def write_spacex_to_sheets() -> ConsumerResult:
    try:
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter
    except ImportError:
        return ConsumerResult(ok=False, rows_written=0, tab="spacex_super_desk", mode="unavailable", error="sheets_writer not available")

    snapshot = read_spacex_snapshot()
    if not snapshot:
        return ConsumerResult(ok=False, rows_written=0, tab="spacex_super_desk", mode="dry_run", error="no snapshot available")

    rows = map_snapshot_to_rows(snapshot)
    writer = SheetsWriter()
    result = writer.write_rows("spacex_super_desk", rows, validate=True)

    return ConsumerResult(
        ok=result.ok,
        rows_written=result.rows_written,
        tab="spacex_super_desk",
        mode=result.mode,
        error=result.error,
    )
