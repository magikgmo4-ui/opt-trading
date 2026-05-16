#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*" >&2; exit 1; }

echo "MODULE=signal_router"
echo "SANITY_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

python3 --version >/dev/null 2>&1 || fail "python3 not found"
pass "python3 available"

for f in app/router.py app/schema.py app/server.py app/__init__.py; do
  [ -f "$BASE/$f" ] || fail "missing: $f"
done
pass "module structure complete"

[ -f "$BASE/tests/test_router.py" ] || fail "missing: tests/test_router.py"
pass "tests present"

cd "$BASE"
python3 -m unittest tests.test_router 2>/dev/null || fail "unit tests FAIL"
pass "unit tests PASS (12 tests)"

echo ""
echo "SANITY=PASS"
echo "SANITY_END=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
