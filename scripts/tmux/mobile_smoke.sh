#!/usr/bin/env bash
# Mobile operator smoke test — CI-safe simulation
# Validates attach-hints, health-aggregate, and session definitions
# Does NOT require a physical device, active SSH, or tmux running
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

PASS=0
FAIL=0

ok()   { echo "  OK  $*"; ((PASS++)) || true; }
fail() { echo "  FAIL $*" >&2; ((FAIL++)) || true; }

# Mobile-relevant host:session pairs
MOBILE_TARGETS=(
    "db-layer:openclaw-core"
    "db-layer:fleet-status"
    "admin-trading:desk-pro"
    "admin-trading:screeners"
)

echo "=== Mobile Operator Smoke Test ==="

# ── Test 1: attach-hint produces correct SSH + tmux lines ─────────────────
echo "--- T1: attach-hint validation ---"
for pair in "${MOBILE_TARGETS[@]}"; do
    host="${pair%%:*}"
    session="${pair##*:}"
    output=$(bash modules/openclaw_tmux_operator/scripts/cmd.sh attach-hint "$host" "$session" 2>&1)
    if echo "$output" | grep -q "ssh $host" && echo "$output" | grep -q "tmux attach -t $session"; then
        ok "attach-hint $host:$session"
    else
        fail "attach-hint $host:$session — got: $output"
    fi
done

# ── Test 2: health-aggregate --dry-run (fleet status readable from mobile) ─
echo "--- T2: health-aggregate dry-run ---"
if health_json=$(bash modules/openclaw_tmux_operator/scripts/cmd.sh health-aggregate --dry-run 2>&1); then
    if echo "$health_json" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert 'machines' in d, 'missing machines key'
assert isinstance(d['total'], int) and d['total'] > 0, 'total must be > 0'
assert 'timestamp' in d, 'missing timestamp'
"; then
        ok "health-aggregate --dry-run JSON valid (total=$(echo "$health_json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["total"])'))"
    else
        fail "health-aggregate --dry-run JSON structure invalid"
    fi
else
    fail "health-aggregate --dry-run exited non-zero"
fi

# ── Test 3: mobile target sessions are in ALL_SESSIONS ───────────────────
echo "--- T3: mobile sessions in ALL_SESSIONS ---"
result=$(python3 - <<'PYEOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))
from scripts.tmux.health_check import ALL_SESSIONS

mobile_sessions = {"openclaw-core", "fleet-status", "desk-pro", "screeners"}
missing = mobile_sessions - ALL_SESSIONS
if missing:
    print("MISSING:" + ",".join(sorted(missing)))
    sys.exit(1)
else:
    print("OK:" + str(len(mobile_sessions)))
    sys.exit(0)
PYEOF
)
if [[ "$result" == OK:* ]]; then
    ok "mobile sessions in ALL_SESSIONS (${result#OK:} sessions)"
else
    fail "sessions not in ALL_SESSIONS: ${result#MISSING:}"
fi

# ── Test 4: cmd.sh usage lists mobile-relevant commands ──────────────────
echo "--- T4: cmd.sh usage completeness ---"
usage=$(bash modules/openclaw_tmux_operator/scripts/cmd.sh 2>&1 || true)
for cmd in "attach-hint" "health-aggregate" "session-logs" "tmux-status" "machine-status"; do
    if echo "$usage" | grep -q "$cmd"; then
        ok "cmd.sh usage contains $cmd"
    else
        fail "cmd.sh usage missing $cmd"
    fi
done

# ── Test 5: mobile runbook doc exists and has key sections ───────────────
echo "--- T5: mobile runbook doc ---"
runbook="docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/40_MOBILE_OPERATOR_ACCESS.md"
if [ -f "$runbook" ]; then
    ok "mobile runbook doc exists"
    for keyword in "Termius" "Termux" "tmux attach" "Interdits mobile"; do
        if grep -q "$keyword" "$runbook"; then
            ok "runbook contains: $keyword"
        else
            fail "runbook missing: $keyword"
        fi
    done
else
    fail "mobile runbook doc missing: $runbook"
fi

# ── Summary ──────────────────────────────────────────────────────────────
echo ""
total=$((PASS + FAIL))
echo "=== Mobile Smoke: $PASS/$total PASS ==="

if [ "$FAIL" -gt 0 ]; then
    echo "FAIL: $FAIL test(s) failed" >&2
    exit 1
fi
