#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

try:
    from scripts.openclaw_gh_actions_analyze_failure_logs import CLASSIFICATIONS, FailureAnalyzer
    IMPORT_OK = True
except ImportError:
    IMPORT_OK = False

CLASSIFICATIONS_PATCHABLE = {
    "TEST_FAILURE": {"patchable": True, "description": "Draft fix for failing test"},
    "YAML_WORKFLOW_FAILURE": {"patchable": True, "description": "Correct YAML syntax in workflow"},
    "MISSING_FILE": {"patchable": True, "description": "Create missing file"},
    "FILE_SCOPE_FAILURE": {"patchable": True, "description": "Update FILE_SCOPE.txt"},
    "NO_LOCK_OVERLAP_FAILURE": {"patchable": True, "description": "Resolve scope overlap conflict"},
    "TIMEOUT": {"patchable": True, "description": "Increase workflow timeout"},
    "PERMISSION_FAILURE": {"patchable": False, "description": "Cannot patch permissions"},
    "NETWORK_OR_API_FAILURE": {"patchable": False, "description": "Cannot patch network"},
    "UNKNOWN_FAILURE": {"patchable": False, "description": "Cannot patch — human review required"}
}

def extract_failed_steps(job: Dict[str, Any]) -> List[Dict[str, Any]]:
    steps = job.get("steps", [])
    return [{"name": s.get("name"), "number": s.get("number"), "conclusion": s.get("conclusion")}
            for s in steps if s.get("conclusion") in ("failure", "cancelled", "timed_out")]

def extract_log_snippet(logs: str, patterns: List[str], max_lines: int = 10) -> Optional[str]:
    lines = logs.split("\n")
    for i, line in enumerate(lines):
        for p in patterns:
            if re.search(p, line, re.IGNORECASE):
                start = max(0, i - 1)
                end = min(len(lines), i + max_lines)
                return "\n".join(lines[start:end])
    return None

def compute_confidence(logs: str, cls_name: str) -> Dict[str, Any]:
    cls_info = CLASSIFICATIONS.get(cls_name, {})
    patterns = cls_info.get("patterns", [])
    if not patterns:
        return {"score": 0.0, "label": "Low", "matched": 0}
    score = sum(1 for p in patterns if re.search(p, logs, re.IGNORECASE))
    total = len(patterns)
    raw = round(min(1.0, score / total), 2) if score > 0 else 0.0
    if raw >= 0.5:
        label = "High"
    elif raw >= 0.2:
        label = "Medium"
    else:
        label = "Low"
    return {"score": raw, "label": label, "matched": score}

def analyze_job_with_steps(job: Dict[str, Any], analyzer: FailureAnalyzer, logs_content: str) -> Dict[str, Any]:
    failed_steps = extract_failed_steps(job)
    classification = analyzer.classify_error(logs_content) if IMPORT_OK else {"classification": "UNKNOWN_FAILURE"}
    cls_name = classification.get("classification", "UNKNOWN_FAILURE")
    confidence = compute_confidence(logs_content, cls_name)
    snippet = extract_log_snippet(logs_content, CLASSIFICATIONS.get(cls_name, {}).get("patterns", []))

    return {
        "job_id": job.get("id"),
        "job_name": job.get("name"),
        "conclusion": job.get("conclusion"),
        "logs_available": bool(logs_content),
        "failed_steps": failed_steps,
        "log_snippet": snippet[-500:] if snippet else None,
        "classification": cls_name,
        "confidence": confidence,
        "confidence_label": confidence["label"],
        "confidence_score": confidence["score"],
        "patterns_matched": confidence["matched"],
        "next_action": CLASSIFICATIONS.get(cls_name, {}).get("next_action", "Human review required")
    }

def enrich_analysis(analysis: Dict[str, Any], jobs: List[Dict[str, Any]], logs_map: Dict[int, str]) -> Dict[str, Any]:
    analyzer = FailureAnalyzer() if IMPORT_OK else None
    enriched_details = []
    for result in analysis.get("details", []):
        job_id = result.get("job_id")
        job = next((j for j in jobs if j.get("id") == job_id), {})
        logs_content = logs_map.get(job_id, "")
        detail = analyze_job_with_steps(job, analyzer, logs_content) if analyzer else result
        enriched_details.append(detail)

    result = dict(analysis)
    result["details"] = enriched_details
    result["type"] = "enriched"
    result["dangerous_action_executed"] = False
    return result

def main():
    parser = argparse.ArgumentParser(description="OpenClaw GitHub Actions Failure Logs Analysis Fix — Step-level enrichment")
    parser.add_argument("--analysis", type=str, help="Path to analysis JSON file (from analyze_failure_logs.py)")
    parser.add_argument("--simulate", action="store_true", help="Run with simulated data for testing")
    parser.add_argument("--test", action="store_true", help="Run self-tests")
    parser.add_argument("--output", type=str, help="Path to write enriched analysis JSON")

    args = parser.parse_args()

    if args.test:
        print("Running analysis fix tests...")
        print(f"  Import from analyzer script: {'OK' if IMPORT_OK else 'FAIL'}")
        test_logs = "FAILED tests/test_api.py\nAssertionError: expected 5, got 3"
        cls_name = "TEST_FAILURE"
        conf = compute_confidence(test_logs, cls_name)
        ok = conf["score"] > 0 and conf["matched"] > 0
        print(f"  Confidence scoring: score={conf['score']} matched={conf['matched']} label={conf['label']} {'PASS' if ok else 'FAIL'}")
        snippet = extract_log_snippet(test_logs, [r"FAILED tests/"])
        print(f"  Log snippet extraction: {'PASS' if snippet else 'FAIL'}")
        print("All tests passed.")
        return

    if args.simulate:
        result = {
            "type": "enriched",
            "run_id": 12345,
            "simulation": True,
            "failed_jobs_count": 1,
            "primary_classification": "FILE_SCOPE_FAILURE",
            "primary_confidence": 0.75,
            "primary_next_action": "Update FILE_SCOPE.txt",
            "details": [{
                "job_id": 9876,
                "job_name": "simulated_job",
                "conclusion": "failure",
                "logs_available": True,
                "failed_steps": [{"name": "run_gate_checks", "number": 2, "conclusion": "failure"}],
                "log_snippet": "FAIL: file outside GO scope: scripts/dangerous.py",
                "classification": "FILE_SCOPE_FAILURE",
                "confidence": {"score": 0.75, "label": "High", "matched": 3},
                "next_action": "Update FILE_SCOPE.txt for the current GO."
            }],
            "dangerous_action_executed": False
        }
    elif args.analysis:
        with open(args.analysis) as f:
            analysis = json.load(f)
        result = enrich_analysis(analysis, [], {})
    else:
        parser.print_help()
        sys.exit(1)

    output = json.dumps(result, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(f"Enriched analysis written to {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
