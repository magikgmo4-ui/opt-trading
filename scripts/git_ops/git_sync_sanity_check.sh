#!/usr/bin/env bash
set -euo pipefail
# Git Sync Sanity Check (Linux)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Checking Git Ops Environment..."

# 1. Git
if command -v git &> /dev/null; then
    echo "PASS: Git found"
else
    echo "FAIL: Git missing"
    exit 1
fi

# 2. Repo
if [ -d "$ROOT_DIR/.git" ]; then
    echo "PASS: Git repository detected"
else
    echo "FAIL: Not a git repository"
    exit 1
fi

# 3. Scripts
if [ -f "$SCRIPT_DIR/git_pull_update_linux.sh" ]; then
    echo "PASS: Git Ops scripts present"
else
    echo "FAIL: Git Ops scripts missing"
    exit 1
fi

# 4. Status
if git status --porcelain >/dev/null 2>&1; then
    echo "PASS: Working tree status checkable"
else
    echo "WARN: Cannot check git status"
fi

echo "Git Sync Sanity Check Passed."
