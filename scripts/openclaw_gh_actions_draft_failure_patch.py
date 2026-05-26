#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent

CLASSIFICATIONS_PATCHABLE = {
    "TEST_FAILURE": {
        "patchable": True,
        "description": "Draft fix for failing test"
    },
    "YAML_WORKFLOW_FAILURE": {
        "patchable": True,
        "description": "Correct YAML syntax in workflow"
    },
    "MISSING_FILE": {
        "patchable": True,
        "description": "Create missing file"
    },
    "FILE_SCOPE_FAILURE": {
        "patchable": True,
        "description": "Update FILE_SCOPE.txt"
    },
    "NO_LOCK_OVERLAP_FAILURE": {
        "patchable": True,
        "description": "Resolve scope overlap conflict"
    },
    "TIMEOUT": {
        "patchable": True,
        "description": "Increase workflow timeout"
    },
    "PERMISSION_FAILURE": {
        "patchable": False,
        "description": "Cannot patch permissions — manual action required"
    },
    "NETWORK_OR_API_FAILURE": {
        "patchable": False,
        "description": "Cannot patch network — manual action required"
    },
    "UNKNOWN_FAILURE": {
        "patchable": False,
        "description": "Cannot patch — human review required"
    }
}

def _draft_patches(classification: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    if classification == "TEST_FAILURE":
        log_snippet = analysis.get("details", [{}])[0].get("log_snippet", "")
        return [{
            "file": "tests/",
            "action": "human_review_and_fix",
            "diff": None,
            "note": f"Review failing test. Log context: {log_snippet[:200] if log_snippet else 'check analysis report'}"
        }]

    elif classification == "YAML_WORKFLOW_FAILURE":
        return [{
            "file": ".github/workflows/",
            "action": "correct_yaml_syntax",
            "diff": None,
            "note": "Validate and fix YAML syntax in the referenced workflow file."
        }]

    elif classification == "MISSING_FILE":
        return [{
            "file": "MISSING_FILE_PLACEHOLDER",
            "action": "create_file",
            "diff": None,
            "note": "Identify the missing file path from analysis logs and create it with appropriate content."
        }]

    elif classification == "FILE_SCOPE_FAILURE":
        return [{
            "file": "docs/chantiers/<GO_ID>/FILE_SCOPE.txt",
            "action": "update_file_scope",
            "diff": None,
            "note": "Add or remove paths in FILE_SCOPE.txt to match the changed files in this PR."
        }]

    elif classification == "NO_LOCK_OVERLAP_FAILURE":
        return [{
            "file": "docs/chantiers/<GO_ID>/FILE_SCOPE.txt",
            "action": "resolve_scope_overlap",
            "diff": None,
            "note": "Remove overlapping paths claimed by other GOs. Coordinate with affected GO owners."
        }]

    elif classification == "TIMEOUT":
        return [{
            "file": ".github/workflows/",
            "action": "increase_timeout",
            "diff": None,
            "note": "Increase `timeout-minutes` in the workflow job definition."
        }]

    return []

def draft_patch(analysis: Dict[str, Any]) -> Dict[str, Any]:
    classification = analysis.get("primary_classification", "UNKNOWN_FAILURE")
    cls_info = CLASSIFICATIONS_PATCHABLE.get(classification, CLASSIFICATIONS_PATCHABLE["UNKNOWN_FAILURE"])

    patches = _draft_patches(classification, analysis) if cls_info["patchable"] else []

    return {
        "classification": classification,
        "patchable": cls_info["patchable"],
        "description": cls_info["description"],
        "patches": patches,
        "patch_count": len(patches),
        "dangerous_action_executed": False,
        "human_review_required": True,
        "note": "This patch draft requires human validation before any application."
    }

def main():
    parser = argparse.ArgumentParser(description="OpenClaw GitHub Actions Failure Patch Drafter")
    parser.add_argument("--analysis", type=str, help="Path to analysis JSON file")
    parser.add_argument("--simulate", type=str, choices=list(CLASSIFICATIONS_PATCHABLE.keys()), help="Simulate a specific failure classification")
    parser.add_argument("--test", action="store_true", help="Run self-tests")
    parser.add_argument("--output", type=str, help="Path to write patch draft JSON")

    args = parser.parse_args()

    if args.test:
        print("Running patch draft tests...")
        test_cases = list(CLASSIFICATIONS_PATCHABLE.keys())
        all_pass = True
        for cls in test_cases:
            analysis = {"primary_classification": cls, "details": [{"job_name": "test_job"}]}
            result = draft_patch(analysis)
            expected_patchable = CLASSIFICATIONS_PATCHABLE[cls]["patchable"]
            ok = (
                result["classification"] == cls
                and result["patchable"] == expected_patchable
                and result["dangerous_action_executed"] == False
                and result["human_review_required"] == True
            )
            if ok:
                print(f"  PASS: {cls:35s} patchable={result['patchable']} patches={result['patch_count']}")
            else:
                print(f"  FAIL: {cls:35s} expected patchable={expected_patchable} got patchable={result['patchable']}")
                all_pass = False

        if not all_pass:
            sys.exit(1)
        print("All tests passed.")
        return

    if args.simulate:
        analysis = {"primary_classification": args.simulate, "details": [{"job_name": "simulated_job"}]}
        result = draft_patch(analysis)
    elif args.analysis:
        with open(args.analysis) as f:
            analysis = json.load(f)
        result = draft_patch(analysis)
    else:
        parser.print_help()
        sys.exit(1)

    output = json.dumps(result, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(f"Patch draft written to {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
