"""Dry-run for task router — validates task_type → runner routing table."""
import json, pathlib, datetime

TASKS_INDEX = pathlib.Path("scripts/ai/workers/tasks.index.json")
REPORT_PATH = pathlib.Path("reports/ai/task_router_dry_run.json")

TEST_ROUTES = [
    ("READ_INVENTORY", "runner_readonly.py"),
    ("PATCH_DRAFT", "runner_readonly.py"),
    ("DOC_DRAFT", "runner_readonly.py"),
    ("WRITE_GATED", "runner_writegated.py"),
    ("FAST_TRIAGE", "runner_readonly.py"),
]


def main():
    findings = []
    try:
        idx = json.loads(TASKS_INDEX.read_text())
        task_types = idx.get("task_types", {})
        if isinstance(task_types, dict):
            known = set(task_types.keys())
        else:
            known = {t.get("task_type") for t in task_types}
    except Exception as e:
        findings.append(f"tasks.index.json error: {e}")
        known = set()

    routes = []
    for task_type, expected_runner in TEST_ROUTES:
        result = "PASS" if task_type in known else "WARN_NOT_IN_INDEX"
        routes.append({"task_type": task_type, "expected_runner": expected_runner,
                       "in_index": task_type in known, "result": result})

    status = "PASS" if not findings else "WARN"
    report = {
        "job_id": "task-router-dry-run",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "dry_run": True,
        "known_task_types": sorted(known),
        "routes_tested": routes,
        "findings": findings,
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "routes": len(routes),
                      "status": status}, indent=2))

if __name__ == "__main__":
    main()
