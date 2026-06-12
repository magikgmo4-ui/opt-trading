"""SPCX V2 — Google Sheets export: A+ and A candidates journal."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from modules.spcx_v2.paper_logger import list_candidates
from modules.spcx_v2.config import OUTPUT_DIR
from shared.logger import setup_logger

logger = setup_logger("spcx_v2.export_sheets")


def _candidate_to_row(candidate) -> dict:
    return {
        "ts": candidate.ts,
        "symbol": candidate.symbol,
        "setup_type": candidate.setup_type,
        "grade": candidate.grade,
        "entry_zone": candidate.entry_zone,
        "invalidation": candidate.invalidation,
        "trade_ready": candidate.scores.trade_ready,
        "liquidity": candidate.scores.liquidity,
        "risk": candidate.scores.risk,
        "smart_money": candidate.scores.smart_money,
        "catalyst": candidate.scores.catalyst,
        "reason_codes": ",".join(candidate.reason_codes),
        "r_multiple": candidate.r_multiple,
        "hit_tp1": candidate.hit_tp1,
        "hit_tp2": candidate.hit_tp2,
        "hit_sl": candidate.hit_sl,
        "status": "paper_only",
    }


def build_export_rows(grade_filter: Optional[list] = None) -> list[dict]:
    if grade_filter is None:
        grade_filter = ["A+", "A"]

    candidates = [c for c in list_candidates() if c.grade in grade_filter]
    return [_candidate_to_row(c) for c in candidates]


def export_to_jsonl(path: Optional[str] = None) -> Path:
    rows = build_export_rows()
    if path:
        out = Path(path)
    else:
        out = OUTPUT_DIR / "sheets_export.jsonl"

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "a") as f:
        for row in rows:
            f.write(json.dumps(row, default=str) + "\n")

    logger.info("exported %d rows to %s", len(rows), out)
    return out


def export_to_csv(path: Optional[str] = None) -> Path:
    import csv
    rows = build_export_rows()
    if path:
        out = Path(path)
    else:
        out = OUTPUT_DIR / "sheets_export.csv"

    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        with open(out, "w", newline="") as f:
            pass
        return out

    fieldnames = list(rows[0].keys())
    with open(out, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if out.stat().st_size == 0:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)

    logger.info("exported %d rows to %s (CSV)", len(rows), out)
    return out
