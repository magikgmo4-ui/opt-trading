"""
Sheets adapter for DatasheetWriter — writes TradeRecord to Google Sheets strategy_events tab.

Maps TradeRecord to a strategy_events row:
  event_id    = trade_id
  event_type  = "trade_result.v1"
  event_ts    = closed_at (normalized to ISO UTC Z)
  ticker      = ticker
  outcome     = outcome
  net_pnl     = net_pnl
  payload_ref = path to JSONL output (or "" if not available)

No Google Sheets API calls by default. Dry-run/fake behavior follows SheetsWriter.mode.
Validation R1-R10 applied by SheetsWriter before any write.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.google_sheets_global_schema.sheets_writer import SheetsWriter, WriteResult
from modules.result_tracker.app.schema import TradeRecord

_ISO_OFFSET_RE = re.compile(r"\+00:00$")
_MICROSECONDS_RE = re.compile(r"\.\d+(?=[Z+])")


@dataclass
class SheetsAdapterResult:
    ok: bool
    rows_written: int
    mode: str   # "fake" | "dry_run" | "controlled_write"
    error: str | None = None


def _to_iso_utc_z(ts: str) -> str:
    """Normalize ISO 8601 timestamp to YYYY-MM-DDTHH:MM:SSZ (R5 format).

    Strips sub-second precision and converts +00:00 offset to Z suffix.
    """
    ts = _MICROSECONDS_RE.sub("", ts)
    return _ISO_OFFSET_RE.sub("Z", ts)


def map_trade_to_event_row(record: TradeRecord, payload_ref: str = "") -> dict:
    """Map a TradeRecord to a Sheets strategy_events row dict.

    Returns a dict with all required strategy_events columns plus optional fields.
    timestamp is normalized to ISO UTC Z format required by R1-R10.
    """
    return {
        "event_id": record.trade_id,
        "event_type": "trade_result.v1",
        "event_ts": _to_iso_utc_z(record.closed_at),
        "ticker": record.ticker,
        "outcome": record.outcome,
        "net_pnl": record.net_pnl,
        "payload_ref": payload_ref,
    }


def write_trade_to_sheets(
    record: TradeRecord,
    writer: SheetsWriter,
    payload_ref: str = "",
) -> SheetsAdapterResult:
    """Write a TradeRecord to the strategy_events Sheets tab via SheetsWriter.

    Parameters
    ----------
    record : TradeRecord
        Completed trade record from ResultTracker.
    writer : SheetsWriter
        Configured writer (fake, dry_run, or controlled_write).
    payload_ref : str
        Relative path to the JSONL datasheet output for this record.
        Used as payload_ref (R8-safe: path, not a JSON payload).

    Returns SheetsAdapterResult reflecting write mode and outcome.
    """
    row = map_trade_to_event_row(record, payload_ref)
    result: WriteResult = writer.write_rows("strategy_events", [row])
    return SheetsAdapterResult(
        ok=result.ok,
        rows_written=result.rows_written,
        mode=result.mode,
        error=result.error,
    )
