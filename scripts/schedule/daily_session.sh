#!/usr/bin/env bash
set -euo pipefail
# Daily Session Scheduler — planifie l'exécution quotidienne du pipeline dry-run.
#
# Usage:
#   ./daily_session.sh [--dry-run] [--controlled-write-sheets]
#
# Modes:
#   --dry-run                 (default) pipeline + Sheets dry-run
#   --controlled-write-sheets  active l'écriture Sheets (pipeline toujours dry-run)
#
# Invariants:
#   DRY_RUN_DEFAULT = true
#   NO_AUTOMATIC_SHEETS_WRITE = true
#   CONTROLLED_WRITE_MANUAL_ONLY = true
#   NO_LIVE_TRADE = true
#   NO_BITGET_ORDER = true
#   LOCALCMS_READ_ONLY = true
#   NO_DANGEROUS_RUNTIME_MUTATION = true

if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCHEDULER_LOG_DIR="$ROOT_DIR/data/logs/scheduler"
JOURNAL_SCRIPT="$ROOT_DIR/scripts/e2e/daily_session_journal.py"
SYNC_SCRIPT="$ROOT_DIR/scripts/sheets/sync_daily_session.py"
LOCALCMS_BASE="http://127.0.0.1:8700"
DRY_RUN="${DRY_RUN:-1}"
PAPER_MODE="${PAPER_MODE:-1}"

mkdir -p "$SCHEDULER_LOG_DIR"

CONTROLLED_WRITE_SHEETS=false
if [ "${1:-}" = "--controlled-write-sheets" ]; then
    CONTROLLED_WRITE_SHEETS=true
fi

log() {
    local level="${1:-INFO}"
    local msg="${2:-}"
    local ts
    ts=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    echo "[$ts] [$level] $msg" | tee -a "$SCHEDULER_LOG_DIR/scheduler.log"
}

log "=== Daily Session Scheduler ==="
log "DRY_RUN=$DRY_RUN PAPER_MODE=$PAPER_MODE"
log "CONTROLLED_WRITE_SHEETS=$CONTROLLED_WRITE_SHEETS"

# ── Precheck TMUX ────────────────────────────────────────────────────
log "STEP" "precheck TMUX"
TMUX_OK=false
if command -v tmux >/dev/null 2>&1; then
    if tmux list-sessions >/dev/null 2>&1; then
        TMUX_OK=true
        log "OK" "TMUX is running"
    else
        log "WARN" "TMUX is installed but no sessions running"
    fi
else
    log "WARN" "tmux not found"
fi

# ── Precheck LocalCMS ────────────────────────────────────────────────
log "STEP" "precheck LocalCMS"
LCMS_OK=false
if command -v curl >/dev/null 2>&1; then
    lcms_status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "$LOCALCMS_BASE/health" 2>/dev/null || echo "000")
    if [ "$lcms_status" = "200" ]; then
        LCMS_OK=true
        log "OK" "LocalCMS /health returned 200"
    else
        log "WARN" "LocalCMS /health returned $lcms_status"
    fi
elif command -v python >/dev/null 2>&1; then
    lcms_ok=$(python -c "
import urllib.request
try:
    r = urllib.request.urlopen('$LOCALCMS_BASE/health', timeout=3)
    print('OK' if r.status == 200 else r.status)
except Exception as e:
    print('FAIL: ' + str(e))
" 2>/dev/null || echo "FAIL: unreachable")
    if [ "$lcms_ok" = "OK" ]; then
        LCMS_OK=true
        log "OK" "LocalCMS /health returned 200"
    else
        log "WARN" "LocalCMS health check: $lcms_ok"
    fi
else
    log "WARN" "No curl or python available for LocalCMS check"
fi

# ── Run daily session journal ────────────────────────────────────────
log "STEP" "run daily_session_journal.py"
JOURNAL_ARGS=("--no-closeout")
log "CMD" "python $JOURNAL_SCRIPT ${JOURNAL_ARGS[*]}"

JOURNAL_EXIT=0
python "$JOURNAL_SCRIPT" "${JOURNAL_ARGS[@]}" || JOURNAL_EXIT=$?
if [ "$JOURNAL_EXIT" -ne 0 ] && [ "$JOURNAL_EXIT" -ne 1 ]; then
    log "ERROR" "daily_session_journal.py failed with unexpected exit code $JOURNAL_EXIT"
    log "STATUS" "FAILED"
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] [scheduler] [FAILED] daily_session_journal.py exit=$JOURNAL_EXIT" >> "$SCHEDULER_LOG_DIR/scheduler.log"
    exit 1
fi
# Exit 1 with --no-closeout is expected (closeout_acknowledged=False)
log "OK" "daily_session_journal.py completed (exit=$JOURNAL_EXIT)"

# ── Get latest run_id ────────────────────────────────────────────────
LATEST_RUN_ID=$(python -c "
import json, sys
from pathlib import Path
d = Path('$ROOT_DIR/data/journal/daily')
files = sorted(d.glob('*.json'), reverse=True)
if files:
    data = json.loads(files[0].read_text())
    print(data.get('run_id', files[0].stem))
" 2>/dev/null || echo "unknown")
log "INFO" "Latest run_id: $LATEST_RUN_ID"

# ── Sync Google Sheets (dry-run par défaut) ──────────────────────────
log "STEP" "sync Google Sheets"
SYNC_ARGS=("--run-id" "$LATEST_RUN_ID")
if [ "$CONTROLLED_WRITE_SHEETS" = true ]; then
    SYNC_ARGS+=("--controlled-write")
    log "INFO" "controlled-write Sheets: ENABLED (manual override)"
else
    log "INFO" "controlled-write Sheets: DISABLED (dry-run only)"
fi
log "CMD" "python $SYNC_SCRIPT ${SYNC_ARGS[*]}"

if ! python "$SYNC_SCRIPT" "${SYNC_ARGS[@]}"; then
    log "WARN" "sync_daily_session.py exited non-zero (expected if no credentials)"
fi

# ── Status ───────────────────────────────────────────────────────────
log "STEP" "status"
log "STATUS" "COMPLETED"
log "RUN_ID" "$LATEST_RUN_ID"

echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] [scheduler] [COMPLETED] run_id=$LATEST_RUN_ID tmux=$TMUX_OK localcms=$LCMS_OK sheets=$CONTROLLED_WRITE_SHEETS" >> "$SCHEDULER_LOG_DIR/scheduler.log"
echo ""
echo "=== Daily Session Scheduler: COMPLETED ==="
echo "  run_id  : $LATEST_RUN_ID"
echo "  tmux    : $TMUX_OK"
echo "  localcms: $LCMS_OK"
echo "  sheets  : $CONTROLLED_WRITE_SHEETS (--controlled-write=$CONTROLLED_WRITE_SHEETS)"
echo "  log     : $SCHEDULER_LOG_DIR/scheduler.log"
echo "=========================================="
