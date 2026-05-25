#!/usr/bin/env python3
import argparse
import json
import os
import sys
import yaml

REGISTRY_PATH = "docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml"

ALLOWED_RISK_LEVELS_DEFAULT = ["low"]
ALLOWED_SURFACES_DEFAULT = ["github_actions"]
ALLOWED_STATUSES = ["implemented_existing", "implemented_child_go"]


def load_registry():
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)


def get_all_jobs(registry: dict) -> list:
    return registry.get("jobs", [])


def reject_job(job: dict, reason: str) -> dict:
    return {
        "job_id": job.get("job_id", "unknown"),
        "decision": "REJECTED",
        "reason": reason,
    }


def accept_job(job: dict) -> dict:
    return {
        "job_id": job["job_id"],
        "decision": "SELECTED",
        "workflow": job.get("workflow"),
        "risk_level": job.get("risk_level"),
        "owner_surface": job.get("owner_surface"),
        "requires_secret": job.get("requires_secret", False),
        "role": job.get("role"),
        "status": job.get("status"),
    }


def route_jobs(
    registry: dict,
    job_id_filter: str = None,
    role_filter: str = None,
    risk_level_limit: list = None,
    allowed_surfaces: list = None,
    allow_secrets: bool = False,
    allow_medium_risk: bool = False,
    allow_openclaw_surface: bool = False,
):
    if risk_level_limit is None:
        risk_level_limit = ALLOWED_RISK_LEVELS_DEFAULT
    if allowed_surfaces is None:
        allowed_surfaces = ALLOWED_SURFACES_DEFAULT

    if allow_medium_risk and "medium" not in risk_level_limit:
        risk_level_limit = risk_level_limit + ["medium"]

    all_jobs = get_all_jobs(registry)
    rejected = []
    selected = []

    for job in all_jobs:
        jid = job.get("job_id", "")

        if job_id_filter and jid != job_id_filter:
            continue
        if role_filter and job.get("role") != role_filter:
            continue

        if not job.get("orchestrable_by_openclaw"):
            rejected.append(reject_job(job, "NOT_ORCHESTRABLE"))
            continue

        if not job.get("workflow"):
            rejected.append(reject_job(job, "NO_WORKFLOW"))
            continue

        risk = job.get("risk_level", "unknown")
        if risk not in risk_level_limit:
            rejected.append(reject_job(job, f"RISK_TOO_HIGH (risk={risk}, allowed={risk_level_limit})"))
            continue

        surface = job.get("owner_surface", "unknown")
        if surface not in allowed_surfaces:
            rejected.append(reject_job(job, f"SURFACE_NOT_ALLOWED (surface={surface}, allowed={allowed_surfaces})"))
            continue

        if job.get("requires_secret") and not allow_secrets:
            rejected.append(reject_job(job, "SECRET_REQUIRED (use --allow-secrets)"))
            continue

        status = job.get("status", "")
        if status not in ALLOWED_STATUSES:
            rejected.append(reject_job(job, f"STATUS_NOT_READY (status={status}, allowed={ALLOWED_STATUSES})"))
            continue

        selected.append(accept_job(job))

    return selected, rejected


def generate_routing_report(selected, rejected, classification="PASS", run_data=None):
    report_dir = os.path.join(
        "docs/chantiers",
        "GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_ROUTING_01",
    )
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "ROUTING_TEST_REPORT_01.md")

    lines = [
        "---",
        "doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_ROUTING_01_REPORT",
        "doc_type: routing_test_report",
        "generated_at: 2026-05-25",
        "classification: " + classification,
        "---",
        "",
        "# Routing Test Report",
        "",
        "## Selected Jobs",
    ]

    if selected:
        for s in selected:
            lines.append(f"- **{s['job_id']}** — workflow={s['workflow']}, risk={s['risk_level']}, surface={s['owner_surface']}")
    else:
        lines.append("(none)")

    lines.extend(["", "## Rejected Jobs", ""])
    if rejected:
        for r in rejected:
            lines.append(f"- **{r['job_id']}** — reason: {r['reason']}")
    else:
        lines.append("(none)")

    if run_data:
        lines.extend([
            "",
            "## Execution",
            "",
            f"| Field | Value |",
            f"|---|---|",
            f"| Run ID | {run_data.get('databaseId', 'N/A')} |",
            f"| Conclusion | {run_data.get('conclusion', 'N/A')} |",
            f"| Status | {run_data.get('status', 'N/A')} |",
            f"| URL | {run_data.get('url', 'N/A')} |",
            f"| Classification | {classification} |",
        ])

    lines.extend([
        "",
        "## Verdict",
        "",
        f"- **Classification**: {classification}",
        f"- **Selected count**: {len(selected)}",
        f"- **Rejected count**: {len(rejected)}",
        "- **No automatic merge, push, or patch was applied.**",
    ])

    with open(report_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Report: {report_path}")


def cmd_list(args):
    registry = load_registry()
    selected, rejected = route_jobs(
        registry,
        risk_level_limit=args.risk_level_limit,
        allowed_surfaces=args.allowed_surfaces,
        allow_secrets=args.allow_secrets,
        allow_medium_risk=args.allow_medium_risk,
        allow_openclaw_surface=args.allow_openclaw_surface,
    )
    print(f"{'job_id':50s} {'workflow':55s} {'risk':10s} {'surface':20s} {'secret':8s} {'decision':12s}")
    print("-" * 160)
    for s in selected:
        wf = s["workflow"] or "N/A"
        sec = "yes" if s["requires_secret"] else "no"
        print(f"{s['job_id']:50s} {wf:55s} {s['risk_level']:10s} {s['owner_surface']:20s} {sec:8s} {'SELECTED':12s}")
    for r in rejected:
        wf = "N/A"
        risk = "N/A"
        surface = "N/A"
        sec = "N/A"
        print(f"{r['job_id']:50s} {wf:55s} {risk:10s} {surface:20s} {sec:8s} REJECTED:{r['reason']}")
    print(f"\nSelected: {len(selected)}  Rejected: {len(rejected)}  Total: {len(selected) + len(rejected)}")


def cmd_filter(args):
    registry = load_registry()
    selected, rejected = route_jobs(
        registry,
        job_id_filter=args.job_id,
        role_filter=args.role,
        risk_level_limit=args.risk_level_limit,
        allowed_surfaces=args.allowed_surfaces,
        allow_secrets=args.allow_secrets,
        allow_medium_risk=args.allow_medium_risk,
        allow_openclaw_surface=args.allow_openclaw_surface,
    )
    output = {
        "selected_jobs": selected,
        "rejected_jobs": rejected,
        "selected_count": len(selected),
        "rejected_count": len(rejected),
    }
    print(json.dumps(output, indent=2))


def cmd_route(args):
    registry = load_registry()
    selected, rejected = route_jobs(
        registry,
        job_id_filter=args.job_id,
        role_filter=args.role,
        risk_level_limit=args.risk_level_limit,
        allowed_surfaces=args.allowed_surfaces,
        allow_secrets=args.allow_secrets,
        allow_medium_risk=args.allow_medium_risk,
        allow_openclaw_surface=args.allow_openclaw_surface,
    )
    print(f"Selected: {len(selected)}  Rejected: {len(rejected)}")
    for s in selected:
        print(f"  ✅ {s['job_id']} — dispatch_allowed=true")
    for r in rejected:
        print(f"  ❌ {r['job_id']} — {r['reason']}")

    if args.execute and len(selected) == 1:
        target = selected[0]
        print(f"\nExecuting workflow_dispatch for {target['job_id']}...")
        from openclaw_gh_actions_orchestrate import gh_workflow_dispatch, gh_get_latest_run, gh_run_view, classify_conclusion, propose_next_action
        import time

        wf = os.path.basename(target["workflow"])
        res = gh_workflow_dispatch(wf, ref=args.ref)
        if not res["ok"]:
            print(f"[FAIL] Trigger: {res['error']}")
            return
        print(f"[PASS] Triggered {wf}")

        run_data = None
        for attempt in range(args.wait // 5 or 1):
            time.sleep(5)
            run_data = gh_get_latest_run(wf)
            if run_data:
                break

        if not run_data:
            print("[FAIL] Run not found after dispatch")
            return

        run_id = run_data.get("databaseId")
        print(f"Run {run_id}: polling...")
        start = time.time()
        while time.time() - start < args.timeout:
            time.sleep(args.interval)
            current = gh_run_view(run_id)
            if not current:
                continue
            print(f"  Status: {current.get('status')}")
            if current.get("status") == "completed":
                run_data = current
                break

        conclusion = run_data.get("conclusion", "unknown")
        classification = classify_conclusion(conclusion)
        next_action = propose_next_action(target["job_id"], classification)
        print(f"\nConclusion: {conclusion}")
        print(f"Classification: {classification}")
        print(f"Next: {next_action}")
        generate_routing_report(selected, rejected, classification, run_data)
    elif args.execute:
        print("ERROR: --execute requires exactly 1 selected job")
        sys.exit(1)
    else:
        generate_routing_report(selected, rejected)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw GitHub Actions Job Router")
    parser.add_argument("--list", action="store_true", help="List all jobs with routing decisions")
    parser.add_argument("--filter", action="store_true", help="Filter jobs and output JSON")
    parser.add_argument("--route", action="store_true", help="Route and optionally execute a job")
    parser.add_argument("--job-id", type=str, help="Filter by job_id")
    parser.add_argument("--role", type=str, help="Filter by role")
    parser.add_argument("--risk-level-limit", nargs="*", default=["low"], help="Allowed risk levels")
    parser.add_argument("--allowed-surfaces", nargs="*", default=["github_actions"], help="Allowed owner surfaces")
    parser.add_argument("--allow-secrets", action="store_true", help="Allow jobs requiring secrets")
    parser.add_argument("--allow-medium-risk", action="store_true", help="Allow medium risk jobs")
    parser.add_argument("--allow-openclaw-surface", action="store_true", help="Allow openclaw surface")
    parser.add_argument("--execute", action="store_true", help="Execute workflow_dispatch on selected job")
    parser.add_argument("--ref", type=str, default="sot/mainline", help="Git ref")
    parser.add_argument("--wait", type=int, default=30, help="Wait for run discovery")
    parser.add_argument("--timeout", type=int, default=300, help="Polling timeout")
    parser.add_argument("--interval", type=int, default=20, help="Polling interval")

    args = parser.parse_args()

    if args.list:
        cmd_list(args)
    elif args.filter:
        cmd_filter(args)
    elif args.route:
        cmd_route(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
