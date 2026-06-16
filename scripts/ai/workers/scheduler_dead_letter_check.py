#!/usr/bin/env python3
"""Scan scheduler/ops logs for recent failure signatures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LOG_PATHS = [
    REPO_ROOT / "logs" / "ops" / "cron.log",
    REPO_ROOT / "logs" / "ops" / "gates_cron.log",
    REPO_ROOT / "logs" / "ops" / "ops_pipeline.log",
    REPO_ROOT / "logs" / "ops" / "pipeline.log",
    REPO_ROOT / "data" / "logs" / "scheduler" / "scheduler.log",
]
KEYWORDS = ("ERROR", "FAIL", "BLOCKED", "Traceback", "TimeoutExpired", "CRITICAL_DOWN")
TAIL_LINES = 200


def scan_log(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []
    findings = []
    for idx, line in enumerate(lines[-TAIL_LINES:], start=max(len(lines) - TAIL_LINES + 1, 1)):
        if any(token in line for token in KEYWORDS):
            findings.append({
                "line": idx,
                "text": line[:220],
            })
    return findings


def main() -> int:
    reports = []
    total = 0
    for path in LOG_PATHS:
        findings = scan_log(path)
        total += len(findings)
        reports.append({
            "path": str(path.relative_to(REPO_ROOT)),
            "exists": path.exists(),
            "findings": findings,
        })

    payload = {
        "status": "PASS" if total == 0 else "FAIL",
        "finding_count": total,
        "logs": reports,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
