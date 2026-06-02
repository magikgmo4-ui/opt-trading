#!/usr/bin/env python3
"""openclaw_strict_worker_dispatcher.py — Deterministic dispatcher: OpenClaw → strict workers.

Routes a job packet to runner_readonly.py or runner_writegated.py based solely
on task_type. No LLM involved in the dispatch decision.

Routing table:
  WRITE_GATED            → runner_writegated.py  (--gate-approved required)
  all other task types   → runner_readonly.py

Exit codes:
  0  PASS / DRY_RUN_PASS
  1  INVALID_INPUT
  2  BLOCKED (git dirty)
  3  REJECTED (validation failed)
  4  REFUSED (unknown task_type / unknown worker / missing gate)
  5  RUNNER_ERROR
"""

import argparse
import atexit
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_tmp_to_cleanup: Path | None = None


def _register_tmp_cleanup(path: Path) -> None:
    global _tmp_to_cleanup
    _tmp_to_cleanup = path
    atexit.register(_cleanup_tmp)


def _cleanup_tmp() -> None:
    if _tmp_to_cleanup and _tmp_to_cleanup.exists():
        _tmp_to_cleanup.unlink(missing_ok=True)

REPO_ROOT = Path(__file__).resolve().parents[3]
JOB_PACKETS_DIR = REPO_ROOT / "scripts/ai/workers/job_packets"
RUNNER_READONLY = REPO_ROOT / "scripts/ai/workers/runner_readonly.py"
RUNNER_WRITEGATED = REPO_ROOT / "scripts/ai/workers/runner_writegated.py"
MODELS_REGISTRY = REPO_ROOT / "scripts/ai/workers/models.registry.json"
TASKS_INDEX = REPO_ROOT / "scripts/ai/workers/tasks.index.json"

WRITEGATED_TASK_TYPES = {"WRITE_GATED"}

DISPATCHER_NAME = "openclaw_strict_worker_dispatcher"


def _load_models_registry() -> dict:
    with open(MODELS_REGISTRY) as f:
        return json.load(f)


def _load_tasks_index() -> dict:
    with open(TASKS_INDEX) as f:
        return json.load(f)


def _resolve_packet(args: argparse.Namespace) -> tuple[Path, dict]:
    if args.packet:
        path = Path(args.packet)
        if not path.is_absolute():
            path = REPO_ROOT / path
        if not path.exists():
            _exit_invalid(f"packet not found: {path}")
        with open(path) as f:
            return path, json.load(f)

    if args.packet_id:
        path = JOB_PACKETS_DIR / f"{args.packet_id}.json"
        if not path.exists():
            _exit_invalid(f"packet_id '{args.packet_id}' not found in {JOB_PACKETS_DIR}")
        with open(path) as f:
            return path, json.load(f)

    if args.packet_json:
        try:
            packet = json.loads(args.packet_json)
        except json.JSONDecodeError as exc:
            _exit_invalid(f"invalid JSON in --packet-json: {exc}")
        packet_id = packet.get("job_packet_id", "inline")
        tmp_path = REPO_ROOT / f"reports/ai/workers/.dispatcher_tmp_{packet_id}.json"
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path.write_text(json.dumps(packet, indent=2))
        _register_tmp_cleanup(tmp_path)
        return tmp_path, packet

    _exit_invalid("one of --packet, --packet-id, or --packet-json is required")


def _exit_invalid(reason: str):
    print(json.dumps({"status": "INVALID_INPUT", "dispatcher": DISPATCHER_NAME, "reason": reason}, indent=2))
    sys.exit(1)


def _exit_refused(reason: str, job_packet_id: str = "unknown"):
    print(json.dumps({
        "status": "REFUSED",
        "dispatcher": DISPATCHER_NAME,
        "job_packet_id": job_packet_id,
        "reason": reason,
    }, indent=2))
    sys.exit(4)


def _validate_worker(worker: str, registry: dict) -> bool:
    models = registry.get("models", {})
    entry = models.get(worker, {})
    return entry.get("status", "") in ("VERIFIED", "VERIFIED_FREE")


def _validate_task_type(task_type: str, tasks_index: dict) -> bool:
    return task_type in tasks_index.get("tasks", {})


def _build_format3(
    *,
    status: str,
    job_packet_id: str,
    task_type: str,
    runner_called: str,
    dry_run: bool,
    gate_approved: bool,
    runner_result: dict,
    report_path: str,
    dispatched_at: str,
    completed_at: str,
) -> dict:
    return {
        "dispatcher": DISPATCHER_NAME,
        "status": status,
        "job_packet_id": job_packet_id,
        "task_type": task_type,
        "runner_called": runner_called,
        "dry_run": dry_run,
        "gate_approved": gate_approved,
        "runner_result": runner_result,
        "report_path": report_path,
        "dispatched_at": dispatched_at,
        "completed_at": completed_at,
    }


def _call_runner(runner: Path, packet_path: Path, dry_run: bool, gate_approved: bool) -> tuple[int, dict]:
    cmd = ["python3", str(runner), str(packet_path)]
    if dry_run:
        cmd.append("--dry-run")
    if gate_approved:
        cmd.append("--gate-approved")

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=REPO_ROOT)
    except subprocess.TimeoutExpired:
        return 5, {"status": "RUNNER_TIMEOUT", "reason": f"runner timed out after 120s"}

    raw = proc.stdout.strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"status": "RUNNER_ERROR", "raw_stdout": raw[:500], "stderr": proc.stderr.strip()[:300]}
        return 5, result

    return proc.returncode, result


def main():
    parser = argparse.ArgumentParser(description=DISPATCHER_NAME)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--packet", metavar="PATH", help="Path to job packet JSON file")
    group.add_argument("--packet-id", metavar="ID", help="Job packet ID (resolved from job_packets/)")
    group.add_argument("--packet-json", metavar="JSON", help="Inline job packet JSON string")
    parser.add_argument("--dry-run", action="store_true", help="Simulate dispatch, no execution")
    parser.add_argument("--gate-approved", action="store_true", help="Authorize write execution (WRITE_GATED only)")
    args = parser.parse_args()

    if not (args.packet or args.packet_id or args.packet_json):
        _exit_invalid("one of --packet, --packet-id, or --packet-json is required")

    dispatched_at = datetime.now(timezone.utc).isoformat()

    packet_path, packet = _resolve_packet(args)
    job_packet_id = packet.get("job_packet_id", "unknown")
    task_type = packet.get("task_type", "")
    worker = packet.get("default_worker", packet.get("worker_assigned", ""))

    registry = _load_models_registry()
    tasks_index = _load_tasks_index()

    if not task_type or not _validate_task_type(task_type, tasks_index):
        _exit_refused(f"unknown or missing task_type: '{task_type}'", job_packet_id)

    if not worker or not _validate_worker(worker, registry):
        _exit_refused(f"unknown or unverified worker: '{worker}'", job_packet_id)

    is_writegated = task_type in WRITEGATED_TASK_TYPES

    if is_writegated and not args.dry_run and not args.gate_approved:
        _exit_refused(
            "WRITE_GATED task_type requires --gate-approved (or --dry-run to simulate)",
            job_packet_id,
        )

    runner = RUNNER_WRITEGATED if is_writegated else RUNNER_READONLY
    runner_name = runner.name

    rc, runner_result = _call_runner(runner, packet_path, args.dry_run, args.gate_approved)

    completed_at = datetime.now(timezone.utc).isoformat()

    runner_status = runner_result.get("status", "UNKNOWN")
    if rc == 0 or runner_status in ("PASS", "DRY_RUN_PASS", "READS_ONLY_PASS"):
        dispatch_status = "DRY_RUN_PASS" if args.dry_run else "PASS"
    else:
        dispatch_status = "RUNNER_ERROR"

    report_path = runner_result.get(
        "output_path",
        f"reports/ai/workers/{job_packet_id}_RUNNER.json",
    )

    output = _build_format3(
        status=dispatch_status,
        job_packet_id=job_packet_id,
        task_type=task_type,
        runner_called=runner_name,
        dry_run=args.dry_run,
        gate_approved=args.gate_approved,
        runner_result=runner_result,
        report_path=report_path,
        dispatched_at=dispatched_at,
        completed_at=completed_at,
    )

    print(json.dumps(output, indent=2))

    # Temp file from --packet-json is cleaned up via atexit handler

    sys.exit(0 if dispatch_status in ("PASS", "DRY_RUN_PASS") else 5)


if __name__ == "__main__":
    main()
