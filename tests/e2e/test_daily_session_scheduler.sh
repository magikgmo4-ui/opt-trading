#!/usr/bin/env bash
set -euo pipefail
# Tests pour le Daily Session Scheduler
# Usage: bash tests/e2e/test_daily_session_scheduler.sh [--verbose]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCHEDULER_SCRIPT="$ROOT_DIR/scripts/schedule/daily_session.sh"
SCHEDULER_LOG_DIR="$ROOT_DIR/data/logs/scheduler"
PASS=0
FAIL=0
VERBOSE=false

if [ "${1:-}" = "--verbose" ]; then
    VERBOSE=true
fi

test() {
    local name="$1"
    shift
    local desc="$1"
    shift

    echo "---"
    echo "TEST: $name"
    echo "  $desc"

    if "$@"; then
        PASS=$((PASS + 1))
        echo "  PASS"
    else
        FAIL=$((FAIL + 1))
        echo "  FAIL"
    fi
}

cleanup() {
    rm -f "$SCHEDULER_LOG_DIR/scheduler.log" "$SCHEDULER_LOG_DIR/scheduler.log.bak"
}
cleanup

# ── Test 1: Script exists and is executable ──────────────────────────
test "scheduler_script_exists" "Scheduler script exists and is executable" \
    test -x "$SCHEDULER_SCRIPT"

# ── Test 2: Script has no live trade references ──────────────────────
test "scheduler_no_live_trade" "Scheduler script has no live trade or Bitget calls (invariant declarations are OK)" \
    bash -c "! grep -qi 'bitget_bridge\|live_order\|\.execute(' '$SCHEDULER_SCRIPT' && \
             grep -q 'NO_LIVE_TRADE' '$SCHEDULER_SCRIPT'"

# ── Test 3: Script has no POST/PUT/DELETE/PATCH ──────────────────────
test "scheduler_no_http_mutations" "Scheduler script has no HTTP mutation calls" \
    bash -c "! grep -qiE '\.post\(|\.put\(|\.delete\(|\.patch\(' '$SCHEDULER_SCRIPT'"

# ── Test 4: Script has invariants declared ──────────────────────────
test "scheduler_has_invariants" "Scheduler script declares invariants" \
    bash -c "grep -q 'DRY_RUN_DEFAULT' '$SCHEDULER_SCRIPT' && \
             grep -q 'NO_AUTOMATIC_SHEETS_WRITE' '$SCHEDULER_SCRIPT' && \
             grep -q 'NO_LIVE_TRADE' '$SCHEDULER_SCRIPT' && \
             grep -q 'NO_BITGET_ORDER' '$SCHEDULER_SCRIPT' && \
             grep -q 'LOCALCMS_READ_ONLY' '$SCHEDULER_SCRIPT'"

# ── Test 5: Script calls daily_session_journal.py ────────────────────
test "scheduler_calls_journal" "Scheduler script references daily_session_journal.py" \
    bash -c "grep -q 'daily_session_journal.py' '$SCHEDULER_SCRIPT'"

# ── Test 6: Script calls sync_daily_session.py ──────────────────────
test "scheduler_calls_sync" "Scheduler script references sync_daily_session.py" \
    bash -c "grep -q 'sync_daily_session.py' '$SCHEDULER_SCRIPT'"

# ── Test 7: Script creates log directory ─────────────────────────────
test "scheduler_creates_log_dir" "Scheduler script defines and creates data/logs/scheduler" \
    bash -c "grep -q 'SCHEDULER_LOG_DIR=.*scheduler' '$SCHEDULER_SCRIPT' && \
             grep -q 'mkdir.*SCHEDULER_LOG_DIR' '$SCHEDULER_SCRIPT'"

# ── Test 8: Script has precheck TMUX ──────────────────────────────
test "scheduler_precheck_tmux" "Scheduler script has TMUX precheck" \
    bash -c "grep -q 'precheck TMUX' '$SCHEDULER_SCRIPT'"

# ── Test 9: Script has precheck LocalCMS ──────────────────────────
test "scheduler_precheck_localcms" "Scheduler script has LocalCMS precheck" \
    bash -c "grep -q 'precheck LocalCMS' '$SCHEDULER_SCRIPT'"

# ── Test 10: Default mode is dry-run ──────────────────────────────
test "scheduler_dry_run_default" "Controlled-write is false by default" \
    bash -c "grep -q 'CONTROLLED_WRITE_SHEETS=false' '$SCHEDULER_SCRIPT'"

# ── Test 11: Script logs scheduler.log ──────────────────────────
test "scheduler_logs_to_file" "Scheduler script writes to scheduler.log" \
    bash -c "grep -q 'scheduler.log' '$SCHEDULER_SCRIPT'"

# ── Test 12: Script can run dry (will pass or fail gracefully) ───────
echo "---"
echo "TEST: scheduler_dry_run_execution"
echo "  Scheduler dry-run execution (no LocalCMS, but should not crash)"

DRY_RUN=1 PAPER_MODE=1 bash "$SCHEDULER_SCRIPT" 2>&1 || true
if [ -f "$SCHEDULER_LOG_DIR/scheduler.log" ]; then
    PASS=$((PASS + 1))
    echo "  PASS (log created)"
    if $VERBOSE; then
        echo "  --- scheduler.log ---"
        cat "$SCHEDULER_LOG_DIR/scheduler.log"
        echo "  --- end ---"
    fi
else
    FAIL=$((FAIL + 1))
    echo "  FAIL (no log created)"
fi

# ── Test 13: Log contains expected sections ─────────────────────────
echo "---"
echo "TEST: scheduler_log_content"
echo "  Log contains expected sections"

if [ -f "$SCHEDULER_LOG_DIR/scheduler.log" ]; then
    LOG_CONTENT=$(cat "$SCHEDULER_LOG_DIR/scheduler.log")
    if echo "$LOG_CONTENT" | grep -q "precheck TMUX" && \
       echo "$LOG_CONTENT" | grep -q "precheck LocalCMS" && \
       echo "$LOG_CONTENT" | grep -q "daily_session_journal.py"; then
        PASS=$((PASS + 1))
        echo "  PASS"
    else
        FAIL=$((FAIL + 1))
        echo "  FAIL (missing expected sections)"
    fi
else
    FAIL=$((FAIL + 1))
    echo "  FAIL (no log)"
fi

# ── Results ──────────────────────────────────────────────────────────
cleanup
echo ""
echo "=============================="
echo "Results: $PASS passed, $FAIL failed"
echo "=============================="
[ "$FAIL" -eq 0 ]
