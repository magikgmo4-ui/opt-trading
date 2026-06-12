#!/usr/bin/env python3
"""
runner_tv.py — TradingView runner for the strict worker dispatcher.

Adapts a strict-worker job packet (with task_type=TV_SNAPSHOT or TV_WRITE_GATED)
to a tv_job_v1 packet and calls modules/tradingview_orchestrator/app/tv_runner.py.

Called by openclaw_strict_worker_dispatcher.py — not invoked directly.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT  = Path(__file__).resolve().parents[3]
TV_RUNNER  = REPO_ROOT / "modules" / "tradingview_orchestrator" / "app" / "tv_runner.py"
REPORTS    = REPO_ROOT / "reports" / "tradingview"


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("packet", help="Strict-worker job packet JSON path")
    ap.add_argument("--gate-approved", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sw_packet = json.loads(Path(args.packet).read_text())
    task_type = sw_packet.get("task_type", "")
    job_type  = sw_packet.get("tv_job_type", "snapshot")

    if task_type == "TV_SNAPSHOT" and job_type not in {"snapshot", "alert.list", "screenshot"}:
        job_type = "snapshot"

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    tv_packet = {
        "schema":      "tv_job_v1",
        "id":          f"tv_job_{ts}_{job_type.replace('.','_')}",
        "type":        job_type,
        "params":      sw_packet.get("tv_params", {}),
        "gate":        "approved" if (args.gate_approved or task_type == "TV_SNAPSHOT") else "pending",
        "created_at":  datetime.now(timezone.utc).isoformat(),
        "approved_at": datetime.now(timezone.utc).isoformat() if args.gate_approved else None,
        "approved_by": "openclaw_dispatcher",
        "status":      "approved" if args.gate_approved else "pending",
        "notes":       f"Dispatched from strict worker — task_type={task_type}",
    }

    REPORTS.mkdir(parents=True, exist_ok=True)
    tmp_packet = REPORTS / f"_tmp_{tv_packet['id']}.json"
    tmp_packet.write_text(json.dumps(tv_packet, indent=2))

    cmd = ["python3", str(TV_RUNNER), str(tmp_packet)]
    if args.gate_approved:
        cmd.append("--gate-approved")
    if args.dry_run:
        cmd.append("--dry-run")

    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout)
        if r.stderr:
            print(r.stderr, file=sys.stderr)
        result = {
            "status": "PASS" if r.returncode == 0 else "RUNNER_ERROR",
            "exit_code": r.returncode,
            "output_path": f"reports/tradingview/{tv_packet['id']}_*.json",
        }
        print(json.dumps(result, indent=2))
        sys.exit(r.returncode)
    finally:
        tmp_packet.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
