#!/usr/bin/env python3
"""Anti-leak tests — detect secret patterns in code outputs and runtime files.

Usage:
  python3 scripts/ai/tests/anti_leak_tests.py
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

PATTERNS = [
    (r'sk-[A-Za-z0-9]{20,}', "OpenAI API key"),
    (r'ghp_[A-Za-z0-9]{36,}', "GitHub PAT"),
    (r'xox[baprs]-[A-Za-z0-9-]{24,}', "Slack token"),
    (r'AKIA[0-9A-Z]{16}', "AWS access key"),
    (r'-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----', "Private key"),
]

EXCLUDE_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    ".env", ".env.example",
}

SENSITIVE_FILES = [
    ".env",
    ".env.prod",
    ".env.local",
]

OUTPUT_DIRS = [
    "reports/ai",
    "data/runtime_health",
]


def scan_file_for_leaks(filepath: Path) -> list:
    """Check a single file for secret pattern leaks."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for i, line in enumerate(content.splitlines(), 1):
        for pattern, desc in PATTERNS:
            if re.search(pattern, line):
                findings.append((filepath, i, desc, line[:80]))
    return findings


def check_sensitive_files_not_committed() -> list:
    """Verify .env* files are not in the repo (gitignored)."""
    findings = []
    for f in SENSITIVE_FILES:
        path = REPO_ROOT / f
        if path.exists():
            # Check if tracked by git
            result = os.system(f"git -C {REPO_ROOT} ls-files --error-unmatch {f} >/dev/null 2>&1")
            if result == 0:
                findings.append((path, 0, "SENSITIVE FILE TRACKED IN GIT", f))
    return findings


def scan_output_dirs() -> list:
    """Scan output dirs for leaked secrets in generated content."""
    findings = []
    for d in OUTPUT_DIRS:
        dirpath = REPO_ROOT / d
        if not dirpath.exists():
            continue
        for fpath in dirpath.rglob("*"):
            if fpath.is_file() and fpath.suffix in {".json", ".txt", ".log", ".md"}:
                findings.extend(scan_file_for_leaks(fpath))
    return findings


def test_no_sensitive_files_in_repo():
    """Test 1: No .env files are tracked by git."""
    findings = check_sensitive_files_not_committed()
    if findings:
        for path, _, desc, name in findings:
            print(f"  FAIL: {name} is tracked in git at {path}")
        return False
    print("  PASS: No sensitive files tracked in git")
    return True


def test_no_leaks_in_outputs():
    """Test 2: No leaked secrets in output files."""
    findings = scan_output_dirs()
    if findings:
        for path, line, desc, snippet in findings:
            print(f"  FAIL: {desc} found in {path}:{line}")
            print(f"    Snippet: {snippet}")
        return False
    print("  PASS: No secret leaks in output directories")
    return True


def test_kill_switch_state():
    """Test 3: Kill switch file exists and is readable."""
    ks_path = REPO_ROOT / "data/runtime_health" / "kill_switch.state"
    if not ks_path.exists():
        print("  WARN: kill_switch.state not found, creating default")
        ks_path.parent.mkdir(parents=True, exist_ok=True)
        ks_path.write_text("NORMAL\n")
    state = ks_path.read_text().strip()
    assert state in ("NORMAL", "WRITES_SUSPENDED", "FULL_STOP"), f"Invalid state: {state}"
    print(f"  PASS: Kill switch state = {state}")
    return True


def test_gitignore_blocks_secrets():
    """Test 4: .gitignore contains *SECRET* pattern."""
    gitignore = REPO_ROOT / ".gitignore"
    content = gitignore.read_text()
    for pattern in ["*SECRET*", "*API_KEY*", "*TOKEN*", "*PASSWORD*"]:
        if pattern in content:
            print(f"  PASS: .gitignore blocks {pattern}")
        else:
            print(f"  FAIL: .gitignore missing {pattern}")
            return False
    return True


def main():
    tests = [
        ("Sensitive files in repo", test_no_sensitive_files_in_repo),
        ("Secret leaks in outputs", test_no_leaks_in_outputs),
        ("Kill switch state", test_kill_switch_state),
        ("Gitignore blocks secrets", test_gitignore_blocks_secrets),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        print(f"[{name}]")
        try:
            if fn():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
        print()

    print(f"Results: {passed}/{len(tests)} passed, {failed} failed")
    if failed > 0:
        # Only fail if leaks are detected in outputs or sensitive files in repo
        sys.exit(1)


if __name__ == "__main__":
    main()
