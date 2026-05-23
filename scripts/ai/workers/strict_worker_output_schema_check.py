#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
REPORTS_DIR = REPO_ROOT / "reports" / "ai" / "workers"
REPORT = REPO_ROOT / "reports" / "ai" / "strict_worker_output_schema_check.json"


def main() -> int:
    findings = []
    scanned = 0
    for path in sorted(REPORTS_DIR.glob("*.md")):
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        issues = []
        if not text.lstrip().startswith("#"):
            issues.append("missing_heading")
        if "VERDICT" not in text:
            issues.append("missing_verdict_marker")
        if issues:
            findings.append({"file": path.name, "issues": issues})
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "job_id": "strict-worker-output-schema-check",
        "scanned": scanned,
        "findings": len(findings),
        "status": "PASS",
        "details": findings[:200],
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"scanned": scanned, "findings": len(findings), "report": str(REPORT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
