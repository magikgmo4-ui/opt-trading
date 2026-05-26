#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.openclaw_github_actions_bridge.app.bridge import GitHubActionsBridge

# Canonical Classifications
CLASSIFICATIONS = {
    "TEST_FAILURE": {
        "patterns": [r"FAILED tests/", r"pytest", r"AssertionError", r"failed in .* seconds"],
        "next_action": "Fix code or update tests.",
        "confidence": "High"
    },
    "YAML_WORKFLOW_FAILURE": {
        "patterns": [r"invalid workflow", r"yaml: line", r"syntax error", r"workflow is invalid"],
        "next_action": "Correct YAML syntax in .github/workflows/.",
        "confidence": "High"
    },
    "PERMISSION_FAILURE": {
        "patterns": [r"Permission denied", r"403", r"resource not accessible", r"Resource not accessible by integration"],
        "next_action": "Check GITHUB_TOKEN permissions or secrets.",
        "confidence": "Medium"
    },
    "TIMEOUT": {
        "patterns": [r"timed_out", r"Job exceeded time limit", r"The operation was canceled"],
        "next_action": "Optimize job performance or increase timeout.",
        "confidence": "High"
    },
    "MISSING_FILE": {
        "patterns": [r"No such file", r"File not found", r"ENOENT"],
        "next_action": "Verify file existence or build artifact creation.",
        "confidence": "Medium"
    },
    "FILE_SCOPE_FAILURE": {
        "patterns": [r"FAIL: file outside GO scope", r"gate/file-scope failed"],
        "next_action": "Update FILE_SCOPE.txt for the current GO.",
        "confidence": "High"
    },
    "NO_LOCK_OVERLAP_FAILURE": {
        "patterns": [r"FAIL: changed file is also claimed", r"gate/no-lock-overlap failed"],
        "next_action": "Release scope from previous GO or resolve conflict.",
        "confidence": "High"
    },
    "NETWORK_OR_API_FAILURE": {
        "patterns": [r"Connection timeout", r"Rate limit exceeded", r"API error", r"Could not resolve host"],
        "next_action": "Retry later or check external service status.",
        "confidence": "Medium"
    },
    "UNKNOWN_FAILURE": {
        "patterns": [],
        "next_action": "Human review of full logs required.",
        "confidence": "Low"
    }
}

class FailureAnalyzer:
    def __init__(self, bridge: Optional[GitHubActionsBridge] = None):
        self.bridge = bridge

    def classify_error(self, logs: str) -> Dict[str, Any]:
        for cls_name, info in CLASSIFICATIONS.items():
            if cls_name == "UNKNOWN_FAILURE":
                continue
            for pattern in info["patterns"]:
                if re.search(pattern, logs, re.IGNORECASE):
                    return {
                        "classification": cls_name,
                        "confidence": info["confidence"],
                        "next_action": info["next_action"]
                    }
        
        return {
            "classification": "UNKNOWN_FAILURE",
            "confidence": CLASSIFICATIONS["UNKNOWN_FAILURE"]["confidence"],
            "next_action": CLASSIFICATIONS["UNKNOWN_FAILURE"]["next_action"]
        }

    def analyze_run(self, run_id: int) -> Dict[str, Any]:
        if not self.bridge:
            return {"ok": False, "error": "Bridge not initialized"}

        # 1. Get jobs
        jobs_resp = self.bridge.get_run_jobs(run_id)
        if not jobs_resp.get("ok"):
            return jobs_resp

        jobs = jobs_resp.get("jobs", [])
        failed_jobs = [j for j in jobs if j.get("conclusion") in ["failure", "cancelled", "timed_out"]]
        
        analysis_results = []
        for job in failed_jobs:
            job_id = job.get("id")
            job_name = job.get("name")
            
            # 2. Get logs
            logs_resp = self.bridge.get_job_logs(job_id)
            logs = logs_resp.get("content", "") if logs_resp.get("ok") else ""
            
            # 3. Classify
            classification = self.classify_error(logs)
            
            analysis_results.append({
                "job_id": job_id,
                "job_name": job_name,
                "conclusion": job.get("conclusion"),
                "logs_available": logs_resp.get("ok", False),
                **classification
            })

        # 4. Summary
        if not analysis_results:
            return {
                "run_id": run_id,
                "status": "PASS",
                "message": "No failed jobs detected"
            }

        primary_failure = analysis_results[0]
        return {
            "run_id": run_id,
            "failed_jobs_count": len(failed_jobs),
            "primary_classification": primary_failure["classification"],
            "primary_next_action": primary_failure["next_action"],
            "details": analysis_results,
            "dangerous_action_executed": False
        }

def main():
    parser = argparse.ArgumentParser(description="OpenClaw GitHub Actions Failure Log Analyzer")
    parser.add_argument("--run-id", type=int, help="GitHub Run ID to analyze")
    parser.add_argument("--simulate", choices=CLASSIFICATIONS.keys(), help="Simulate a specific failure type")
    parser.add_argument("--test", action="store_true", help="Run self-tests")
    parser.add_argument("--output", help="Path to write JSON output")
    parser.add_argument("--registry", default="docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml", help="Path to jobs registry")

    args = parser.parse_args()

    analyzer = FailureAnalyzer()
    
    if args.simulate:
        # Create dummy log matching the simulation type
        dummy_logs = ""
        if args.simulate != "UNKNOWN_FAILURE":
            dummy_logs = CLASSIFICATIONS[args.simulate]["patterns"][0].replace(r"\\", "").replace(r".*", "XYZ")
        
        result = {
            "run_id": 12345,
            "simulation": True,
            "failed_jobs_count": 1,
            "primary_classification": args.simulate,
            "primary_next_action": CLASSIFICATIONS[args.simulate]["next_action"],
            "details": [{
                "job_name": "simulated_job",
                "classification": args.simulate,
                "next_action": CLASSIFICATIONS[args.simulate]["next_action"],
                "confidence": CLASSIFICATIONS[args.simulate]["confidence"]
            }],
            "dangerous_action_executed": False
        }
    elif args.test:
        print("Running classification tests...")
        test_cases = [
            ("FAILED tests/test_api.py", "TEST_FAILURE"),
            ("yaml: line 10: mapping values not allowed", "YAML_WORKFLOW_FAILURE"),
            ("Permission denied (publickey)", "PERMISSION_FAILURE"),
            ("The operation was canceled because it timed out", "TIMEOUT"),
            ("No such file or directory: 'config.json'", "MISSING_FILE"),
            ("FAIL: file outside GO scope: scripts/dangerous.py", "FILE_SCOPE_FAILURE"),
            ("FAIL: changed file is also claimed by another GO scope", "NO_LOCK_OVERLAP_FAILURE"),
            ("Could not resolve host: api.github.com", "NETWORK_OR_API_FAILURE"),
            ("Random error message", "UNKNOWN_FAILURE")
        ]
        
        all_pass = True
        for logs, expected in test_cases:
            res = analyzer.classify_error(logs)
            if res["classification"] == expected:
                print(f"✓ PASS: '{logs[:30]}...' -> {expected}")
            else:
                print(f"✗ FAIL: '{logs[:30]}...' -> {res['classification']} (Expected: {expected})")
                all_pass = False
        
        if not all_pass:
            sys.exit(1)
        print("All tests passed.")
        return
    elif args.run_id:
        try:
            bridge = GitHubActionsBridge(args.registry)
            analyzer.bridge = bridge
            result = analyzer.analyze_run(args.run_id)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Report written to {args.output}")
    else:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
