#!/usr/bin/env bash
set -Eeuo pipefail
# SPCX Ops Readiness Check
# GO_SPACEX_OPS_READINESS_LIVE_01
#
# Usage: ./spacex_ops_ready_check.sh [--json]
# Output: console + reports/ipo/spacex/ops_ready_YYYYMMDD_HHMM.md

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

NOW=$(date -Iseconds)
REPORT_DIR="reports/ipo/spacex"
REPORT_FILE="$REPORT_DIR/ops_ready_$(date +%Y%m%d_%H%M).md"
mkdir -p "$REPORT_DIR"

PASS=0
FAIL=0
WARN=0
LINES=()

check() {
    local name="$1" cmd="$2"
    if eval "$cmd" &>/dev/null; then
        LINES+=("| ✅ | $name |")
        ((PASS++)) || true
    else
        LINES+=("| ❌ | $name |")
        ((FAIL++)) || true
    fi
}

check_warn() {
    local name="$1" cmd="$2"
    if eval "$cmd" &>/dev/null; then
        LINES+=("| ✅ | $name |")
        ((PASS++)) || true
    else
        LINES+=("| ⚠️ | $name |")
        ((WARN++)) || true
    fi
}

# ----- CHECKS -----

# Git
EXPECTED_COMMIT="${EXPECTED_COMMIT:-}"
ACTUAL_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
check "git repo accessible" "git rev-parse HEAD"
if [ -n "$EXPECTED_COMMIT" ]; then
    if [ "$ACTUAL_COMMIT" = "$EXPECTED_COMMIT" ]; then
        LINES+=("| ✅ | git commit = $EXPECTED_COMMIT |")
        ((PASS++)) || true
    else
        LINES+=("| ❌ | git commit $ACTUAL_COMMIT != expected $EXPECTED_COMMIT |")
        ((FAIL++)) || true
    fi
else
    LINES+=("| ℹ️ | git commit = $ACTUAL_COMMIT |")
fi

check_warn "git clean (no modified tracked)" "git diff --quiet HEAD"

# Services
check "webhook_server :8000" "ss -lntp | grep -q ':8000 '"
check_warn "perf_app :8010" "ss -lntp | grep -q ':8010 '"
check_warn "cloudflared tunnel" "pgrep -f cloudflared"

# Timers
check "orderflow timer active" "systemctl is-active spcx-orderflow-pipeline.timer 2>/dev/null | grep -q active"
check "EOD backtest timer active" "systemctl is-active spcx-v2-backtest.timer 2>/dev/null | grep -q active"

# Data freshness
SNAPSHOT_PATH="data/ipo/spacex/scored/latest_snapshot.json"
if [ -f "$SNAPSHOT_PATH" ]; then
    SNAP_AGE=$(($(date +%s) - $(stat -c %Y "$SNAPSHOT_PATH" 2>/dev/null || echo 0)))
    TV_ACTIVE=$(python3 -c "import json; d=json.load(open('$SNAPSHOT_PATH')); print(d.get('tv_alert_active','false'))" 2>/dev/null || echo "false")
    if [ "$SNAP_AGE" -lt 600 ]; then
        LINES+=("| ✅ | latest_snapshot.json fresh (${SNAP_AGE}s) |")
        ((PASS++)) || true
    elif [ "$SNAP_AGE" -lt 3600 ]; then
        LINES+=("| ⚠️ | latest_snapshot.json stale (${SNAP_AGE}s) |")
        ((WARN++)) || true
    else
        LINES+=("| ❌ | latest_snapshot.json very stale (${SNAP_AGE}s) |")
        ((FAIL++)) || true
    fi
    if [ "$TV_ACTIVE" = "True" ] || [ "$TV_ACTIVE" = "true" ]; then
        LINES+=("| ✅ | tv_alert_active=True |")
        ((PASS++)) || true
    else
        LINES+=("| ⚠️ | tv_alert_active=False (no real TradingView fire yet) |")
        ((WARN++)) || true
    fi
    PIPELINE_STATE=$(python3 -c "import json; d=json.load(open('$SNAPSHOT_PATH')); print(d.get('pipeline_state','unknown'))" 2>/dev/null || echo "unknown")
    SQ_TIER=$(python3 -c "import json; d=json.load(open('$SNAPSHOT_PATH')); print(d.get('source_quality',{}).get('overall_tier','unknown'))" 2>/dev/null || echo "unknown")
    LINES+=("| ℹ️ | pipeline_state=$PIPELINE_STATE source_quality=$SQ_TIER |")
else
    LINES+=("| ❌ | latest_snapshot.json missing |")
    ((FAIL++)) || true
fi

BUCKET_PATH="state/ipo/spacex/orderflow_buckets/latest.json"
if [ -f "$BUCKET_PATH" ]; then
    BUCKET_AGE=$(($(date +%s) - $(stat -c %Y "$BUCKET_PATH" 2>/dev/null || echo 0)))
    BUCKET_COUNT=$(python3 -c "import json; d=json.load(open('$BUCKET_PATH')); print(d.get('count',0))" 2>/dev/null || echo 0)
    if [ "$BUCKET_AGE" -lt 600 ]; then
        LINES+=("| ✅ | orderflow buckets fresh (${BUCKET_AGE}s, ${BUCKET_COUNT} buckets) |")
        ((PASS++)) || true
    else
        LINES+=("| ⚠️ | orderflow buckets stale (${BUCKET_AGE}s) |")
        ((WARN++)) || true
    fi
else
    LINES+=("| ⚠️ | orderflow buckets not yet generated |")
    ((WARN++)) || true
fi

SPCX_WEBHOOK_JSONL="data/ipo/spacex/raw/spacex_snapshots.jsonl"
GENERIC_EVENTS_JSONL="state/events.jsonl"

if [ -s "$SPCX_WEBHOOK_JSONL" ] && tail -n 1 "$SPCX_WEBHOOK_JSONL" 2>/dev/null | python3 -c "import sys,json; json.loads(sys.stdin.read())" 2>/dev/null; then
    LAST_EVENT=$(tail -n 1 "$SPCX_WEBHOOK_JSONL" 2>/dev/null | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('received_at','')[:19])" 2>/dev/null || echo "?")
    LINES+=("| ✅ | SPCX webhook jsonl parseable (last: $LAST_EVENT) |")
    ((PASS++)) || true
elif [ -s "$GENERIC_EVENTS_JSONL" ] && tail -n 1 "$GENERIC_EVENTS_JSONL" 2>/dev/null | python3 -c "import sys,json; json.loads(sys.stdin.read())" 2>/dev/null; then
    LINES+=("| ⚠️ | generic webhook events (SPCX raw path empty) |")
    ((WARN++)) || true
else
    LINES+=("| ⚠️ | webhook events jsonl empty or unparseable |")
    ((WARN++)) || true
fi

# Disk
check "disk > 1GB free" "[ $(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//') -gt 1 ]"

# Journal errors
ERROR_COUNT=$(journalctl -u spcx-orderflow-pipeline.service --since "1 hour ago" 2>/dev/null | grep -ci "error\|traceback\|fail" 2>/dev/null || echo "0")
ERROR_COUNT=$(echo "$ERROR_COUNT" | tr -d '\n\r' | grep -o '[0-9]*' || echo "0")
ERROR_COUNT=${ERROR_COUNT:-0}
if [ "$ERROR_COUNT" -eq 0 ]; then
    LINES+=("| ✅ | no recent orderflow timer errors |")
    ((PASS++)) || true
else
    LINES+=("| ⚠️ | $ERROR_COUNT recent orderflow timer errors |")
    ((WARN++)) || true
fi

# ----- REPORT -----
{
    echo "# SPCX Ops Readiness Report"
    echo ""
    echo "Generated: $NOW"
    echo "Host: $(hostname)"
    echo "Git: $ACTUAL_COMMIT"
    echo ""
    echo "## Results"
    echo ""
    echo "| Status | Check |"
    echo "|--------|-------|"
    for line in "${LINES[@]}"; do echo "$line"; done
    echo ""
    echo "## Summary"
    echo ""
    echo "- ✅ Pass: $PASS"
    echo "- ❌ Fail: $FAIL"
    echo "- ⚠️  Warn: $WARN"
    echo ""
    VERDICT="NOT READY"
    if [ "$FAIL" -eq 0 ] && [ "$WARN" -le 2 ]; then
        VERDICT="OPS READY"
    elif [ "$FAIL" -eq 0 ]; then
        VERDICT="OPS READY (with warnings)"
    fi
    echo "## Verdict: **$VERDICT**"
    echo ""
    echo "---"
} > "$REPORT_FILE"

# Console output
cat "$REPORT_FILE"

echo ""
echo "Report: $REPORT_FILE"
