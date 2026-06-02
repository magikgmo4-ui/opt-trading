"""Verify write gates are enforced — checks runner invariants and gate config."""
import json, pathlib, datetime

TASKS_INDEX = pathlib.Path("scripts/ai/workers/tasks.index.json")
REPORT_PATH = pathlib.Path("reports/ai/deny_by_default_check.json")


def main():
    findings = []
    checks = []

    # 1. tasks.index global_invariants
    try:
        idx = json.loads(TASKS_INDEX.read_text())
        inv = idx.get("global_invariants", {})
        if inv.get("no_git_write_ops") is True:
            checks.append({"check": "no_git_write_ops", "result": "PASS"})
        else:
            checks.append({"check": "no_git_write_ops", "result": "WARN"})
            findings.append("no_git_write_ops not enforced in tasks.index")
        if inv.get("no_runtime_write_by_default") is True:
            checks.append({"check": "no_runtime_write_by_default", "result": "PASS"})
        else:
            checks.append({"check": "no_runtime_write_by_default", "result": "WARN"})
            findings.append("no_runtime_write_by_default not set")
    except Exception as e:
        findings.append(f"tasks.index.json error: {e}")

    # 2. WRITE_GATED task type requires gate_approved in dispatcher
    dispatcher = pathlib.Path("scripts/ai/workers/openclaw_strict_worker_dispatcher.py")
    if dispatcher.exists():
        src = dispatcher.read_text()
        if "gate_approved" in src and "WRITE_GATED" in src:
            checks.append({"check": "dispatcher_write_gate", "result": "PASS"})
        else:
            checks.append({"check": "dispatcher_write_gate", "result": "WARN"})
            findings.append("dispatcher gate logic not found")
    else:
        findings.append("dispatcher script not found")

    # 3. runner_writegated exists
    runner = pathlib.Path("scripts/ai/workers/runner_writegated.py")
    checks.append({"check": "runner_writegated_exists",
                   "result": "PASS" if runner.exists() else "WARN"})
    if not runner.exists():
        findings.append("runner_writegated.py not found")

    status = "PASS" if not findings else "WARN"
    report = {
        "job_id": "deny-by-default-check",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "checks": checks,
        "findings": findings,
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
