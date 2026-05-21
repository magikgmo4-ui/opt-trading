#!/usr/bin/env python3
"""P8 Scheduler/CI — job queue, retries, dead-letter, alerting.

Usage:
  # List all jobs
  python3 scripts/ai/workers/scheduler_worker.py list

  # Submit a new job
  python3 scripts/ai/workers/scheduler_worker.py submit --action "inventory" --target "repo"

  # Run the scheduler cycle (process pending jobs)
  python3 scripts/ai/workers/scheduler_worker.py run

  # View dead-letter queue
  python3 scripts/ai/workers/scheduler_worker.py dead-letter

  # View alerts
  python3 scripts/ai/workers/scheduler_worker.py alerts
"""

import argparse
import json
import os
import sys
import time
import traceback
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = REPO_ROOT / "data" / "runtime_health" / "ledger" / "events.jsonl"
SCHEDULER_DIR = REPO_ROOT / "data" / "scheduler"
JOBS_DIR = SCHEDULER_DIR / "jobs"
DEAD_LETTER_DIR = SCHEDULER_DIR / "dead_letter"
ALERTS_DIR = SCHEDULER_DIR / "alerts"
OUTPUT_DIR = REPO_ROOT / "reports" / "ai" / "workers"

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = [10, 60, 300]  # 10s, 1min, 5min
JOB_TIMEOUT_SECONDS = 300

# Allowed job actions
ALLOWED_ACTIONS = frozenset({
    "inventory",
    "observe",
    "draft",
    "hitl_gate",
    "bridge_sync",
    "signal_dry_run",
    "health_check",
    "journal_cleanup",
    "report_generate",
})


def log_ledger(event_type, actor, surface, action, status, payload=None):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "event_id": uuid.uuid4().hex[:12],
        "event_type": event_type,
        "actor_id": actor,
        "surface_id": surface,
        "action": action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "payload": payload or {},
    }
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")
    return event


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _load_jobs(status_filter=None):
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    jobs = []
    for f in sorted(JOBS_DIR.glob("*.json")):
        try:
            job = json.loads(f.read_text())
            if status_filter is None or job.get("status") == status_filter:
                jobs.append(job)
        except (json.JSONDecodeError, OSError):
            pass
    return jobs


def _save_job(job):
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    path = JOBS_DIR / f"{job['job_id']}.json"
    path.write_text(json.dumps(job, indent=2))


def _move_to_dead_letter(job, reason):
    DEAD_LETTER_DIR.mkdir(parents=True, exist_ok=True)
    src = JOBS_DIR / f"{job['job_id']}.json"
    job["dead_letter_ts"] = _now_iso()
    job["dead_letter_reason"] = reason
    dl_path = DEAD_LETTER_DIR / f"{job['job_id']}_{job['retry_count']}.json"
    dl_path.write_text(json.dumps(job, indent=2))
    if src.exists():
        src.unlink()


def _load_alerts():
    ALERTS_DIR.mkdir(parents=True, exist_ok=True)
    alerts = []
    for f in sorted(ALERTS_DIR.glob("*.json"), reverse=True):
        try:
            alerts.append(json.loads(f.read_text()))
        except (json.JSONDecodeError, OSError):
            pass
    return alerts


def _execute_job(job):
    """Simulate job execution. In production, this would call the appropriate worker."""
    action = job["action"]
    target = job.get("target", "unknown")

    if action not in ALLOWED_ACTIONS:
        return False, f"unknown action: {action}"

    error_rate = job.get("_simulate_error_rate", 0)
    if error_rate > 0 and hash(job["job_id"]) % 100 < error_rate:
        return False, "simulated failure"

    return True, f"{action} on {target} completed"


def _create_alert(level, title, message, job_id=None):
    ALERTS_DIR.mkdir(parents=True, exist_ok=True)
    alert = {
        "alert_id": uuid.uuid4().hex[:12],
        "level": level,
        "title": title,
        "message": message,
        "job_id": job_id,
        "timestamp": _now_iso(),
        "acknowledged": False,
    }
    path = ALERTS_DIR / f"{alert['alert_id']}.json"
    path.write_text(json.dumps(alert, indent=2))
    return alert


# ── Commands ─────────────────────────────────────────────────────────

def cmd_list():
    jobs = _load_jobs()
    print(f"{'Job ID':20s} {'Action':20s} {'Target':20s} {'Status':15s} {'Retry':6s}")
    print("-" * 81)
    for j in jobs:
        print(f"{j['job_id']:20s} {j['action']:20s} {j.get('target','?'):20s} {j['status']:15s} {j['retry_count']}/3")
    print(f"\nTotal: {len(jobs)} jobs")


def cmd_submit(action, target, payload=None):
    if action not in ALLOWED_ACTIONS:
        print(f"ERROR: invalid action '{action}'. Allowed: {sorted(ALLOWED_ACTIONS)}")
        return False

    job = {
        "job_id": uuid.uuid4().hex[:12],
        "action": action,
        "target": target or "repo",
        "status": "pending",
        "retry_count": 0,
        "max_retries": MAX_RETRIES,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "last_error": None,
        "payload": payload or {},
    }
    _save_job(job)
    log_ledger("scheduler", "scheduler_worker", target, "JOB_SUBMIT", "PASS",
               {"job_id": job["job_id"], "action": action})
    print(f"Submitted: {job['job_id']} ({action} → {target})")
    return True


def cmd_run():
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    ALERTS_DIR.mkdir(parents=True, exist_ok=True)
    DEAD_LETTER_DIR.mkdir(parents=True, exist_ok=True)

    pending = _load_jobs(status_filter="pending")
    failed = _load_jobs(status_filter="failed")

    cycle_id = uuid.uuid4().hex[:8]
    print(f"[{cycle_id}] Scheduler cycle: {len(pending)} pending, {len(failed)} failed")

    processed = 0
    alerts_created = 0

    # Process pending jobs
    for job in pending:
        job["status"] = "running"
        job["updated_at"] = _now_iso()
        _save_job(job)

        log_ledger("scheduler", "scheduler_worker", job.get("target", "?"),
                   "JOB_START", "PASS", {"job_id": job["job_id"], "action": job["action"]})
        print(f"  Run: {job['job_id']} ({job['action']})")

        ok, msg = _execute_job(job)

        if ok:
            job["status"] = "success"
            job["updated_at"] = _now_iso()
            _save_job(job)
            log_ledger("scheduler", "scheduler_worker", job.get("target", "?"),
                       "JOB_SUCCESS", "PASS", {"job_id": job["job_id"], "message": msg})
            print(f"    PASS: {msg}")
        else:
            job["retry_count"] += 1
            job["last_error"] = msg
            job["updated_at"] = _now_iso()

            if job["retry_count"] >= job["max_retries"]:
                _move_to_dead_letter(job, f"max retries ({job['max_retries']}) exceeded: {msg}")
                log_ledger("scheduler", "scheduler_worker", job.get("target", "?"),
                           "JOB_DEAD_LETTER", "FAIL",
                           {"job_id": job["job_id"], "retries": job["retry_count"], "error": msg})
                alert = _create_alert("critical", f"Job {job['job_id']} dead-lettered",
                                      f"{job['action']} → {job.get('target','?')}: {msg}", job["job_id"])
                alerts_created += 1
                print(f"    DEAD-LETTER: {msg} (alert {alert['alert_id']})")
            else:
                job["status"] = "failed"
                _save_job(job)
                backoff = RETRY_BACKOFF_SECONDS[min(job["retry_count"] - 1, len(RETRY_BACKOFF_SECONDS) - 1)]
                log_ledger("scheduler", "scheduler_worker", job.get("target", "?"),
                           "JOB_FAILED", "WARN",
                           {"job_id": job["job_id"], "retry": job["retry_count"], "backoff": backoff, "error": msg})
                print(f"    FAIL: {msg} (retry {job['retry_count']}/{job['max_retries']}, backoff {backoff}s)")

        processed += 1

    # Process failed jobs eligible for retry
    now = datetime.now(timezone.utc)
    for job in failed:
        updated_str = job["updated_at"]
        if updated_str.endswith("Z"):
            updated_str = updated_str[:-1] + "+00:00"
        updated = datetime.fromisoformat(updated_str)
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=timezone.utc)
        retry_idx = min(job["retry_count"] - 1, len(RETRY_BACKOFF_SECONDS) - 1)
        backoff = RETRY_BACKOFF_SECONDS[retry_idx]
        if (now - updated).total_seconds() >= backoff:
            job["status"] = "pending"
            job["updated_at"] = _now_iso()
            _save_job(job)
            log_ledger("scheduler", "scheduler_worker", job.get("target", "?"),
                       "JOB_RETRY_SCHEDULED", "PASS",
                       {"job_id": job["job_id"], "retry": job["retry_count"]})
            print(f"  Retry scheduled: {job['job_id']} (attempt {job['retry_count']}/{job['max_retries']})")

    summary = {"cycle_id": cycle_id, "processed": processed, "alerts": alerts_created}
    log_ledger("scheduler", "scheduler_worker", "scheduler", "SCHEDULER_CYCLE", "PASS", summary)
    al = len(_load_alerts())
    dl = len(list(DEAD_LETTER_DIR.glob("*.json"))) if DEAD_LETTER_DIR.exists() else 0
    print(f"  Summary: {processed} processed, {alerts_created} alerts, {dl} dead-letter, {al} total alerts")


def cmd_dead_letter():
    dl_dir = DEAD_LETTER_DIR
    if not dl_dir.exists():
        print("No dead-letter queue.")
        return
    items = sorted(dl_dir.glob("*.json"))
    print(f"{'File':40s} {'Action':20s} {'Retries':8s} {'Reason':30s}")
    print("-" * 98)
    for f in items:
        try:
            j = json.loads(f.read_text())
            print(f"{f.name:40s} {j['action']:20s} {j['retry_count']}/3  {j.get('dead_letter_reason','?'):30s}")
        except (json.JSONDecodeError, OSError):
            print(f"{f.name:40s} {'ERROR':20s} {'?':8s} {'corrupt':30s}")
    print(f"\nTotal dead-letter: {len(items)}")


def cmd_alerts():
    alerts = _load_alerts()
    if not alerts:
        print("No alerts.")
        return
    print(f"{'Alert ID':16s} {'Level':10s} {'Title':40s} {'Acknowledged':12s} {'Timestamp':20s}")
    print("-" * 100)
    for a in alerts[:20]:
        ack = "YES" if a.get("acknowledged") else "NO"
        ts = a.get("timestamp", "?")[:19]
        print(f"{a['alert_id']:16s} {a['level']:10s} {a['title'][:40]:40s} {ack:12s} {ts:20s}")
    print(f"\nTotal alerts: {len(alerts)} (showing last 20)")


def main():
    parser = argparse.ArgumentParser(description="P8 Scheduler/CI worker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List all jobs")

    p_submit = sub.add_parser("submit", help="Submit a new job")
    p_submit.add_argument("--action", required=True, choices=sorted(ALLOWED_ACTIONS),
                          help="Job action type")
    p_submit.add_argument("--target", default="repo", help="Target surface")
    p_submit.add_argument("--payload", help="JSON payload string")

    p_run = sub.add_parser("run", help="Run scheduler cycle")

    p_dl = sub.add_parser("dead-letter", help="List dead-letter queue")

    p_alerts = sub.add_parser("alerts", help="List alerts")

    args = parser.parse_args()

    ok = True
    if args.command == "list":
        cmd_list()
    elif args.command == "submit":
        payload = json.loads(args.payload) if args.payload else None
        ok = cmd_submit(args.action, args.target, payload)
    elif args.command == "run":
        cmd_run()
    elif args.command == "dead-letter":
        cmd_dead_letter()
    elif args.command == "alerts":
        cmd_alerts()

    return 0 if ok else 1


if __name__ == "__main__":
    main()
