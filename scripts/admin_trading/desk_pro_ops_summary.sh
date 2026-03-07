#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Ops Summary (Short)
# A quick status overview for operators

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$ROOT_DIR/data/logs/desk_pro"
JOURNAL_FILE="$LOGS_DIR/session_journal.log"

echo "=== Desk Pro Ops Summary ==="

# 1. Latest Run Status
if [ -f "$LOGS_DIR/latest_status.txt" ]; then
    STATUS=$(cat "$LOGS_DIR/latest_status.txt")
    RUN_ID=$(cat "$LOGS_DIR/latest_run_id.txt" 2>/dev/null || echo "Unknown")
    echo "Last Run: $STATUS ($RUN_ID)"
else
    echo "Last Run: No status file found."
fi

# 2. Latest Log File
if [ -L "$LOGS_DIR/latest.log" ]; then
    TARGET=$(readlink -f "$LOGS_DIR/latest.log")
    echo "Log File: $(basename "$TARGET")"
else
    echo "Log File: None"
fi

# 3. Latest Journal Entry
if [ -f "$JOURNAL_FILE" ]; then
    echo "Last Note:"
    tail -n 1 "$JOURNAL_FILE" | cut -c 1-60
else
    echo "Journal: Empty"
fi

echo "============================"
