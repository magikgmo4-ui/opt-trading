from __future__ import annotations
import csv
import json
import logging
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.result_tracker.app.schema import TradeRecord
from .schema import WriteResult

log = logging.getLogger("datasheet_writer")

_DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "datasheet"

_CSV_FIELDS = [
    "trade_id", "request_id", "signal_id", "ticker", "action",
    "entry_price", "close_price", "fill_qty", "size_pct",
    "sl", "tp", "gross_pnl", "net_pnl", "fees",
    "duration_s", "outcome", "opened_at", "closed_at", "dry_run",
]


class DatasheetWriter:
    def __init__(self, output_dir: Path | None = None):
        self.output_dir = output_dir or _DEFAULT_OUTPUT_DIR

    def _date_str(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y%m%d")

    def _to_row(self, record: TradeRecord) -> dict:
        d = asdict(record)
        d.pop("meta", None)
        return d

    def write(self, record: TradeRecord, dry_run: bool = True) -> WriteResult:
        if dry_run:
            log.info("dry_run write trade_id=%s skipped", record.trade_id)
            return WriteResult(ok=True, dry_run=True, written=False)

        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            date_str = self._date_str()
            jsonl_path = self.output_dir / f"trades_{date_str}.jsonl"
            csv_path = self.output_dir / f"trades_{date_str}.csv"
            row = self._to_row(record)

            # JSONL — append
            with jsonl_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")

            # CSV — append with header on first write
            write_header = not csv_path.exists()
            with csv_path.open("a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=_CSV_FIELDS, extrasaction="ignore")
                if write_header:
                    writer.writeheader()
                writer.writerow(row)

            log.info(
                "datasheet_writer wrote trade_id=%s jsonl=%s csv=%s",
                record.trade_id, jsonl_path, csv_path,
            )
            return WriteResult(
                ok=True, dry_run=False, written=True,
                jsonl_path=str(jsonl_path), csv_path=str(csv_path),
            )

        except Exception as exc:
            log.error("datasheet_writer error: %s", exc)
            return WriteResult(ok=False, dry_run=False, written=False, error=str(exc))
