import os
import sys
import json
import time
from datetime import datetime
from modules.openclaw_github_actions_bridge.app.bridge import GitHubActionsBridge

def run_dry_run_test():
    print("=== OpenClaw GitHub Actions Orchestration Dry-Run ===")
    
    registry_path = "docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml"
    
    # Check environment
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    
    if not token or not repo:
        print("[FAIL] GITHUB_TOKEN or GITHUB_REPOSITORY not set.")
        sys.exit(1)
        
    try:
        bridge = GitHubActionsBridge(registry_path)
    except Exception as e:
        print(f"[FAIL] Failed to initialize bridge: {e}")
        sys.exit(1)

    # Job to test (low risk, dry-run)
    job_id = "github-actions-job-registry-check"
    print(f"Testing job: {job_id}")
    
    # 1. Trigger
    res = bridge.trigger_workflow(job_id, inputs={})
    if not res.get("ok"):
        print(f"[FAIL] Trigger failed: {res.get('error')}")
        sys.exit(1)
    
    print(f"[PASS] {res.get('message')}")
    
    # 2. Wait for the run to appear and poll status
    print("Waiting for run to start...")
    time.sleep(10) # Wait a bit for GitHub to register the dispatch
    
    job = bridge.get_job(job_id)
    workflow_filename = os.path.basename(job["workflow"]) if job.get("workflow") else "strict-workers-smoke.yml" # fallback for dry-run if null in registry
    
    latest_run = bridge.get_latest_run(workflow_filename)
    if not latest_run:
        print("[FAIL] Could not find any run for the workflow.")
        sys.exit(1)
        
    run_id = latest_run["id"]
    print(f"Found latest run: {run_id} ({latest_run.get('status')})")
    
    # 3. Poll
    print(f"Polling run {run_id}...")
    poll_res = bridge.poll_run_status(run_id, timeout_s=300, interval_s=20)
    
    if poll_res.get("ok"):
        print(f"[PASS] Run completed with conclusion: {poll_res.get('conclusion')}")
        generate_report(job_id, poll_res)
    else:
        print(f"[FAIL] Polling failed: {poll_res.get('error')}")
        sys.exit(1)

def generate_report(job_id, result):
    report_path = "docs/chantiers/GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_DRY_RUN_REPORT_01/ORCHESTRATION_REPORT_01.md"
    
    status = "PASS" if result.get("conclusion") == "success" else "FAIL"
    if result.get("conclusion") in ["cancelled", "timed_out"]:
        status = "BLOCKED"
        
    content = f"""# Orchestration Report: {job_id}

- **Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Job ID**: {job_id}
- **Run ID**: {result.get('run_id')}
- **Status**: {status}
- **Conclusion**: {result.get('conclusion')}
- **URL**: {result.get('html_url')}

## Summary
The OpenClaw-GitHub Actions orchestration dry-run has been completed.
The bridge successfully triggered the workflow and polled the status until completion.

## Verdict
- **{status}**
"""
    with open(report_path, 'w') as f:
        f.write(content)
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    run_dry_run_test()
