#!/usr/bin/env python3
"""
Google Sheets controlled sync for daily session journal.

Usage:
  python scripts/sheets/sync_daily_session.py [--run-id ID|--latest] [--controlled-write]

Environment:
  GOOGLE_SHEETS_CREDENTIALS_JSON  — service account JSON (required for controlled-write)
  GOOGLE_SHEETS_SYNC_SHEET_ID     — target sheet ID (required for controlled-write)

Output:
  - dry-run preview to stdout
  - sync log to data/journal/sync_log.jsonl
  - (controlled-write) appends row to Google Sheets
"""
from __future__ import annotations
import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
JOURNAL_DIR = PROJECT_ROOT / "data" / "journal" / "daily"
SYNC_LOG = PROJECT_ROOT / "data" / "journal" / "sync_log.jsonl"

COLUMNS = [
    "run_id", "date", "signal", "side", "ticker",
    "action", "confidence", "verdict", "exec_status",
    "fill_price", "outcome", "net_pnl", "datasheet_written",
    "bridge_status", "brick_stored", "tmux_before", "tmux_after",
    "localcms_before_ok", "localcms_after_ok", "closeout_acknowledged",
    "duration_s", "all_ok",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
log = logging.getLogger("sync_daily_session")


def _load_journal(run_id: str) -> dict:
    path = JOURNAL_DIR / f"{run_id}.json"
    if not path.exists():
        log.error("Journal entry not found: %s", path)
        sys.exit(1)
    return json.loads(path.read_text())


def _find_latest() -> str | None:
    files = sorted(JOURNAL_DIR.glob("*.json"), reverse=True)
    if not files:
        log.error("No journal entries found in %s", JOURNAL_DIR)
        sys.exit(1)
    return json.loads(files[0].read_text()).get("run_id", files[0].stem)


def _extract_row(entry: dict) -> dict:
    signal = entry.get("signal_source", {})
    proposition = entry.get("proposition_summary", {})
    pnl = entry.get("pnl_paper", {})
    tmux_before = entry.get("tmux_before", {})
    tmux_after = entry.get("tmux_after", {})
    lcms_before = entry.get("localcms_before", {})
    lcms_after = entry.get("localcms_after", {})
    ds = entry.get("datasheet_writer", {})
    lf = entry.get("learning_feeder", {})
    started = entry.get("started_at", "")[:10] if entry.get("started_at") else ""

    lcms_before_ok = sum(1 for v in lcms_before.values() if isinstance(v, dict) and v.get("ok")) if lcms_before else 0
    lcms_before_total = len(lcms_before) if lcms_before else 0
    lcms_after_ok = sum(1 for v in lcms_after.values() if isinstance(v, dict) and v.get("ok")) if lcms_after else 0
    lcms_after_total = len(lcms_after) if lcms_after else 0

    return {
        "run_id": entry.get("run_id", ""),
        "date": started,
        "signal": f"{signal.get('signal', '')} {signal.get('symbol', '')}".strip(),
        "side": signal.get("signal", ""),
        "ticker": signal.get("symbol", ""),
        "action": proposition.get("action", ""),
        "confidence": proposition.get("confidence", ""),
        "verdict": entry.get("validation_verdict", ""),
        "exec_status": entry.get("trade_executor_status", ""),
        "fill_price": pnl.get("fill_price", ""),
        "outcome": pnl.get("outcome", ""),
        "net_pnl": pnl.get("net_pnl", ""),
        "datasheet_written": ds.get("written", False),
        "bridge_status": lf.get("bridge_status", ""),
        "brick_stored": lf.get("brick_stored", False),
        "tmux_before": tmux_before.get("count", ""),
        "tmux_after": tmux_after.get("count", ""),
        "localcms_before_ok": f"{lcms_before_ok}/{lcms_before_total}" if lcms_before_total else "",
        "localcms_after_ok": f"{lcms_after_ok}/{lcms_after_total}" if lcms_after_total else "",
        "closeout_acknowledged": entry.get("closeout_acknowledged", False),
        "duration_s": entry.get("duration_s", ""),
        "all_ok": entry.get("all_ok", ""),
    }


def _row_values(row: dict) -> list[str]:
    vals = []
    for col in COLUMNS:
        v = row.get(col, "")
        if isinstance(v, bool):
            vals.append("YES" if v else "NO")
        elif isinstance(v, float):
            vals.append(f"{v:.4f}" if v else "")
        elif v is None:
            vals.append("")
        else:
            vals.append(str(v))
    return vals


def _try_get_sheets_client():
    creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")
    sheet_id = os.environ.get("GOOGLE_SHEETS_SYNC_SHEET_ID")
    if not creds_json or not sheet_id:
        return None, None
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).sheet1
        return client, sheet
    except Exception as e:
        log.warning("Sheets client init failed: %s", e)
        return None, None


def _append_row(sheet, values: list[str]) -> bool:
    try:
        sheet.append_row(values)
        return True
    except Exception as e:
        log.error("Sheets append failed: %s", e)
        return False


def _log_sync(run_id: str, mode: str, status: str, row: dict | None = None) -> None:
    SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "mode": mode,
        "status": status,
        "row": row,
    }
    with open(SYNC_LOG, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


def _read_sync_status(run_id: str) -> dict | None:
    if not SYNC_LOG.exists():
        return None
    last = None
    with open(SYNC_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("run_id") == run_id:
                    last = entry
            except json.JSONDecodeError:
                continue
    return last


def main() -> dict:
    parser = argparse.ArgumentParser(description="Google Sheets controlled sync for daily session journal")
    parser.add_argument("--run-id", help="Specific run_id to sync")
    parser.add_argument("--latest", action="store_true", help="Sync latest journal entry")
    parser.add_argument("--controlled-write", action="store_true",
                        help="Actually write to Google Sheets (dry-run by default)")
    parser.add_argument("--check-status", metavar="RUN_ID", help="Check sync status for a run_id")
    args = parser.parse_args()

    if args.check_status:
        status = _read_sync_status(args.check_status)
        if status:
            print(json.dumps(status, indent=2, default=str))
        else:
            print(json.dumps({"run_id": args.check_status, "status": "not_found"}))
        return status or {"run_id": args.check_status, "status": "not_found"}

    if args.run_id and args.latest:
        log.error("Use --run-id OR --latest, not both")
        sys.exit(1)

    run_id = args.run_id or _find_latest()
    entry = _load_journal(run_id)
    row = _extract_row(entry)
    values = _row_values(row)

    dry_run = not args.controlled_write
    mode = "dry_run" if dry_run else "controlled_write"

    print("=" * 60)
    print(f"GOOGLE SHEETS SYNC — {run_id}")
    print("=" * 60)
    print(f"Mode     : {mode}")
    print(f"Run ID   : {run_id}")
    print(f"Date     : {row['date']}")
    print(f"Signal   : {row['signal']}")
    print(f"Verdict  : {row['verdict']}")
    print(f"Outcome  : {row['outcome']} net={row['net_pnl']}")
    print(f"Closeout : {row['closeout_acknowledged']}")
    print()
    print("── Row preview (columns → values) ──")
    for col, val in zip(COLUMNS, values):
        print(f"  {col:25s} = {val}")
    print()

    if dry_run:
        client, sheet = None, None
        _log_sync(run_id, mode, "dry_run_skipped", row)
        print("⚠ DRY-RUN — no write to Google Sheets.")
        print("  Use --controlled-write to actually sync.")
        print("=" * 60)
        if not os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON"):
            print("  Note: set GOOGLE_SHEETS_CREDENTIALS_JSON and GOOGLE_SHEETS_SYNC_SHEET_ID")
            print("  for controlled-write mode.")
        print("=" * 60)
        result = {"run_id": run_id, "mode": mode, "status": "dry_run_skipped", "row": row}
        return result

    client, sheet = _try_get_sheets_client()
    if sheet is None:
        _log_sync(run_id, mode, "failed_no_credentials", row)
        log.error("Cannot write: Google Sheets credentials or sheet ID not configured.")
        log.error("Set GOOGLE_SHEETS_CREDENTIALS_JSON and GOOGLE_SHEETS_SYNC_SHEET_ID.")
        sys.exit(1)

    ok = _append_row(sheet, values)
    status = "synced" if ok else "failed"
    _log_sync(run_id, mode, status, row)
    if ok:
        print(f"✓ Row appended to Google Sheets (sheet_id={os.environ.get('GOOGLE_SHEETS_SYNC_SHEET_ID', '?')})")
    else:
        print("✗ Failed to append row to Google Sheets")
    print("=" * 60)

    return {"run_id": run_id, "mode": mode, "status": status, "row": row}


if __name__ == "__main__":
    result = main()
    ok = result.get("status") in ("dry_run_skipped", "synced")
    sys.exit(0 if ok else 1)
