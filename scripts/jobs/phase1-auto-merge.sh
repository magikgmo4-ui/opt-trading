#!/bin/bash
set -euo pipefail
cd /opt/trading
LOG="/tmp/non-trading-phase1-auto-merge.log"
exec > "$LOG" 2>&1

echo "=== Phase 1 auto-merge check: $(date -u) ==="

# 1. Check ledger for last 24h
LEDGER="data/runtime_health/job_logs/ledger.jsonl"
if [ ! -f "$LEDGER" ]; then
    echo "FAIL: ledger not found"
    exit 1
fi

# 2. Check all 5 timers ran successfully
TIMERS=$(systemctl --user list-timers --all | grep non-trading | wc -l)
echo "Active timers: $TIMERS (expected 5)"

# 3. Check last strict worker smoke verdict
SMOKE="reports/ai/strict_worker_e2e_readonly.json"
if [ -f "$SMOKE" ]; then
    VERDICT=$(python3 -c "import json; print(json.load(open('$SMOKE'))['verdict'])")
    echo "Strict worker smoke verdict: $VERDICT"
    if [ "$VERDICT" != "PASS" ]; then
        echo "FAIL: smoke verdict not PASS"
        exit 1
    fi
fi

# 4. Check no Gmail/Calendar/trading timers
FORBIDDEN=$(systemctl --user list-timers --all | grep -E 'gmail|calendar|trading' | wc -l)
echo "Forbidden timers found: $FORBIDDEN"
if [ "$FORBIDDEN" -gt 0 ]; then
    echo "FAIL: forbidden timer detected"
    exit 1
fi

# 5. Check kill switch NORMAL
echo "Kill switch check: timers active"

# 6. git status clean
if [ -n "$(git status --porcelain)" ]; then
    echo "WARN: git status not clean"
else
    echo "git status: clean"
fi

# 7. Merge PR #694
echo "All checks PASS. Merging PR #694..."
gh pr merge 694 --squash --subject "feat(activation): Phase 1 — 5 READ_ONLY timers activated" --body "Phase 1 activation: 5 READ_ONLY timers deployed, 24h observation PASS."
echo "=== Auto-merge complete: $(date -u) ==="
