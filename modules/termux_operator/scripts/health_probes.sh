#!/usr/bin/env bash
# health_probes.sh — tmux health probes from Android Termux
# Non-destructive: READ-ONLY. No session creation/deletion.
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." 2>/dev/null && pwd || echo "/opt/trading")"
REMOTE_ROOT="/opt/trading"  # path on fleet machines

MACHINES=("db-layer" "admin-trading" "fantome" "student")
PASS=0
FAIL=0
TIMEOUT=5

ok()   { echo "  OK  $*"; ((PASS++)) || true; }
fail() { echo "  FAIL $*" >&2; ((FAIL++)) || true; }

health_tmux_sessions() {
    local host="$1"
    local output
    output=$(ssh -o BatchMode=yes -o ConnectTimeout="$TIMEOUT" "$host" \
        "tmux list-sessions -F '#{session_name}' 2>/dev/null || echo '__NO_TMUX__'" 2>&1)
    local rc=$?
    if [ $rc -ne 0 ]; then
        fail "$host: SSH unreachable ($output)"
        return 1
    fi
    if echo "$output" | grep -q "__NO_TMUX__"; then
        fail "$host: tmux not running"
        return 1
    fi
    local count
    count=$(echo "$output" | grep -cv "^$" || true)
    ok "$host: $count tmux session(s)"
    echo "$output" | while IFS= read -r s; do
        [ -n "$s" ] && echo "       - $s"
    done
}

health_ssh_connectivity() {
    local host="$1"
    if ssh -o BatchMode=yes -o ConnectTimeout="$TIMEOUT" "$host" 'echo ok' 2>/dev/null | grep -q ok; then
        ok "$host: SSH reachable"
    else
        fail "$host: SSH unreachable"
    fi
}

health_fleet_status() {
    local host="db-layer"
    local output
    output=$(ssh -o BatchMode=yes -o ConnectTimeout="$TIMEOUT" "$host" \
        "cd $REMOTE_ROOT && python3 modules/runtime_health/fleet_orchestrator.py --dry-run 2>/dev/null || echo '__FLEET_UNAVAIL__'" 2>&1)
    local rc=$?
    if [ $rc -ne 0 ] || echo "$output" | grep -q "__FLEET_UNAVAIL__"; then
        fail "db-layer: fleet orchestrator unavailable"
    else
        local status
        status=$(echo "$output" | grep -o '"overall_status": *"[^"]*"' | head -1 | cut -d'"' -f4)
        ok "fleet orchestrator: overall_status=${status:-unknown}"
    fi
}

health_runtime_health() {
    local host="db-layer"
    local output
    output=$(ssh -o BatchMode=yes -o ConnectTimeout="$TIMEOUT" "$host" \
        "cat /opt/trading/data/runtime_health/latest.json 2>/dev/null || echo '__NO_RUNTIME_HEALTH__'" 2>&1)
    if echo "$output" | grep -q "__NO_RUNTIME_HEALTH__"; then
        fail "db-layer: runtime health json unavailable"
    else
        local status
        status=$(echo "$output" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('overall_status','unknown'))" 2>/dev/null || echo "parse_error")
        ok "runtime health: overall_status=${status}"
    fi
}

health_aggregate() {
    local host="db-layer"
    local output
    output=$(ssh -o BatchMode=yes -o ConnectTimeout="$TIMEOUT" "$host" \
        "cd $REMOTE_ROOT && python3 modules/openclaw_tmux_operator/scripts/health_aggregate.py --dry-run 2>/dev/null || echo '__AGG_UNAVAIL__'" 2>&1)
    if echo "$output" | grep -q "__AGG_UNAVAIL__"; then
        fail "db-layer: health aggregate unavailable"
        return 1
    fi
    local total
    total=$(echo "$output" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('total','?'))" 2>/dev/null || echo "?")
    ok "health aggregate: $total machine(s) in scope"
}

health_attachment_hints() {
    local output
    output=$(bash "$PROJECT_ROOT/modules/openclaw_tmux_operator/scripts/cmd.sh" attach-hint db-layer openclaw-core 2>&1 || true)
    if echo "$output" | grep -q "ssh db-layer" && echo "$output" | grep -q "tmux attach -t openclaw-core"; then
        ok "attach-hint: db-layer:openclaw-core"
    else
        fail "attach-hint: db-layer:openclaw-core — got: $output"
    fi
}

stats() {
    local total=$((PASS + FAIL))
    echo ""
    echo "=== Health Probes: $PASS/$total PASS ==="
    [ "$FAIL" -gt 0 ] && echo "FAIL: $FAIL probe(s) failed" >&2
    return "$FAIL"
}

# ── main ────────────────────────────────────────────────────────────────────

echo "=== Termux Health Probes ==="
echo ""

echo "--- SSH Connectivity ---"
for m in "${MACHINES[@]}"; do
    health_ssh_connectivity "$m"
done

echo ""
echo "--- tmux Sessions ---"
for m in "${MACHINES[@]}"; do
    health_tmux_sessions "$m"
done

echo ""
echo "--- Fleet ---"
health_fleet_status

echo ""
echo "--- Runtime Health ---"
health_runtime_health

echo ""
echo "--- Aggregate ---"
health_aggregate

echo ""
echo "--- Attachment Hints ---"
health_attachment_hints

stats
