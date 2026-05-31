#!/usr/bin/env python3
"""runner_writegated.py — Strict Workers write-gated runner.

Extends runner_readonly with a controlled write phase. Writes are blocked
by default and require --gate-approved + a write_plan in the job packet.

Flow:
  1. Validate job packet (same as runner_readonly)
  2. Read allowed_inputs (same as runner_readonly)
  3. Parse write_plan from packet
  4. Validate each target against write_allowlist / forbidden_targets
  5. --dry-run  : report what would be written, 0 actual writes
  6. --gate-approved : execute writes to allowlisted targets only
  7. (default) : read-only pass, writes blocked

Usage:
  python3 scripts/ai/workers/runner_writegated.py <job_packet.json> [--dry-run]
  python3 scripts/ai/workers/runner_writegated.py <job_packet.json> --gate-approved
"""

import argparse
import fnmatch
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = REPO_ROOT / "scripts/ai/workers/_validate_job.py"
TASKS_INDEX = REPO_ROOT / "scripts/ai/workers/tasks.index.json"
MODELS_REGISTRY = REPO_ROOT / "scripts/ai/workers/models.registry.json"
OUTPUT_DIR = REPO_ROOT / "reports/ai/workers"
LOG_DIR = REPO_ROOT / "data/runtime_health/job_logs"

MAX_CONTENT_LINES_DEFAULT = 50


def _check_git_clean():
    rc = subprocess.run(
        ["git", "diff", "--quiet"], cwd=REPO_ROOT, capture_output=True
    ).returncode
    if rc != 0:
        print(json.dumps({"status": "BLOCKED", "reason": "git working tree has unstaged changes to tracked files"}))
        sys.exit(2)


def _validate_job_packet(packet_path: str) -> dict:
    env = os.environ.copy()
    env["TASKS_INDEX_PATH"] = str(TASKS_INDEX)
    env["MODELS_REGISTRY_PATH"] = str(MODELS_REGISTRY)
    env["JOB_PACKET_PATH"] = packet_path
    env["OUTPUT_DIR_PATH"] = str(OUTPUT_DIR)
    env["REPO_ROOT"] = str(REPO_ROOT)
    r = subprocess.run(
        ["python3", str(VALIDATOR)],
        capture_output=True, text=True, timeout=30, env=env
    )
    if r.returncode != 0:
        return {"status": "FAILED", "errors": [r.stdout.strip()]}
    return json.loads(r.stdout)


def _load_task_def(task_type: str) -> dict:
    with open(TASKS_INDEX) as f:
        idx = json.load(f)
    return idx.get("tasks", {}).get(task_type, {})


def _run_reads(allowed_inputs: list) -> list:
    reads = []
    for inp in allowed_inputs:
        for p in Path(REPO_ROOT).glob(inp):
            if p.is_file() and p.suffix in (".md", ".json", ".yaml", ".yml", ".py", ".sh"):
                try:
                    content = p.read_text(encoding="utf-8", errors="replace")
                    reads.append({"path": str(p.relative_to(REPO_ROOT)), "size_bytes": len(content)})
                except Exception as e:
                    reads.append({"path": str(p.relative_to(REPO_ROOT)), "error": str(e)})
    return reads


def _validate_write_target(target: str, task_def: dict) -> list[str]:
    """Return list of blocking errors for a write target. Empty = allowed."""
    errors = []
    allowlist = task_def.get("write_allowlist", [])
    forbidden = task_def.get("forbidden_targets", [])

    if any(fnmatch.fnmatch(target, pat) for pat in forbidden):
        errors.append(f"FORBIDDEN_TARGET: {target}")
        return errors

    if not any(fnmatch.fnmatch(target, pat) for pat in allowlist):
        errors.append(f"NOT_IN_ALLOWLIST: {target} — allowlist={allowlist}")

    return errors


def _execute_writes(write_plan: list, task_def: dict, dry_run: bool) -> list:
    max_lines = task_def.get("max_lines_per_write", MAX_CONTENT_LINES_DEFAULT)
    results = []

    for entry in write_plan:
        target = entry.get("target", "")
        content = entry.get("content", "")
        line_count = len(content.splitlines())

        op = {"target": target, "lines": line_count}

        target_errors = _validate_write_target(target, task_def)
        if target_errors:
            op["status"] = "BLOCKED"
            op["errors"] = target_errors
            results.append(op)
            continue

        if line_count > max_lines:
            op["status"] = "BLOCKED"
            op["errors"] = [f"EXCEEDS_MAX_LINES: {line_count} > {max_lines}"]
            results.append(op)
            continue

        if dry_run:
            op["status"] = "DRY_RUN_WOULD_WRITE"
        else:
            abs_target = REPO_ROOT / target
            abs_target.parent.mkdir(parents=True, exist_ok=True)
            abs_target.write_text(content, encoding="utf-8")
            op["status"] = "WRITTEN"

        results.append(op)

    return results


def _write_log(job_id: str, result: dict):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{job_id}.json"
    log_path.write_text(json.dumps(result, indent=2))
    return log_path


def _write_output(job_id: str, result: dict):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{job_id}_RUNNER.json"
    out_path.write_text(json.dumps(result, indent=2))
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Strict Workers write-gated runner")
    parser.add_argument("job_packet", help="Path to job packet JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Simulate reads+writes, no actual writes")
    parser.add_argument("--gate-approved", action="store_true", help="Gate APPROVE — authorize write execution")
    args = parser.parse_args()

    if args.dry_run and args.gate_approved:
        print(json.dumps({"status": "ERROR", "reason": "--dry-run and --gate-approved are mutually exclusive"}))
        sys.exit(1)

    packet_path = Path(args.job_packet)
    if not packet_path.exists():
        print(json.dumps({"status": "ERROR", "reason": f"packet not found: {packet_path}"}))
        sys.exit(1)

    _check_git_clean()

    with open(packet_path) as f:
        packet = json.load(f)
    job_id = packet.get("job_packet_id", "unknown")
    task_type = packet.get("task_type", "unknown")

    validation = _validate_job_packet(str(packet_path))
    if validation.get("status") == "FAILED":
        result = {"status": "REJECTED", "job_id": job_id, "validation": validation}
        log_path = _write_log(job_id, result)
        print(json.dumps(result))
        print(f"LOG: {log_path}", file=sys.stderr)
        sys.exit(3)

    task_def = _load_task_def(task_type)
    scope = packet.get("scope", {})
    write_plan = packet.get("write_plan", [])

    reads = _run_reads(scope.get("allowed_inputs", []))

    now = datetime.now(timezone.utc).isoformat()

    if args.dry_run:
        write_results = _execute_writes(write_plan, task_def, dry_run=True)
        result = {
            "job_id": job_id,
            "task_type": task_type,
            "status": "DRY_RUN_PASS",
            "dry_run": True,
            "gate_approved": False,
            "read_count": len(reads),
            "read_operations": reads,
            "write_plan_count": len(write_plan),
            "write_results": write_results,
            "produced_at": now,
            "validation": validation,
        }
    elif args.gate_approved:
        write_results = _execute_writes(write_plan, task_def, dry_run=False)
        blocked = [w for w in write_results if w["status"] == "BLOCKED"]
        written = [w for w in write_results if w["status"] == "WRITTEN"]
        status = "PASS" if not blocked else "PARTIAL_BLOCKED"
        result = {
            "job_id": job_id,
            "task_type": task_type,
            "status": status,
            "dry_run": False,
            "gate_approved": True,
            "read_count": len(reads),
            "read_operations": reads,
            "write_plan_count": len(write_plan),
            "write_results": write_results,
            "writes_executed": len(written),
            "writes_blocked": len(blocked),
            "produced_at": now,
            "validation": validation,
        }
    else:
        # Default: reads only, writes blocked
        result = {
            "job_id": job_id,
            "task_type": task_type,
            "status": "READS_ONLY_PASS",
            "dry_run": False,
            "gate_approved": False,
            "read_count": len(reads),
            "read_operations": reads,
            "write_plan_count": len(write_plan),
            "write_results": [{"target": e.get("target"), "status": "BLOCKED_NO_GATE"} for e in write_plan],
            "message": "writes blocked — pass --gate-approved to authorize",
            "produced_at": now,
            "validation": validation,
        }

    out_path = _write_output(job_id, result)
    log_path = _write_log(job_id, result)

    print(json.dumps(result, indent=2))
    print(f"OUTPUT: {out_path}", file=sys.stderr)
    print(f"LOG: {log_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
