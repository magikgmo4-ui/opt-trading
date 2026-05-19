#!/usr/bin/env bash
# SSH connectivity matrix test — validates all-to-all SSH reachability
# Run from db-layer (has access to all machines)
# READ_ONLY: only tests connectivity, no modifications
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

PASS=0
FAIL=0

ok()   { echo "  OK  $*"; ((PASS++)) || true; }
fail() { echo "  FAIL $*" >&2; ((FAIL++)) || true; }

LINUX_MACHINES=(db-layer admin-trading fantome student)
ALL_MACHINES=(db-layer admin-trading fantome student cursor-ai)

echo "=== SSH Fleet Matrix Test (from $(hostname)) ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# ── From db-layer (local) → all ───────────────────────────────────────────
echo "--- db-layer → all ---"
for to in admin-trading fantome student cursor-ai; do
    result=$(ssh -o BatchMode=yes -o ConnectTimeout=5 "$to" "hostname" 2>&1)
    rc=$?
    [ $rc -eq 0 ] && ok "db-layer -> $to ($result)" || fail "db-layer -> $to : $result"
done

# ── From admin-trading → others ──────────────────────────────────────────
echo "--- admin-trading → others ---"
for to in db-layer fantome student cursor-ai; do
    result=$(ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading \
        "ssh -o BatchMode=yes -o ConnectTimeout=5 $to hostname 2>&1")
    rc=$?
    [ $rc -eq 0 ] && ok "admin-trading -> $to ($result)" || fail "admin-trading -> $to : $result"
done

# ── From fantome → others ─────────────────────────────────────────────────
echo "--- fantome → others ---"
for to in db-layer admin-trading student cursor-ai; do
    result=$(ssh -o BatchMode=yes -o ConnectTimeout=5 fantome \
        "ssh -o BatchMode=yes -o ConnectTimeout=5 $to hostname 2>&1")
    rc=$?
    [ $rc -eq 0 ] && ok "fantome -> $to ($result)" || fail "fantome -> $to : $result"
done

# ── Summary ──────────────────────────────────────────────────────────────
echo ""
total=$((PASS + FAIL))
echo "=== SSH Matrix: $PASS/$total PASS ==="

if [ "$FAIL" -gt 0 ]; then
    echo "FAIL: $FAIL pair(s) unreachable" >&2
    exit 1
fi
