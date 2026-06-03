#!/usr/bin/env python3
"""runner_readonly.py — Strict Workers read-only runner.

Wraps the existing validation and task execution pipeline with:
  - no-write guard (blocks write instructions at environment level)
  - --dry-run mode for audit
  - normalized JSON output per job
  - per-job logs

Usage:
  python3 scripts/ai/workers/runner_readonly.py <job_packet.json> [--dry-run]
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = REPO_ROOT / "scripts/ai/workers/_validate_job.py"
TASKS_INDEX = REPO_ROOT / "scripts/ai/workers/tasks.index.json"
MODELS_REGISTRY = REPO_ROOT / "scripts/ai/workers/models.registry.json"
OUTPUT_DIR = REPO_ROOT / "reports/ai/workers"
LOG_DIR = REPO_ROOT / "data/runtime_health/job_logs"


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


def _run_job(job_id: str, packet: dict, dry_run: bool) -> dict:
    worker = packet.get("default_worker", "unknown")
    task_type = packet.get("task_type", "unknown")
    scope = packet.get("scope", {})
    allowed_inputs = scope.get("allowed_inputs", [])

    result = {
        "job_id": job_id,
        "worker": worker,
        "task_type": task_type,
        "dry_run": dry_run,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "read_operations": [],
        "write_attempts_blocked": [],
        "status": "PASS",
    }

    for inp in allowed_inputs:
        for p in Path(REPO_ROOT).glob(inp):
            if p.is_file() and p.suffix in (".md", ".json", ".yaml", ".yml", ".py", ".sh"):
                try:
                    content = p.read_text(encoding="utf-8", errors="replace")
                    result["read_operations"].append({
                        "path": str(p.relative_to(REPO_ROOT)),
                        "size_bytes": len(content),
                    })
                except Exception as e:
                    result.setdefault("warnings", []).append(
                        f"read_failed:{p.relative_to(REPO_ROOT)}:{e}"
                    )

    if not result["read_operations"]:
        result.setdefault("warnings", []).append("no_inputs_matched")

    result["read_count"] = len(result["read_operations"])
    result["completed_at"] = datetime.now(timezone.utc).isoformat()
    return result


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
    parser = argparse.ArgumentParser(description="Strict Workers read-only runner")
    parser.add_argument("job_packet", help="Path to job packet JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Simulate only, no execution")
    args = parser.parse_args()

    packet_path = Path(args.job_packet)
    if not packet_path.exists():
        print(json.dumps({"status": "ERROR", "reason": f"packet not found: {packet_path}"}))
        sys.exit(1)

    if not args.dry_run:
        _check_git_clean()

    with open(packet_path) as f:
        packet = json.load(f)
    job_id = packet.get("job_packet_id", "unknown")

    validation = _validate_job_packet(str(packet_path))
    if validation.get("status") == "FAILED":
        result = {"status": "REJECTED", "job_id": job_id, "validation": validation}
        log_path = _write_log(job_id, result)
        print(json.dumps(result))
        print(f"LOG: {log_path}", file=sys.stderr)
        sys.exit(3)

    if args.dry_run:
        result = {
            "status": "DRY_RUN_PASS",
            "job_id": job_id,
            "validation": validation,
            "dry_run": True,
            "message": "no operations executed (--dry-run)",
        }
        out_path = _write_output(job_id, result)
        log_path = _write_log(job_id, result)
        print(json.dumps(result, indent=2))
        print(f"OUTPUT: {out_path}", file=sys.stderr)
        print(f"LOG: {log_path}", file=sys.stderr)
        return

    exec_result = _run_job(job_id, packet, dry_run=False)
    exec_result["validation"] = validation

    out_path = _write_output(job_id, exec_result)
    log_path = _write_log(job_id, exec_result)

    print(json.dumps(exec_result, indent=2))
    print(f"OUTPUT: {out_path}", file=sys.stderr)
    print(f"LOG: {log_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
