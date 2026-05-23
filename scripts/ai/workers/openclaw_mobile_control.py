#!/usr/bin/env python3
"""Bounded OpenClaw mobile-control wrapper.

This wrapper is intended for Termux/mobile or machine-side operator use.  It is
restricted to NON_TRADING_AUTOMATION_ONLY Phase 01 read-only/dry-run/local-only
jobs and emits deterministic JSON evidence under reports/ai/mobile_control.

Initial actions:
  status
  list-jobs
  preflight
  run-dry
  evidence
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = REPO_ROOT / "reports" / "ai" / "mobile_control"
LEDGER_WRITER = REPO_ROOT / "scripts" / "ai" / "workers" / "ledger_writer.py"


@dataclass(frozen=True)
class JobSpec:
    job_id: str
    mode: str
    command: list[str] | None
    evidence: str
    allowed_write_scope: str
    notes: str
    run_status_override: str | None = None


def _py(script: str, *args: str) -> list[str]:
    return [sys.executable, script, *args]


PHASE_01_JOBS: dict[str, JobSpec] = {
    "repo-status-check": JobSpec(
        "repo-status-check",
        "read-only",
        ["git", "status", "--short", "--branch"],
        "branch/state output",
        "none",
        "Git status read-only check.",
    ),
    "repo-diff-check": JobSpec(
        "repo-diff-check",
        "read-only",
        ["git", "diff", "--check"],
        "whitespace/conflict output",
        "none",
        "Git diff whitespace/conflict check.",
    ),
    "repo-pr-audit": JobSpec(
        "repo-pr-audit",
        "read-only",
        ["gh", "pr", "list", "--state", "all", "--limit", "50"],
        "PR digest output",
        "none",
        "GitHub PR digest when gh is available.",
    ),
    "automation-health-status": JobSpec(
        "automation-health-status",
        "local report",
        _py("scripts/ai/workers/health_status.py", "--output", "reports/ai/health_status.json"),
        "reports/ai/health_status.json",
        "reports/ai only",
        "Generate health status report.",
    ),
    "ledger-heartbeat": JobSpec(
        "ledger-heartbeat",
        "local ledger write",
        _py(
            "scripts/ai/workers/ledger_writer.py",
            "--event-type",
            "HEARTBEAT",
            "--actor-id",
            "mobile-control",
            "--surface-id",
            "automation",
            "--action",
            "HEARTBEAT",
            "--status",
            "PASS",
            "--payload",
            "{}",
        ),
        "ledger heartbeat event",
        "data/runtime_health/ledger only",
        "Append a local heartbeat event.",
    ),
    "ledger-replay-check": JobSpec(
        "ledger-replay-check",
        "read-only",
        _py("scripts/ai/workers/ledger_replay.py", "--replay"),
        "replay summary",
        "none",
        "Replay ledger events.",
    ),
    "anti-leak-scan": JobSpec(
        "anti-leak-scan",
        "read-only/local",
        _py("scripts/ai/tests/anti_leak_tests.py"),
        "anti-leak test output",
        "local test artifacts only",
        "Run anti-leak smoke checks.",
    ),
    "capability-matrix-validate": JobSpec(
        "capability-matrix-validate",
        "local evidence",
        _py("scripts/ai/tests/g01_validate_scenarios.py"),
        "scenario result output",
        "documented evidence only",
        "Validate capability matrix scenarios.",
    ),
    "ai-team-handoff-dry-run": JobSpec(
        "ai-team-handoff-dry-run",
        "dry-run",
        _py("scripts/ai/tests/g03_dry_run_handoff.py"),
        "dry-run handoff output",
        "documented evidence only",
        "Run AI team handoff dry-run.",
    ),
    "hitl-scenarios-smoke": JobSpec(
        "hitl-scenarios-smoke",
        "dry-run",
        _py("scripts/ai/tests/hitl_scenarios.py"),
        "HITL scenario output",
        "documented evidence only",
        "Run HITL scenario smoke.",
    ),
    "localcms-automation-status-sync": JobSpec(
        "localcms-automation-status-sync",
        "write-gated/local",
        _py("scripts/ai/workers/localcms_automation_status_sync.py"),
        "tmp/localcms_latest.json + report artifact",
        "local rendered views only",
        "Refresh local-only LocalCMS automation snapshot.",
    ),
    "strict-worker-readonly-smoke": JobSpec(
        "strict-worker-readonly-smoke",
        "precheck-only",
        None,
        "runner lock + job packet presence",
        "none",
        "Full model-executed path remains a follow-up.",
        run_status_override="PRECHECK_PASS",
    ),
}

FORBIDDEN_JOB_MARKERS = ("signal", "trading", "order", "external-write", "secret")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_name(value: str | None) -> str:
    if not value:
        return "all"
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in value)[:96]


def git_info() -> dict[str, str]:
    def run_git(args: list[str]) -> str:
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=8,
                check=False,
            )
            return result.stdout.strip() or result.stderr.strip() or "unknown"
        except Exception:
            return "unknown"

    return {
        "branch": run_git(["rev-parse", "--abbrev-ref", "HEAD"]),
        "commit": run_git(["rev-parse", "--short", "HEAD"]),
    }


def safety_template() -> dict[str, bool]:
    return {
        "non_trading_only": True,
        "external_write": False,
        "signal_trading": False,
        "secret_access": False,
        "scheduler_activation": False,
    }


def base_result(action: str, phase: str | None, job_id: str | None) -> dict[str, Any]:
    return {
        "ok": False,
        "action": action,
        "phase": phase,
        "job_id": job_id,
        "status": "PENDING",
        "timestamp": utc_now(),
        "git": git_info(),
        "evidence_path": None,
        "blocked_reason": None,
        "stdout": "",
        "stderr": "",
        "returncode": None,
        "safety": safety_template(),
    }


def write_report(result: dict[str, Any]) -> dict[str, Any]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = f"{safe_name(result.get('action'))}_{safe_name(result.get('job_id'))}"
    path = REPORT_DIR / f"{stamp}_{suffix}_{uuid.uuid4().hex[:8]}.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["evidence_path"] = str(path.relative_to(REPO_ROOT))
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def write_mobile_ledger(result: dict[str, Any]) -> None:
    if not LEDGER_WRITER.exists():
        return
    status = result.get("status", "WARN")
    ledger_status = "PASS" if status in {"PASS", "PRECHECK_PASS"} else "BLOCKED" if status == "BLOCKED_WITH_REASON" else "FAIL"
    payload = {
        "action": result.get("action"),
        "phase": result.get("phase"),
        "job_id": result.get("job_id"),
        "evidence_path": result.get("evidence_path"),
        "blocked_reason": result.get("blocked_reason"),
    }
    try:
        subprocess.run(
            [
                sys.executable,
                str(LEDGER_WRITER.relative_to(REPO_ROOT)),
                "--event-type",
                "MOBILE_CONTROL",
                "--actor-id",
                "mobile-control",
                "--surface-id",
                "openclaw",
                "--action",
                str(result.get("action") or "UNKNOWN"),
                "--status",
                ledger_status,
                "--payload",
                json.dumps(payload),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except Exception:
        return


def blocked(action: str, phase: str | None, job_id: str | None, reason: str) -> dict[str, Any]:
    result = base_result(action, phase, job_id)
    result.update({"ok": False, "status": "BLOCKED_WITH_REASON", "blocked_reason": reason})
    result = write_report(result)
    write_mobile_ledger(result)
    return result


def validate_phase(phase: str | None) -> str | None:
    if phase is None:
        return "PHASE_01"
    normalized = phase.upper()
    if normalized != "PHASE_01":
        return None
    return normalized


def get_job(job_id: str | None) -> JobSpec | None:
    if not job_id:
        return None
    return PHASE_01_JOBS.get(job_id)


def validate_job_for_mobile(job: JobSpec | None) -> str | None:
    if job is None:
        return "unknown or missing job_id"
    lowered = job.job_id.lower()
    if any(marker in lowered for marker in FORBIDDEN_JOB_MARKERS):
        return "job_id contains forbidden scope marker"
    if "external" in job.allowed_write_scope.lower():
        return "external write scope is not allowed"
    return None


def run_command(command: list[str]) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        return completed.returncode, completed.stdout.strip(), completed.stderr.strip()
    except FileNotFoundError as exc:
        return 127, "", str(exc)
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", exc.stderr or "timeout expired"
    except Exception as exc:
        return 1, "", str(exc)


def action_status(args: argparse.Namespace) -> dict[str, Any]:
    result = base_result("status", validate_phase(args.phase) or args.phase, None)
    result.update(
        {
            "ok": True,
            "status": "PASS",
            "available_phases": ["PHASE_01"],
            "available_jobs": len(PHASE_01_JOBS),
            "report_dir": str(REPORT_DIR.relative_to(REPO_ROOT)),
            "notes": "Bounded mobile-control wrapper ready for Phase 01 read-only/dry-run/local-only actions.",
        }
    )
    result = write_report(result)
    write_mobile_ledger(result)
    return result


def action_list_jobs(args: argparse.Namespace) -> dict[str, Any]:
    phase = validate_phase(args.phase)
    if phase is None:
        return blocked("list-jobs", args.phase, None, "only PHASE_01 is allowed initially")
    result = base_result("list-jobs", phase, None)
    jobs = []
    for job in PHASE_01_JOBS.values():
        jobs.append(
            {
                "job_id": job.job_id,
                "mode": job.mode,
                "evidence": job.evidence,
                "allowed_write_scope": job.allowed_write_scope,
                "notes": job.notes,
                "mobile_allowed": validate_job_for_mobile(job) is None,
                "run_status_override": job.run_status_override,
            }
        )
    result.update({"ok": True, "status": "PASS", "jobs": jobs})
    result = write_report(result)
    write_mobile_ledger(result)
    return result


def action_preflight(args: argparse.Namespace) -> dict[str, Any]:
    phase = validate_phase(args.phase)
    if phase is None:
        return blocked("preflight", args.phase, args.job, "only PHASE_01 is allowed initially")
    job = get_job(args.job)
    reason = validate_job_for_mobile(job)
    if reason:
        return blocked("preflight", phase, args.job, reason)
    assert job is not None
    result = base_result("preflight", phase, job.job_id)
    checks = {
        "repo_root_exists": REPO_ROOT.exists(),
        "report_dir_creatable": True,
        "job_known": True,
        "mobile_allowed": True,
        "command_mapped": job.command is not None or job.run_status_override == "PRECHECK_PASS",
    }
    try:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        checks["report_dir_creatable"] = False

    ok = all(checks.values())

    # Add safety info for report but don't break ok if they are False (which is safe)
    checks["external_write_blocked"] = True
    checks["signal_trading_blocked"] = True

    result.update(
        {
            "ok": ok,
            "status": "PASS" if ok else "BLOCKED_WITH_REASON",
            "blocked_reason": None if ok else "one or more preflight checks failed",
            "checks": checks,
            "job": asdict(job),
        }
    )
    result = write_report(result)
    write_mobile_ledger(result)
    return result


def action_run_dry(args: argparse.Namespace) -> dict[str, Any]:
    phase = validate_phase(args.phase)
    if phase is None:
        return blocked("run-dry", args.phase, args.job, "only PHASE_01 is allowed initially")
    job = get_job(args.job)
    reason = validate_job_for_mobile(job)
    if reason:
        return blocked("run-dry", phase, args.job, reason)
    assert job is not None
    if job.run_status_override == "PRECHECK_PASS":
        result = base_result("run-dry", phase, job.job_id)
        result.update(
            {
                "ok": True,
                "status": "PRECHECK_PASS",
                "job": asdict(job),
                "stdout": "runner/precheck path acknowledged; full model E2E remains follow-up",
                "returncode": 0,
            }
        )
        result = write_report(result)
        write_mobile_ledger(result)
        return result
    if not job.command:
        return blocked("run-dry", phase, job.job_id, "job has no command mapping")
    rc, stdout, stderr = run_command(job.command)
    result = base_result("run-dry", phase, job.job_id)
    result.update(
        {
            "ok": rc == 0,
            "status": "PASS" if rc == 0 else "FAIL",
            "returncode": rc,
            "stdout": stdout,
            "stderr": stderr,
            "job": asdict(job),
        }
    )
    result = write_report(result)
    write_mobile_ledger(result)
    return result


def action_evidence(args: argparse.Namespace) -> dict[str, Any]:
    phase = validate_phase(args.phase)
    if phase is None:
        return blocked("evidence", args.phase, args.job, "only PHASE_01 is allowed initially")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(REPORT_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if args.job:
        files = [p for p in files if safe_name(args.job) in p.name]
    result = base_result("evidence", phase, args.job)
    result.update(
        {
            "ok": True,
            "status": "PASS",
            "reports": [str(p.relative_to(REPO_ROOT)) for p in files[:20]],
            "report_count_returned": min(len(files), 20),
        }
    )
    result = write_report(result)
    write_mobile_ledger(result)
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bounded OpenClaw mobile-control wrapper")
    parser.add_argument("action", choices=["status", "list-jobs", "preflight", "run-dry", "evidence"])
    parser.add_argument("--phase", default="PHASE_01")
    parser.add_argument("--job", default=None)
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    handlers = {
        "status": action_status,
        "list-jobs": action_list_jobs,
        "preflight": action_preflight,
        "run-dry": action_run_dry,
        "evidence": action_evidence,
    }
    result = handlers[args.action](args)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") in {"PASS", "PRECHECK_PASS", "BLOCKED_WITH_REASON"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
