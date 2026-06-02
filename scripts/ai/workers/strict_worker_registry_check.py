"""Validate models.registry.json and tasks.index.json integrity."""
import json, pathlib, datetime

MODELS_REG = pathlib.Path("scripts/ai/workers/models.registry.json")
TASKS_IDX = pathlib.Path("scripts/ai/workers/tasks.index.json")
REPORT_PATH = pathlib.Path("reports/ai/strict_worker_registry_check.json")

REQUIRED_MODEL_FIELDS = {"model_id", "status", "provider"}
REQUIRED_TASK_FIELDS = {"task_type", "runner"}


def check_models(data: dict) -> list[str]:
    findings = []
    models_raw = data.get("models", {})
    # models can be dict {model_id: {...}} or list [{model_id:...}]
    if isinstance(models_raw, dict):
        models = [{"model_id": k, **v} for k, v in models_raw.items()]
    else:
        models = models_raw
    if not models:
        findings.append("models registry is empty")
    verified = [m for m in models
                if m.get("status") in ("VERIFIED", "VERIFIED_FREE")]
    if not verified:
        findings.append("no VERIFIED models found")
    return findings


def check_tasks(data: dict) -> list[str]:
    findings = []
    tasks_raw = data.get("task_types", data.get("tasks", {}))
    # task_types can be dict {task_type: {...}} or list
    if isinstance(tasks_raw, dict):
        tasks = [{"task_type": k, **v} for k, v in tasks_raw.items()]
    else:
        tasks = tasks_raw
    if not tasks:
        findings.append("task_types index is empty")
    return findings


def main():
    findings = []

    try:
        models_data = json.loads(MODELS_REG.read_text())
        findings += check_models(models_data)
        models_count = len(models_data.get("models", []))
    except (OSError, json.JSONDecodeError) as e:
        findings.append(f"models.registry.json error: {e}")
        models_count = 0

    try:
        tasks_data = json.loads(TASKS_IDX.read_text())
        findings += check_tasks(tasks_data)
        tasks_count = len(tasks_data.get("task_types", tasks_data.get("tasks", [])))
    except (OSError, json.JSONDecodeError) as e:
        findings.append(f"tasks.index.json error: {e}")
        tasks_count = 0

    report = {
        "job_id": "strict-worker-registry-check",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "models_count": models_count,
        "tasks_count": tasks_count,
        "findings": findings,
        "status": "PASS" if not findings else "WARN",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
