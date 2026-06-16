#!/usr/bin/env python3
"""Scan tracked files for obvious secret leaks.

Conservative detector for local ops usage and CI.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MAX_BYTES = 512_000
TEXT_EXTS = {".py", ".json", ".yml", ".yaml", ".sh", ".env", ".txt", ".ini", ".cfg"}
ALLOWED_ROOTS = {
    "scripts",
    "modules",
    ".github",
    "schemas",
}
IGNORED_PARTS = {
    "docs",
    "reports",
    "bundles",
    ".bundle_reviews",
    "tools",
    "venv",
    ".venv",
    "tmp",
    "logs",
    "data",
    "fixtures",
    "tests",
}
CONTENT_PATTERNS = [
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("bearer_token_literal", re.compile(r"Authorization:\s*Bearer\s+(?!\$\{?)(?!\$?[A-Z_]+\b)\S+", re.IGNORECASE)),
    ("literal_secret_assign", re.compile(r"\b[A-Z0-9_]*(API_KEY|TOKEN|SECRET|PASSWORD)\b\s*[:=]\s*['\"](?!REPLACE_ME|xxx|yyy|\.\.\.)[^'\"]{8,}['\"]", re.IGNORECASE)),
    ("private_key_block", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
]


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO_ROOT / line for line in result.stdout.splitlines() if line.strip()]


def is_text_candidate(path: Path) -> bool:
    rel_parts = path.relative_to(REPO_ROOT).parts
    if not rel_parts or rel_parts[0] not in ALLOWED_ROOTS:
        return False
    if any(part in IGNORED_PARTS for part in rel_parts):
        return False
    if path.suffix.lower() in TEXT_EXTS:
        return True
    return path.name.startswith(".env")


def scan_file(path: Path) -> list[dict]:
    try:
        if path.stat().st_size > MAX_BYTES or not is_text_candidate(path):
            return []
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    findings = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if "$(" in line:
            continue
        for kind, pattern in CONTENT_PATTERNS:
            if pattern.search(line):
                findings.append({
                    "path": str(path.relative_to(REPO_ROOT)),
                    "line": lineno,
                    "kind": kind,
                    "preview": line[:160],
                })
    return findings


def main() -> int:
    findings = []
    files = tracked_files()
    for path in files:
        findings.extend(scan_file(path))

    report = {
        "repo_root": str(REPO_ROOT),
        "tracked_files": len(files),
        "findings": findings,
        "finding_count": len(findings),
        "status": "PASS" if not findings else "FAIL",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
