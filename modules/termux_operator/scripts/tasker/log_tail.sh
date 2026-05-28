#!/data/data/com.termux/files/usr/bin/bash
# Tasker-callable: tail last N lines of a session log
# Usage: log_tail.sh <session> [lines=30] [host=db-layer]
set -Eeuo pipefail
SESSION="${1:-}"
LINES="${2:-30}"
HOST="${3:-db-layer}"
if [ -z "$SESSION" ]; then
    echo "Usage: log_tail.sh <session> [lines=30] [host=db-layer]"
    exit 2
fi
LOG_FILE="/opt/trading/logs/${SESSION}.log"
ssh -o BatchMode=yes -o ConnectTimeout=5 "$HOST" \
    "tail -n $LINES $LOG_FILE 2>/dev/null || echo 'Log not found: $LOG_FILE'"
