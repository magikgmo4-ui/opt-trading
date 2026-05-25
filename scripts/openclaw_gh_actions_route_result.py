#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime
from typing import Optional

REPORT_DIR = "docs/chantiers/GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01"
REPORT_PATH = os.path.join(REPORT_DIR, "RESULT_ROUTING_TEST_REPORT_01.md")


def classify_conclusion(conclusion: Optional[str], status: Optional[str] = None) -> str:
    mapping = {
        "success": "PASS",
        "failure": "FAIL",
        "cancelled": "BLOCKED",
        "timed_out": "BLOCKED",
        "action_required": "NEEDS_HUMAN_REVIEW",
        "neutral": "NEEDS_HUMAN_REVIEW",
        "skipped": "NEEDS_HUMAN_REVIEW",
    }
    if conclusion and conclusion in mapping:
        return mapping[conclusion]
    if conclusion is None or conclusion == "unknown":
        if status == "completed":
            return "NEEDS_HUMAN_REVIEW"
        return "BLOCKED"
    return "NEEDS_HUMAN_REVIEW"


def infer_probable_cause(conclusion: Optional[str], status: Optional[str] = None) -> Optional[str]:
    causes = {
        "failure": "Failed run — check run steps, tests, or build output",
        "cancelled": "Cancelled manually by user or by concurrency policy",
        "timed_out": "Exceeded maximum workflow timeout",
        "action_required": "Manual review or approval pending on GitHub",
        "neutral": "Neutral conclusion — no clear pass/fail signal",
        "skipped": "Job skipped by conditional workflow step",
    }
    if conclusion and conclusion in causes:
        return causes[conclusion]
    if not conclusion or conclusion == "unknown":
        if status == "completed":
            return "Completed without conclusion — possible API race condition"
        if status in ("in_progress", "queued", "pending"):
            return "Run not yet completed"
        return "Unknown state — investigate manually"
    return None


def logs_available(conclusion: Optional[str], status: Optional[str] = None) -> bool:
    if status == "completed" and conclusion:
        return True
    return False


def propose_next_action(job_id: str, classification: str) -> str:
    proposals = {
        "PASS": "ready_for_human_review",
        "FAIL": "inspect_logs_and_prepare_fix",
        "BLOCKED": "unblock_permissions_or_timeout",
        "NEEDS_HUMAN_REVIEW": "manual_review_required",
    }
    return proposals.get(classification, "manual_review_required")


def route_result(
    run_id: int,
    html_url: Optional[str],
    job_id: str,
    workflow: Optional[str],
    status: Optional[str],
    conclusion: Optional[str],
) -> dict:
    classification = classify_conclusion(conclusion, status)
    return {
        "run_id": run_id,
        "html_url": html_url,
        "job_id": job_id,
        "workflow": workflow,
        "status": status,
        "conclusion": conclusion,
        "classification": classification,
        "logs_available": logs_available(conclusion, status),
        "probable_cause": infer_probable_cause(conclusion, status),
        "next_action": propose_next_action(job_id, classification),
    }


def fetch_real_run(run_id: int) -> Optional[dict]:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        from modules.openclaw_github_actions_bridge.app.bridge import GitHubActionsBridge
        bridge = GitHubActionsBridge("docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml")
        url = f"https://api.github.com/repos/{bridge.repo}/actions/runs/{run_id}"
        import requests
        resp = requests.get(url, headers=bridge._get_headers())
        if resp.status_code != 200:
            print(f"[FAIL] API error {resp.status_code}: {resp.text}", file=sys.stderr)
            return None
        return resp.json()
    except Exception as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        return None


def generate_report(result: dict):
    os.makedirs(REPORT_DIR, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "---",
        "doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01_REPORT",
        "doc_type: result_routing_test_report",
        f"generated_at: {now[:10]}",
        f"classification: {result['classification']}",
        "---",
        "",
        "# Result Routing Test Report",
        "",
        "## Routed Result",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Run ID | {result['run_id']} |",
        f"| HTML URL | {result['html_url'] or 'N/A'} |",
        f"| Job ID | {result['job_id']} |",
        f"| Workflow | {result['workflow'] or 'N/A'} |",
        f"| Status | {result['status'] or 'N/A'} |",
        f"| Conclusion | {result['conclusion'] or 'N/A'} |",
        f"| Classification | {result['classification']} |",
        f"| Logs Available | {result['logs_available']} |",
        f"| Probable Cause | {result['probable_cause'] or 'N/A'} |",
        f"| Next Action | {result['next_action']} |",
        "",
        "## Verdict",
        "",
        f"- **No automatic merge, push, or patch was applied.**",
        f"- **Next action is a proposal — human validation required.**",
        "",
        f"Generated at: {now}",
    ]
    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Report: {REPORT_PATH}")


def cmd_list_classifications():
    header = f"{'conclusion':25s} {'status':20s} {'classification':25s} {'next_action':35s}"
    sep = "-" * 110
    print(header)
    print(sep)
    test_cases = [
        ("success", "completed"),
        ("failure", "completed"),
        ("cancelled", "completed"),
        ("timed_out", "completed"),
        ("action_required", "completed"),
        ("neutral", "completed"),
        ("skipped", "completed"),
        (None, "completed"),
        (None, "in_progress"),
        (None, "queued"),
        ("unknown", "completed"),
    ]
    for conclusion, status in test_cases:
        cls = classify_conclusion(conclusion, status)
        action = propose_next_action("test-job", cls)
        conc = conclusion or "null"
        print(f"{conc:25s} {status:20s} {cls:25s} {action:35s}")


def cmd_route(args):
    if args.run_id:
        raw = fetch_real_run(args.run_id)
        if not raw:
            sys.exit(1)
        job_id = args.job_id or str(args.run_id)
        result = route_result(
            run_id=args.run_id,
            html_url=raw.get("html_url"),
            job_id=job_id,
            workflow=raw.get("workflow", args.workflow),
            status=raw.get("status"),
            conclusion=raw.get("conclusion"),
        )
    elif args.simulate:
        result = route_result(
            run_id=args.run_id or 0,
            html_url=args.html_url,
            job_id=args.job_id or "simulated-job",
            workflow=args.workflow,
            status=args.status,
            conclusion=args.simulate,
        )
    else:
        print("ERROR: specify --run-id (real) or --simulate (test)")
        sys.exit(1)

    print(json.dumps(result, indent=2))
    generate_report(result)


def cmd_test():
    errors = []
    test_cases = [
        ("success", "completed", "PASS", "ready_for_human_review", True),
        ("failure", "completed", "FAIL", "inspect_logs_and_prepare_fix", True),
        ("cancelled", "completed", "BLOCKED", "unblock_permissions_or_timeout", True),
        ("timed_out", "completed", "BLOCKED", "unblock_permissions_or_timeout", True),
        ("action_required", "completed", "NEEDS_HUMAN_REVIEW", "manual_review_required", True),
        ("neutral", "completed", "NEEDS_HUMAN_REVIEW", "manual_review_required", True),
        ("skipped", "completed", "NEEDS_HUMAN_REVIEW", "manual_review_required", True),
        (None, "completed", "NEEDS_HUMAN_REVIEW", "manual_review_required", False),
        (None, "in_progress", "BLOCKED", "unblock_permissions_or_timeout", False),
        (None, "queued", "BLOCKED", "unblock_permissions_or_timeout", False),
        ("unknown", "completed", "NEEDS_HUMAN_REVIEW", "manual_review_required", False),
    ]

    print(f"{'#':3s} {'conclusion':20s} {'status':15s} {'expect_cls':25s} {'expect_action':35s} {'result':10s}")
    print("-" * 115)
    for i, (conclusion, status, exp_cls, exp_action, exp_logs) in enumerate(test_cases, 1):
        cls = classify_conclusion(conclusion, status)
        action = propose_next_action("test-job", cls)
        logs = logs_available(conclusion, status)
        ok = cls == exp_cls and action == exp_action
        status_str = "PASS" if ok else "FAIL"
        if not ok:
            err = f"  Case {i}: conclusion={conclusion}, status={status}: expected cls={exp_cls}, got cls={cls}; expected action={exp_action}, got action={action}"
            errors.append(err)
        conc = conclusion or "null"
        print(f"{i:3d} {conc:20s} {status:15s} {exp_cls:25s} {exp_action:35s} {status_str:10s}")

    if errors:
        print("\nFAILURES:")
        for e in errors:
            print(e)
        sys.exit(1)
    print(f"\nAll {len(test_cases)} test cases PASS.")
    print("No mutation dangerous — no API calls, no dispatch, no push.")


def main():
    parser = argparse.ArgumentParser(description="OpenClaw GitHub Actions Result Router")
    parser.add_argument("--list-classifications", action="store_true", help="List all classification mappings")
    parser.add_argument("--route", action="store_true", help="Route a run result")
    parser.add_argument("--test", action="store_true", help="Run classification mapping tests")
    parser.add_argument("--run-id", type=int, help="GitHub Actions run ID (real)")
    parser.add_argument("--job-id", type=str, help="Job identifier")
    parser.add_argument("--workflow", type=str, help="Workflow filename")
    parser.add_argument("--simulate", type=str, choices=["success", "failure", "cancelled", "timed_out", "action_required", "neutral", "skipped"], help="Simulated conclusion for testing")
    parser.add_argument("--status", type=str, default="completed", help="Run status (for --simulate)")
    parser.add_argument("--html-url", type=str, default="https://github.com/simulated/run", help="HTML URL (for --simulate)")

    args = parser.parse_args()

    if args.list_classifications:
        cmd_list_classifications()
    elif args.route:
        cmd_route(args)
    elif args.test:
        cmd_test()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
