#!/usr/bin/env python3
import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

BRIDGE_PATH = REPO_ROOT / "modules" / "openclaw_github_actions_bridge" / "app" / "bridge.py"
REGISTRY_PATH = "docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml"

def _load_script_module(module_name: str, script_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_bridge():
    if not BRIDGE_PATH.exists():
        return None
    mod = _load_script_module("bridge", BRIDGE_PATH)
    if mod is None:
        return None
    return mod.GitHubActionsBridge


def validate_env(verbose: bool = False) -> dict:
    gh_token = os.getenv("GITHUB_TOKEN")
    gh_repo = os.getenv("GITHUB_REPOSITORY")
    result = {
        "GITHUB_TOKEN": bool(gh_token),
        "GITHUB_REPOSITORY": bool(gh_repo),
        "bridge_available": BRIDGE_PATH.exists(),
        "registry_available": Path(REGISTRY_PATH).exists(),
        "all_valid": False,
    }
    result["all_valid"] = (
        result["GITHUB_TOKEN"]
        and result["GITHUB_REPOSITORY"]
        and result["bridge_available"]
        and result["registry_available"]
    )
    if verbose:
        result["GITHUB_REPOSITORY_value"] = gh_repo
        result["GITHUB_TOKEN_prefix"] = (gh_token or "")[:8] + "..." if gh_token else None
        result["bridge_path"] = str(BRIDGE_PATH)
        result["registry_path"] = REGISTRY_PATH
    return result


def get_bridge(registry_path: str = REGISTRY_PATH):
    bridge_cls = _load_bridge()
    if bridge_cls is None:
        return None, "Bridge module not found"
    try:
        bridge = bridge_cls(registry_path)
        return bridge, None
    except ValueError as e:
        return None, str(e)


def cmd_validate(args):
    result = validate_env(verbose=args.verbose)
    all_valid = result.pop("all_valid")
    for k, v in result.items():
        status = "OK" if v else "MISSING"
        print(f"  {k:30s} {status}")
    if all_valid:
        print("\nAll env vars and dependencies present.")
    else:
        print("\nSome requirements missing. Use --verbose for details.", file=sys.stderr)
        sys.exit(1)


def cmd_run_info(args):
    bridge, err = get_bridge()
    if err:
        print(f"[FAIL] {err}", file=sys.stderr)
        sys.exit(1)
    url = f"https://api.github.com/repos/{bridge.repo}/actions/runs/{args.run_id}"
    import requests
    resp = requests.get(url, headers=bridge._get_headers())
    if resp.status_code != 200:
        print(f"[FAIL] API error {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)
    data = resp.json()
    print(json.dumps({
        "run_id": data.get("id"),
        "status": data.get("status"),
        "conclusion": data.get("conclusion"),
        "html_url": data.get("html_url"),
        "workflow": data.get("workflow", {}).get("path"),
        "display_title": data.get("display_title"),
    }, indent=2))


def cmd_pipeline(args):
    bridge, err = get_bridge()
    if err:
        print(f"[FAIL] {err}", file=sys.stderr)
        sys.exit(1)

    print(f"Pipeline: route result for run {args.run_id}")

    route_result_mod = _load_script_module(
        "openclaw_gh_actions_route_result",
        REPO_ROOT / "scripts" / "openclaw_gh_actions_route_result.py",
    )
    if route_result_mod is None:
        print("[FAIL] Could not load route_result module", file=sys.stderr)
        sys.exit(1)

    import requests
    url = f"https://api.github.com/repos/{bridge.repo}/actions/runs/{args.run_id}"
    resp = requests.get(url, headers=bridge._get_headers())
    if resp.status_code != 200:
        print(f"[FAIL] API error {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)
    raw = resp.json()
    result = route_result_mod.route_result(
        run_id=args.run_id,
        html_url=raw.get("html_url"),
        job_id=args.job_id or str(args.run_id),
        workflow=raw.get("workflow", {}).get("path"),
        status=raw.get("status"),
        conclusion=raw.get("conclusion"),
    )
    print(json.dumps(result, indent=2))

    if result.get("classification") == "FAIL" and args.analyze:
        analyzer_mod = _load_script_module(
            "openclaw_gh_actions_analyze_failure_logs",
            REPO_ROOT / "scripts" / "openclaw_gh_actions_analyze_failure_logs.py",
        )
        if analyzer_mod is None:
            print("[WARN] analyzer module not loaded — skipping analysis")
        else:
            analyzer = analyzer_mod.FailureAnalyzer(bridge=bridge)
            analysis = analyzer.analyze_run(args.run_id)
            print("\n--- Failure Analysis ---")
            print(json.dumps(analysis, indent=2))


def cmd_simulate_pipeline(args):
    route_result_mod = _load_script_module(
        "openclaw_gh_actions_route_result",
        REPO_ROOT / "scripts" / "openclaw_gh_actions_route_result.py",
    )
    if route_result_mod is None:
        print("[FAIL] Could not load route_result module", file=sys.stderr)
        sys.exit(1)

    result = route_result_mod.route_result(
        run_id=args.run_id or 0,
        html_url="https://github.com/simulated/run",
        job_id=args.job_id or "simulated-job",
        workflow=args.workflow,
        status=args.status,
        conclusion=args.conclusion,
    )
    print(json.dumps(result, indent=2))

    if result.get("classification") == "FAIL" and args.analyze:
        analyzer_mod = _load_script_module(
            "openclaw_gh_actions_analyze_failure_logs",
            REPO_ROOT / "scripts" / "openclaw_gh_actions_analyze_failure_logs.py",
        )
        if analyzer_mod is None:
            print("[WARN] analyzer module not loaded")
            return
        analyzer = analyzer_mod.FailureAnalyzer()
        dummy_logs = analyzer_mod.CLASSIFICATIONS.get("TEST_FAILURE", {}).get("patterns", [""])[0]
        classification = analyzer.classify_error(dummy_logs)
        analysis = {
            "run_id": args.run_id or 0,
            "simulation": True,
            "failed_jobs_count": 1,
            "primary_classification": classification["classification"],
            "primary_next_action": classification["next_action"],
            "dangerous_action_executed": False,
        }
        print("\n--- Simulated Failure Analysis ---")
        print(json.dumps(analysis, indent=2))


def cmd_test(args):
    errors = []

    env = {"GITHUB_TOKEN": "test-token", "GITHUB_REPOSITORY": "owner/repo"}
    if args.with_env:
        for k, v in env.items():
            os.environ.setdefault(k, v)

    print("1. validate_env() — no env")
    result = validate_env()
    if result["all_valid"]:
        errors.append("validate_env should return False without env vars")

    if args.with_env:
        for k, v in env.items():
            os.environ[k] = v
        result = validate_env()
        if not result["all_valid"]:
            errors.append("validate_env should return True with env vars set")
        print("   PASS" if result["all_valid"] else "   FAIL")

    print("2. Bridge import (module exists)")
    bridge_cls = _load_bridge()
    if bridge_cls is None:
        errors.append("Bridge module should loadable")
        print("   FAIL — bridge module not found")
    else:
        print("   PASS")

    print("3. Simulate pipeline (route_result dispatch)")
    route_result_mod = _load_script_module(
        "openclaw_gh_actions_route_result",
        REPO_ROOT / "scripts" / "openclaw_gh_actions_route_result.py",
    )
    if route_result_mod is None:
        errors.append("route_result module should be loadable")
        print("   FAIL")
    else:
        test_cases = [
            ("success", "completed", "PASS"),
            ("failure", "completed", "FAIL"),
            ("cancelled", "completed", "BLOCKED"),
        ]
        for conclusion, status, expected in test_cases:
            result = route_result_mod.route_result(
                run_id=0, html_url=None, job_id="test",
                workflow=None, status=status, conclusion=conclusion,
            )
            ok = result["classification"] == expected
            if not ok:
                errors.append(f"route_result({conclusion}, {status}): expected {expected}, got {result['classification']}")
            print(f"   {'PASS' if ok else 'FAIL'} {conclusion:20s} -> {result['classification']}")

    print("4. Simulate pipeline (analyze failure)")
    analyzer_mod = _load_script_module(
        "openclaw_gh_actions_analyze_failure_logs",
        REPO_ROOT / "scripts" / "openclaw_gh_actions_analyze_failure_logs.py",
    )
    if analyzer_mod is None:
        errors.append("analyzer module should be loadable")
        print("   FAIL")
    else:
        analyzer = analyzer_mod.FailureAnalyzer()
        res = analyzer.classify_error("FAILED tests/test_api.py")
        ok = res["classification"] == "TEST_FAILURE"
        if not ok:
            errors.append(f"classify_error: expected TEST_FAILURE, got {res['classification']}")
        print(f"   {'PASS' if ok else 'FAIL'} classify_error -> {res['classification']}")

    print("5. Simulate pipeline (enrich fix)")
    fix_path = REPO_ROOT / "scripts" / "openclaw_gh_actions_analyze_failure_logs_fix.py"
    if fix_path.exists():
        fix_mod = _load_script_module("openclaw_gh_actions_analyze_failure_logs_fix", fix_path)
        if fix_mod is None:
            errors.append("fix module should be loadable")
            print("   FAIL")
        else:
            print("   PASS — fix module loaded")
    else:
        print("   SKIP — fix module not found")

    if errors:
        print(f"\nFAILURES ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("\nAll tests passed.")


def main():
    parser = argparse.ArgumentParser(description="OpenClaw GitHub Actions Live Environment")
    sub = parser.add_subparsers(dest="command")

    p_validate = sub.add_parser("validate", help="Validate env vars and dependencies")
    p_validate.add_argument("--verbose", action="store_true")

    p_run_info = sub.add_parser("run-info", help="Fetch run info from GitHub API")
    p_run_info.add_argument("--run-id", type=int, required=True)

    p_pipeline = sub.add_parser("pipeline", help="Run live pipeline (route + analyze)")
    p_pipeline.add_argument("--run-id", type=int, required=True)
    p_pipeline.add_argument("--job-id", type=str)
    p_pipeline.add_argument("--analyze", action="store_true", help="Run failure analysis on FAIL")

    p_sim = sub.add_parser("simulate-pipeline", help="Simulate pipeline without API")
    p_sim.add_argument("--run-id", type=int, default=0)
    p_sim.add_argument("--job-id", type=str)
    p_sim.add_argument("--workflow", type=str)
    p_sim.add_argument("--status", type=str, default="completed")
    p_sim.add_argument("--conclusion", type=str, required=True,
                       choices=["success", "failure", "cancelled", "timed_out",
                                "action_required", "neutral", "skipped"])
    p_sim.add_argument("--analyze", action="store_true")

    p_test = sub.add_parser("test", help="Run self-tests")
    p_test.add_argument("--with-env", action="store_true", help="Set test env vars")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "validate": cmd_validate,
        "run-info": cmd_run_info,
        "pipeline": cmd_pipeline,
        "simulate-pipeline": cmd_simulate_pipeline,
        "test": cmd_test,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
