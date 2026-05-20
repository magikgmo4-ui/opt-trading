#!/usr/bin/env python3
"""
Daily Session Journal - transforms the E2E dry-run proof into a traceable daily session.

Usage:
  python scripts/e2e/daily_session_journal.py [--controlled-write] [--no-closeout] [--sync-sheets] [--sheets-controlled-write]

Output:
  - JSON report to data/journal/daily/<run_id>.json
  - CSV summary to data/journal/daily/<run_id>.csv
  - Human-readable summary to stdout
"""
from __future__ import annotations
import argparse
import csv
import json
import logging
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
JOURNAL_DIR = PROJECT_ROOT / "data" / "journal" / "daily"
LOCALCMS_BASE = "http://127.0.0.1:8700"
DRY_RUN = os.environ.get("DRY_RUN", "1") == "1"
PAPER_MODE = os.environ.get("PAPER_MODE", "1") == "1"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
log = logging.getLogger("daily_session_journal")


def _ascii_safe(s: str) -> str:
    return s.encode("ascii", "replace").decode("ascii")


def _resolve_run_id() -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    existing = [p.stem for p in JOURNAL_DIR.glob(f"{today}_*.json")]
    seq = 1
    while f"{today}_{seq:03d}" in existing:
        seq += 1
    return f"{today}_{seq:03d}"


def _tmux_snapshot() -> dict:
    try:
        r = subprocess.run(
            ["tmux", "list-sessions", "-F", "#S"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode != 0:
            return {"error": f"tmux rc={r.returncode}", "stderr": r.stderr.strip(), "active": []}
        active = [s.strip() for s in r.stdout.splitlines() if s.strip()]
        return {"timestamp": datetime.now(timezone.utc).isoformat(), "active": sorted(active), "count": len(active)}
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return {"error": str(e), "active": []}


def _localcms_snapshot() -> dict:
    results = {}
    for ep in ["/health", "/menu", "/menu/state", "/runtime/tmux"]:
        try:
            import urllib.request
            r = urllib.request.urlopen(f"{LOCALCMS_BASE}{ep}", timeout=5)
            results[ep] = {"status": r.status, "ok": r.status == 200}
            if r.status == 200:
                body = r.read().decode()
                if ep in ("/health", "/runtime/tmux"):
                    results[ep]["data"] = json.loads(body)
                elif ep == "/menu":
                    data = json.loads(body)
                    domains = [d.get("label") for d in data.get("menu", [])]
                    results[ep]["domain_count"] = len(domains)
                    results[ep]["domains"] = domains
                elif ep == "/menu/state":
                    data = json.loads(body)
                    results[ep]["state_count"] = len(data) if isinstance(data, list) else 0
        except Exception as e:
            results[ep] = {"status": "unreachable", "ok": False, "error": str(e)}
    return results


def _run_pipeline() -> dict:
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from scripts.e2e.dry_run_pipeline import main as pipeline_main
    return pipeline_main()


def _extract_metrics(report: dict) -> dict:
    steps = {s["step"]: s["result"] for s in report.get("steps", [])}

    def get(key: str, default: str = "N/A") -> str:
        return str(steps.get(key, {}).get(key.split("_", 1)[1] if "_" in key else "", default))

    return {
        "signal_side": steps.get("1_signal_router", {}).get("side", "N/A"),
        "signal_ticker": steps.get("1_signal_router", {}).get("ticker", "N/A"),
        "proposition_action": steps.get("2_proposition_engine", {}).get("action", "N/A"),
        "proposition_confidence": steps.get("2_proposition_engine", {}).get("confidence", "N/A"),
        "validation_verdict": steps.get("3_validation_gate", {}).get("verdict", "N/A"),
        "executor_status": steps.get("4_trade_executor", {}).get("status", "N/A"),
        "executor_fill_price": steps.get("4_trade_executor", {}).get("fill_price", "N/A"),
        "tracker_outcome": steps.get("5_result_tracker", {}).get("outcome", "N/A"),
        "tracker_net_pnl": steps.get("5_result_tracker", {}).get("net_pnl", "N/A"),
        "writer_dry_run": steps.get("6_datasheet_writer", {}).get("dry_run", True),
        "writer_written": steps.get("6_datasheet_writer", {}).get("written", False),
        "feeder_bridge_status": steps.get("7_learning_feeder", {}).get("bridge_status", "N/A"),
        "feeder_brick_stored": steps.get("7_learning_feeder", {}).get("brick_stored", False),
        "telegram_dispatch_count": len(steps.get("1c_notification_dispatcher_dry_run", {}).get("dispatch", []) or []),
    }


def _build_human_summary(metrics: dict, report: dict) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append(f"DAILY SESSION JOURNAL - {report.get('run_id', 'N/A')}")
    lines.append("=" * 60)
    lines.append(f"Started : {report.get('started_at', 'N/A')}")
    lines.append(f"Duration: {report.get('duration_s', 'N/A')}s")
    lines.append(f"All OK  : {report.get('all_ok', False)}")
    lines.append("")
    lines.append("-- Signal --")
    lines.append(f"  {metrics.get('signal_side', 'N/A')} {metrics.get('signal_ticker', 'N/A')}")
    lines.append("")
    lines.append("-- Proposition --")
    lines.append(f"  Action={metrics.get('proposition_action', 'N/A')}  "
                  f"Confidence={metrics.get('proposition_confidence', 'N/A')}")
    lines.append("")
    lines.append("-- Validation --")
    lines.append(f"  Verdict={metrics.get('validation_verdict', 'N/A')}")
    lines.append("")
    lines.append("-- Execution --")
    lines.append(f"  Status={metrics.get('executor_status', 'N/A')}  "
                  f"Fill={metrics.get('executor_fill_price', 'N/A')}")
    lines.append("")
    lines.append("-- Result --")
    lines.append(f"  Outcome={metrics.get('tracker_outcome', 'N/A')}  "
                  f"P&L={metrics.get('tracker_net_pnl', 'N/A')}")
    lines.append("")
    lines.append("-- Datasheet --")
    lines.append(f"  Dry-run={metrics.get('writer_dry_run', 'N/A')}  "
                  f"Written={metrics.get('writer_written', 'N/A')}")
    lines.append("")
    lines.append("-- Learning --")
    lines.append(f"  Bridge={metrics.get('feeder_bridge_status', 'N/A')}  "
                  f"Brick={metrics.get('feeder_brick_stored', 'N/A')}")
    lines.append("")
    lines.append("-- Telegram --")
    lines.append(f"  Dispatch previews: {metrics.get('telegram_dispatch_count', 0)}")
    steps = {s["step"]: s["result"] for s in report.get("steps", [])}
    dispatches = steps.get("1c_notification_dispatcher_dry_run", {}).get("dispatch", []) or []
    for d in dispatches[:3]:
        event_type = str(d.get("event_type", ""))
        msg = str(d.get("message", ""))
        msg_one = _ascii_safe(" ".join(msg.split()))
        if msg_one:
            lines.append(f"  {event_type}: {msg_one[:160]}")
    lines.append("")
    if report.get("sheets_sync", {}).get("enabled"):
        lines.append("-- Sheets --")
        ss = report.get("sheets_sync", {})
        lines.append(f"  Mode={ss.get('mode', 'dry_run')}  RC={ss.get('returncode', '?')}")
        lines.append("")
    lines.append("-- TMUX --")
    tmux_before = report.get("tmux_before", {})
    tmux_after = report.get("tmux_after", {})
    lines.append(f"  Before: {tmux_before.get('count', '?')} sessions")
    lines.append(f"  After : {tmux_after.get('count', '?')} sessions")
    lines.append("")
    lines.append("-- LocalCMS --")
    lcms = report.get("localcms", {})
    all_ok = all(v.get("ok", False) for v in lcms.values()) if lcms else False
    lines.append(f"  All endpoints OK: {all_ok}")
    lines.append("")
    closeout = report.get("closeout_acknowledged", False)
    if closeout:
        lines.append("CLOSEOUT ACKNOWLEDGED")
    else:
        lines.append("PENDING CLOSEOUT")
    lines.append("=" * 60)
    return "\n".join(lines)


def _save_json(report: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, default=str))
    log.info("JSON report saved: %s", path)


def _save_csv(metrics: dict, report: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "run_id": report.get("run_id", ""),
        "started_at": report.get("started_at", ""),
        "duration_s": report.get("duration_s", ""),
        "all_ok": report.get("all_ok", ""),
        "signal_side": metrics.get("signal_side", ""),
        "signal_ticker": metrics.get("signal_ticker", ""),
        "proposition_action": metrics.get("proposition_action", ""),
        "proposition_confidence": metrics.get("proposition_confidence", ""),
        "validation_verdict": metrics.get("validation_verdict", ""),
        "executor_status": metrics.get("executor_status", ""),
        "executor_fill_price": metrics.get("executor_fill_price", ""),
        "tracker_outcome": metrics.get("tracker_outcome", ""),
        "tracker_net_pnl": metrics.get("tracker_net_pnl", ""),
        "writer_written": metrics.get("writer_written", ""),
        "feeder_bridge_status": metrics.get("feeder_bridge_status", ""),
        "tmux_sessions_before": report.get("tmux_before", {}).get("count", ""),
        "tmux_sessions_after": report.get("tmux_after", {}).get("count", ""),
        "localcms_ok": report.get("localcms_ok", ""),
        "closeout_acknowledged": report.get("closeout_acknowledged", ""),
    }
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader()
        w.writerow(row)
    log.info("CSV summary saved: %s", path)


def _prompt_closeout() -> bool:
    try:
        ans = input("\nAcknowledge closeout? [Y/n]: ").strip().lower()
        return ans in ("", "y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False


def _sync_google_sheets(run_id: str, controlled_write: bool) -> dict:
    args = [sys.executable, str(PROJECT_ROOT / "scripts" / "sheets" / "sync_daily_session.py"), "--run-id", run_id]
    mode = "dry_run"
    if controlled_write:
        args.append("--controlled-write")
        mode = "controlled_write"
    env = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT)}
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=20, env=env)
        out_lines = (r.stdout or "").splitlines()
        tail = "\n".join(out_lines[-40:]) if out_lines else ""
        return {
            "enabled": True,
            "mode": mode,
            "returncode": r.returncode,
            "stdout_tail": tail,
            "stderr": (r.stderr or "").strip()[:500],
        }
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "").splitlines() if e.stdout else []
        tail = "\n".join(out[-40:]) if out else ""
        return {
            "enabled": True,
            "mode": mode,
            "returncode": "timeout",
            "stdout_tail": tail,
            "stderr": (e.stderr or "").strip()[:500] if e.stderr else "",
        }
    except (FileNotFoundError, OSError, ValueError) as e:
        return {
            "enabled": True,
            "mode": mode,
            "returncode": "error",
            "stdout_tail": "",
            "stderr": str(e)[:500],
        }


def main() -> dict:
    parser = argparse.ArgumentParser(description="Daily Session Journal")
    parser.add_argument("--controlled-write", action="store_true",
                        help="Allow datasheet_writer to actually write")
    parser.add_argument("--no-closeout", action="store_true",
                        help="Skip closeout prompt (for automation)")
    parser.add_argument("--sync-sheets", action="store_true",
                        help="Run Google Sheets sync for this run_id (dry-run by default)")
    parser.add_argument("--sheets-controlled-write", action="store_true",
                        help="Allow Google Sheets append_row (requires ADC + GOOGLE_SHEETS_SYNC_SHEET_ID)")
    args = parser.parse_args()

    run_id = _resolve_run_id()
    log.info("=== Daily Session Journal: %s ===", run_id)

    tmux_before = _tmux_snapshot()
    localcms_before = _localcms_snapshot()

    t0 = time.time()
    pipeline_report = _run_pipeline()
    pipeline_report["run_id"] = run_id

    tmux_after = _tmux_snapshot()
    localcms_after = _localcms_snapshot()

    metrics = _extract_metrics(pipeline_report)
    session_id = str(uuid.uuid4())

    report = {
        "run_id": run_id,
        "session_id": session_id,
        "journal_type": "daily_session",
        "pipeline": "E2E dry-run pipeline daily session journal",
        "controlled_write": args.controlled_write,
        "dry_run": DRY_RUN,
        "paper_mode": PAPER_MODE,
        "started_at": pipeline_report.get("started_at", datetime.now(timezone.utc).isoformat()),
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "duration_s": round(time.time() - t0, 3),
        "pipeline_duration_s": pipeline_report.get("duration_s", 0),
        "all_ok": pipeline_report.get("all_ok", False),
        "steps": pipeline_report.get("steps", []),
        "signal_source": {
            "engine": "e2e_dry_run",
            "signal": metrics.get("signal_side"),
            "symbol": metrics.get("signal_ticker"),
        },
        "proposition_summary": {
            "action": metrics.get("proposition_action"),
            "confidence": metrics.get("proposition_confidence"),
        },
        "validation_verdict": metrics.get("validation_verdict"),
        "trade_executor_status": metrics.get("executor_status"),
        "result_tracker_outcome": metrics.get("tracker_outcome"),
        "pnl_paper": {
            "net_pnl": metrics.get("tracker_net_pnl"),
            "outcome": metrics.get("tracker_outcome"),
        },
        "datasheet_writer": {
            "dry_run": metrics.get("writer_dry_run"),
            "written": metrics.get("writer_written"),
        },
        "learning_feeder": {
            "bridge_status": metrics.get("feeder_bridge_status"),
            "brick_stored": metrics.get("feeder_brick_stored"),
        },
        "tmux_before": tmux_before,
        "tmux_after": tmux_after,
        "localcms": localcms_after,
        "localcms_ok": pipeline_report.get("localcms_ok", False),
        "localcms_before": localcms_before,
        "localcms_after": localcms_after,
        "closeout_required": not args.no_closeout,
        "closeout_acknowledged": False,
    }

    json_path = JOURNAL_DIR / f"{run_id}.json"
    _save_json(report, json_path)

    csv_path = JOURNAL_DIR / f"{run_id}.csv"
    _save_csv(metrics, report, csv_path)

    if args.sync_sheets:
        report["sheets_sync"] = _sync_google_sheets(run_id, controlled_write=args.sheets_controlled_write)
        _save_json(report, json_path)

    summary = _build_human_summary(metrics, report)
    print(summary)

    if not args.no_closeout:
        ack = _prompt_closeout()
        report["closeout_acknowledged"] = ack
        if ack:
            print("Closeout acknowledged. Journal entry finalized.")
            _save_json(report, json_path)
            _save_csv(metrics, report, csv_path)
        else:
            print("Closeout pending — journal saved without acknowledgment.")
    else:
        report["closeout_acknowledged"] = False

    return report


if __name__ == "__main__":
    report = main()
    ok = report.get("all_ok", False) and report.get("closeout_acknowledged", False)
    sys.exit(0 if ok else 1)
