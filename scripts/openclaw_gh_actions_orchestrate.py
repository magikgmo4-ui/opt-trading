import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime
from typing import Optional

REGISTRY_PATH = "docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml"
REPORT_PATH = "docs/chantiers/GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_OPERATIONAL_01/OPERATIONAL_REPORT_01.md"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_registry():
    import yaml
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)


def list_orchestrable_jobs(registry: dict) -> list:
    jobs = []
    for job in registry.get("jobs", []):
        if job.get("orchestrable_by_openclaw") is True:
            jobs.append({
                "job_id": job["job_id"],
                "workflow": job.get("workflow"),
                "risk_level": job.get("risk_level", "unknown"),
                "requires_secret": job.get("requires_secret", False),
            })
    return jobs


def gh_workflow_dispatch(workflow_filename: str, ref: str = "sot/mainline", inputs: Optional[dict] = None):
    cmd = ["gh", "workflow", "run", workflow_filename, "--ref", ref]
    if inputs:
        for k, v in inputs.items():
            if v is not None:
                cmd.extend(["-f", f"{k}={v}"])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        output = result.stdout.strip()
        run_url = None
        for line in result.stderr.split("\n") if result.stderr else []:
            if "actions/runs/" in line:
                run_url = line.strip()
        return {"ok": True, "message": output, "url": run_url}
    return {"ok": False, "error": result.stderr.strip()}


GH_RUN_FIELDS = "databaseId,status,conclusion,displayTitle,url,createdAt"


def gh_get_latest_run(workflow_filename: str) -> Optional[dict]:
    cmd = ["gh", "run", "list", "--workflow", workflow_filename, "--limit", "1", "--json", GH_RUN_FIELDS]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if result.returncode == 0:
        runs = json.loads(result.stdout)
        if runs:
            return runs[0]
    return None


def gh_run_view(run_id: int) -> Optional[dict]:
    cmd = ["gh", "run", "view", str(run_id), "--json", GH_RUN_FIELDS]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if result.returncode == 0:
        return json.loads(result.stdout)
    return None


def classify_conclusion(conclusion: Optional[str]) -> str:
    mapping = {
        "success": "PASS",
        "failure": "FAIL",
        "cancelled": "BLOCKED",
        "timed_out": "BLOCKED",
        "action_required": "NEEDS_HUMAN_REVIEW",
        "skipped": "SKIPPED",
        "neutral": "PASS",
    }
    return mapping.get(conclusion or "", "UNKNOWN")


def propose_next_action(job_id: str, classification: str) -> str:
    proposals = {
        "PASS": f"✅ Job `{job_id}` completed successfully. Ready for next operational cycle.",
        "FAIL": f"❌ Job `{job_id}` failed. Check run logs — possible registry or workflow issue.",
        "BLOCKED": f"⏸ Job `{job_id}` was blocked. Check GitHub Actions queue or permissions.",
        "NEEDS_HUMAN_REVIEW": f"👤 Job `{job_id}` requires manual intervention on GitHub.",
        "SKIPPED": f"⏭ Job `{job_id}` was skipped.",
    }
    return proposals.get(classification, f"❓ Job `{job_id}` returned unknown status.")


def generate_report(job_id: str, run_data: dict, classification: str, next_action: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_dir = os.path.dirname(REPORT_PATH)
    os.makedirs(report_dir, exist_ok=True)

    content = f"""---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_OPERATIONAL_01_REPORT
doc_type: operational_report
generated_at: {now}
job_id: {job_id}
classification: {classification}
---

# Operational Orchestration Report

| Field | Value |
|---|---|
| **Date** | {now} |
| **Job ID** | {job_id} |
| **Run ID** | {run_data.get('databaseId', 'N/A')} |
| **Title** | {run_data.get('displayTitle', 'N/A')} |
| **Status** | {run_data.get('status', 'N/A')} |
| **Conclusion** | {run_data.get('conclusion', 'N/A')} |
| **Classification** | {classification} |
| **URL** | {run_data.get('url', 'N/A')} |

## Next Action

{next_action}

## Summary

OpenClaw orchestrated a GitHub Actions workflow_dispatch for job `{job_id}`.
The run was polled until completion. Classification and next action are provided above.
No automatic merge, push, or patch was applied.
"""

    with open(REPORT_PATH, "w") as f:
        f.write(content)
    print(f"Report generated: {REPORT_PATH}")


def cmd_list_jobs(args):
    registry = load_registry()
    jobs = list_orchestrable_jobs(registry)
    if not jobs:
        print("No orchestrable jobs found.")
        sys.exit(1)
    print(f"{'job_id':45s} {'workflow':50s} {'risk':8s} {'secret':8s}")
    print("-" * 115)
    for j in jobs:
        wf = j["workflow"] or "N/A"
        risk = j["risk_level"]
        secret = "yes" if j["requires_secret"] else "no"
        print(f"{j['job_id']:45s} {wf:50s} {risk:8s} {secret:8s}")
    print(f"\nTotal: {len(jobs)} orchestrable jobs")


def cmd_run_job(args):
    if not args.job_id:
        print("ERROR: --job-id is required")
        sys.exit(1)

    registry = load_registry()
    jobs = list_orchestrable_jobs(registry)
    target = None
    for j in jobs:
        if j["job_id"] == args.job_id:
            target = j
            break

    if not target:
        print(f"ERROR: Job '{args.job_id}' not found or not orchestrable.")
        print("Available jobs:")
        for j in jobs:
            print(f"  - {j['job_id']}")
        sys.exit(1)

    if not target["workflow"]:
        print(f"ERROR: Job '{args.job_id}' has no workflow file.")
        sys.exit(1)

    workflow_filename = os.path.basename(target["workflow"])
    print(f"Triggering workflow_dispatch for job '{args.job_id}'...")
    print(f"  Workflow: {workflow_filename}")
    print(f"  Ref: {args.ref}")

    res = gh_workflow_dispatch(workflow_filename, ref=args.ref, inputs={})
    if not res["ok"]:
        print(f"[FAIL] Trigger failed: {res['error']}")
        sys.exit(1)

    print(f"[PASS] Workflow triggered successfully")

    print("Waiting for the run to appear...")
    run_data = None
    retries = args.wait // 5 or 1
    for attempt in range(retries):
        time.sleep(5)
        run_data = gh_get_latest_run(workflow_filename)
        if run_data:
            break
        print(f"  (attempt {attempt + 1}/{retries} — run not yet visible)")

    if not run_data:
        print("[FAIL] Could not find run after dispatch.")
        sys.exit(1)

    run_id = run_data.get("databaseId")
    print(f"Found run: {run_id} ({run_data.get('status')})")
    print(f"  URL: {run_data.get('url')}")

    print(f"Polling run {run_id} (timeout={args.timeout}s, interval={args.interval}s)...")
    start = time.time()
    while time.time() - start < args.timeout:
        time.sleep(args.interval)
        current = gh_run_view(run_id)
        if not current:
            continue
        status = current.get("status")
        print(f"  Status: {status}")
        if status == "completed":
            run_data = current
            break
    else:
        print("[FAIL] Timeout reached while polling.")
        run_data = {"databaseId": run_id, "status": "timed_out", "conclusion": "timed_out", "displayTitle": "N/A", "url": "N/A"}

    conclusion = run_data.get("conclusion", "unknown")
    classification = classify_conclusion(conclusion)
    next_action = propose_next_action(args.job_id, classification)

    print(f"\n=== Result ===")
    print(f"Conclusion: {conclusion}")
    print(f"Classification: {classification}")
    print(f"Next action: {next_action}")

    generate_report(args.job_id, run_data, classification, next_action)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw GitHub Actions Orchestration")
    parser.add_argument("--list-jobs", action="store_true", help="List orchestrable jobs")
    parser.add_argument("--job-id", type=str, help="Job ID to orchestrate")
    parser.add_argument("--ref", type=str, default="sot/mainline", help="Git ref for workflow_dispatch")
    parser.add_argument("--wait", type=int, default=10, help="Seconds to wait after dispatch before polling")
    parser.add_argument("--timeout", type=int, default=300, help="Polling timeout in seconds")
    parser.add_argument("--interval", type=int, default=20, help="Polling interval in seconds")

    args = parser.parse_args()

    if args.list_jobs:
        cmd_list_jobs(args)
    elif args.job_id:
        cmd_run_job(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
