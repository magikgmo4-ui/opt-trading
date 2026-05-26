from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from modules.google_sheets_global_schema.market_metrics_consumer import map_mm_v1_to_rows
from modules.google_sheets_global_schema.sheets_writer import SheetsWriter, WriteResult

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_DC_MM_LATEST = Path("data/data_center/views/market_metrics/latest.json")
_SOURCE_REF_LATEST = "data/data_center/views/market_metrics/latest.json"


@dataclass
class ConsumerResult:
    ok: bool
    rows_written: int
    rows_attempted: int
    source_path: str
    mode: str
    error: str | None = None


def _load_market_metrics_v1_or_raise(source_path: Path) -> dict:
    if not source_path.exists():
        raise FileNotFoundError(str(source_path))
    try:
        data = json.loads(source_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc
    if data.get("input_class") != "market_metrics.v1":
        raise ValueError(f"input_class must be 'market_metrics.v1', got '{data.get('input_class')}'")
    return data


def consume_google_sheets_market_reporting(
    writer: SheetsWriter,
    *,
    root: Optional[Path] = None,
    source_path: Optional[Path] = None,
) -> ConsumerResult:
    root = Path(root) if root is not None else _PROJECT_ROOT

    resolved = (root / _DC_MM_LATEST) if source_path is None else (
        source_path if source_path.is_absolute() else root / source_path
    )
    payload = _load_market_metrics_v1_or_raise(resolved)

    source_ref = _SOURCE_REF_LATEST
    if source_path is not None:
        try:
            source_ref = resolved.relative_to(root).as_posix()
        except Exception:
            source_ref = source_path.as_posix()

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
