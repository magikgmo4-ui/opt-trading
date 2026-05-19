#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*" >&2; exit 1; }

echo "MODULE=notification_dispatcher"
echo "SANITY_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

python3 --version >/dev/null 2>&1 || fail "python3 not found"
pass "python3 available"

python3 -c "import requests" 2>/dev/null || fail "requests not installed"
pass "requests available"

for f in app/dispatcher.py app/events.py app/__init__.py; do
  [ -f "$BASE/$f" ] || fail "missing: $f"
done
pass "module structure complete"

cd "$BASE"
python3 -m unittest tests.test_dispatcher 2>/dev/null || fail "unit tests FAIL"
pass "unit tests PASS (11 tests)"

# Dry-run smoke — no Telegram required
result=$(python3 -m app signal_received --dry-run ticker=BTCUSDT side=BUY price=65000 tf=1h strategy_id=smoke)
echo "$result" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok'] is True" \
  || fail "dry-run smoke FAIL"
pass "dry-run smoke PASS"

echo ""
echo "SANITY=PASS"
echo "SANITY_END=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
