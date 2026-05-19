#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GATEWAY_HEALTH_URL="http://127.0.0.1:18789/health"

pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*" >&2; exit 1; }

echo "MODULE=openclaw_operator_bridge"
echo "SANITY_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Check Python available
python3 --version >/dev/null 2>&1 || fail "python3 not found"
pass "python3 available"

# Check openclaw CLI in PATH
command -v openclaw >/dev/null 2>&1 || fail "openclaw not in PATH"
pass "openclaw CLI found: $(command -v openclaw)"

# Check gateway reachable
response=$(curl -sf --max-time 5 "$GATEWAY_HEALTH_URL" 2>/dev/null) || fail "gateway unreachable at $GATEWAY_HEALTH_URL"
echo "$response" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d.get('ok') is True" 2>/dev/null \
  || fail "gateway health response invalid: $response"
pass "gateway reachable: $response"

# Check module structure
for f in app/bridge.py app/client.py app/schema.py app/__init__.py; do
  [ -f "$BASE/$f" ] || fail "missing: $f"
done
pass "module structure complete"

# Check tests present
[ -f "$BASE/tests/test_bridge_mock.py" ] || fail "missing: tests/test_bridge_mock.py"
pass "tests present"

# Run mock tests
cd "$BASE"
python3 -m unittest tests.test_bridge_mock -v 2>&1 | tail -5
python3 -m unittest tests.test_bridge_mock 2>/dev/null || fail "mock tests FAIL"
pass "mock tests PASS"

echo ""
echo "SANITY=PASS"
echo "SANITY_END=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
