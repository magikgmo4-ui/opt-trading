"""
Consumer: Data Center market_metrics.v1 -> Google Sheets 'market_metrics' tab.

Reads: data/data_center/views/market_metrics/latest.json (or by_symbol/<SYM>.json)
Maps:  metrics from market_metrics.v1 payload -> rows for Sheets market_metrics tab
Writes: via SheetsWriter (FakeSheetsClient in tests, real API blocked by default)

Data Center remains the canonical source. Sheets is an export/reporting surface.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .sheets_writer import SheetsWriter, WriteResult

_DC_MM_LATEST = Path("data/data_center/views/market_metrics/latest.json")
SOURCE_REF_LATEST = "data/data_center/views/market_metrics/latest.json"


@dataclass
class ConsumerResult:
    ok: bool
    rows_written: int
    rows_attempted: int
    source_path: str
    mode: str
    error: str | None = None


def _load_mm_v1(source_path: Path) -> dict | None:
    """Load and basic-validate a market_metrics.v1 file. Returns None on any failure."""
    if not source_path.exists():
        return None
    try:
        data = json.loads(source_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if data.get("input_class") != "market_metrics.v1":
        return None
    return data


def map_mm_v1_to_rows(payload: dict, source_ref: str) -> list[dict]:
    """Map a market_metrics.v1 dict to Sheets market_metrics rows.

    Only metrics present in provider_coverage.collectable_metrics and with
    non-None values are emitted. One row per metric per symbol.
    """
    symbol = payload.get("symbol", "UNKNOWN")
    as_of = payload.get("metrics_ts", "")
    coverage = payload.get("provider_coverage", {})
    collectable = set(coverage.get("collectable_metrics", []))
    metrics = payload.get("metrics", {})

    rows: list[dict] = []
    for metric_name, value in metrics.items():
        if value is None or metric_name not in collectable:
            continue
        rows.append({
            "as_of": as_of,
            "symbol": symbol,
            "metric_name": metric_name,
            "value": value,
            "source_ref": source_ref,
        })
    return rows


def write_market_metrics_to_sheets(
    writer: SheetsWriter,
    source_path: Path | None = None,
    *,
    root: Path | None = None,
) -> ConsumerResult:
    """Read market_metrics.v1 from Data Center and write rows to Sheets.

    Parameters
    ----------
    writer : SheetsWriter
        Configured writer (fake, dry_run, or controlled_write).
    source_path : Path, optional
        Override the default latest.json path (testing or multi-symbol feeds).
        Relative paths are resolved from root.
    root : Path, optional
        Project root override (tests use temp dirs).

    Returns
    -------
    ConsumerResult with ok=True and mode="no_source" when the file is absent
    (silent-empty fallback — same contract as desk_pro consumer).
    """
    _root = Path(root) if root is not None else Path(__file__).resolve().parent.parent.parent

    if source_path is None:
        resolved = _root / _DC_MM_LATEST
        source_ref = SOURCE_REF_LATEST
    else:
        resolved = source_path if source_path.is_absolute() else _root / source_path
        try:
            source_ref = resolved.relative_to(_root).as_posix()
        except Exception:
            source_ref = source_path.as_posix()

    payload = _load_mm_v1(resolved)
    if payload is None:
        return ConsumerResult(
            ok=True,
            rows_written=0,
            rows_attempted=0,
            source_path=str(resolved),
            mode="no_source",
        )

    rows = map_mm_v1_to_rows(payload, source_ref)
    if not rows:
        return ConsumerResult(
            ok=True,
            rows_written=0,
            rows_attempted=0,
            source_path=str(resolved),
            mode=writer.mode,
        )

    write_result: WriteResult = writer.write_rows("market_metrics", rows)
    return ConsumerResult(
        ok=write_result.ok,
        rows_written=write_result.rows_written,
        rows_attempted=write_result.rows_attempted,
        source_path=str(resolved),
        mode=write_result.mode,
        error=write_result.error,
    )
