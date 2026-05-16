#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*" >&2; exit 1; }

echo "MODULE=proposition_engine"
echo "SANITY_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

python3 --version >/dev/null 2>&1 || fail "python3 not found"
pass "python3 available"

for f in app/schema.py app/engines.py app/builder_prompt.py app/engine.py app/__init__.py; do
  [ -f "$BASE/$f" ] || fail "missing: $f"
done
pass "module structure complete"

python3 -c "from modules.proposition_engine.app.schema import Proposition" 2>/dev/null \
  || (cd "$BASE" && python3 -c "from app.schema import Proposition") || fail "schema import FAIL"
pass "schema import PASS"

cd "$BASE"
python3 -m unittest tests.test_proposition 2>/dev/null || fail "unit tests FAIL"
pass "unit tests PASS (18 tests)"

result=$(python3 -m app BTCUSDT BUY 65000 1h --dry-run --strategy-id sanity_smoke)
echo "$result" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['dry_run'] is True and d['status']=='ok'" \
  || fail "dry-run smoke FAIL"
pass "dry-run smoke PASS"

echo ""
echo "SANITY=PASS"
echo "SANITY_END=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
