#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$BASE/../.." && pwd)"

fail() {
  echo "SANITY FAIL: $1"
  exit 1
}

command -v git >/dev/null 2>&1 || fail "git not found"
command -v python3 >/dev/null 2>&1 || fail "python3 not found"
git -C "$REPO_ROOT" rev-parse --show-toplevel >/dev/null 2>&1 || fail "not inside git repo"
[ -f "$REPO_ROOT/modules/memory_bricks/tests/test_api_v2_http.py" ] || fail "memory_bricks HTTP tests file missing"
[ -f "$REPO_ROOT/modules/trading_lab_v1/scripts/cmd.sh" ] || fail "trading_lab_v1 cmd.sh missing"

echo "SANITY PASS: dev_validation_hub"
echo "REPO_ROOT=$REPO_ROOT"
echo "PYTHON3=$(command -v python3)"
echo "BRANCH=$(git -C "$REPO_ROOT" branch --show-current)"
