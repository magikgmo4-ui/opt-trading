#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Last Run Info
# Summarizes the latest execution details
# Updated: Support for latest_status.txt and latest_run_id.txt

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

RUNS_DIR="$ROOT_DIR/data/desk_runs"
LOGS_DIR="$ROOT_DIR/data/logs/desk_pro"

echo "=== Last Run Info ==="
echo "Date: $(date -u)"

# 1. Check Latest Log Info
LATEST_LOG="$LOGS_DIR/latest.log"
LATEST_RUN_ID_FILE="$LOGS_DIR/latest_run_id.txt"
LATEST_STATUS_FILE="$LOGS_DIR/latest_status.txt"

if [ -f "$LATEST_RUN_ID_FILE" ]; then
    RUN_ID=$(cat "$LATEST_RUN_ID_FILE")
    STATUS=$(cat "$LATEST_STATUS_FILE" 2>/dev/null || echo "UNKNOWN")
    echo "Latest Logged Run:"
    echo "  ID:     $RUN_ID"
    echo "  Status: $STATUS"
    
    if [ -L "$LATEST_LOG" ]; then
        TARGET=$(readlink -f "$LATEST_LOG")
        echo "  Log:    $(basename "$TARGET")"
        echo "  Path:   $TARGET"
    fi
else
    echo "Latest Logged Run: No info file found."
fi

echo "----------------------------------------"

# 2. Check Orchestrator Runs
if [ -d "$RUNS_DIR" ]; then
    LATEST_RUN=$(find "$RUNS_DIR" -maxdepth 1 -name "desk_run_*" -type d -exec test -e "{}/run_summary.json" \; -print | sort -r | head -n 1)
    if [ -n "$LATEST_RUN" ]; then
        echo "Latest Orchestration Output:"
        echo "  ID: $(basename "$LATEST_RUN")"
        echo "  Path: $LATEST_RUN"
        
        if [ -f "$LATEST_RUN/run_summary.json" ]; then
            SUMMARY_HEAD=$(grep "summary" "$LATEST_RUN/run_summary.json" | head -n 1 | cut -c 1-60)
            echo "  Summary: $SUMMARY_HEAD..."
        else
            echo "  Summary: (File Missing)"
        fi
    else
        echo "Orchestration: No valid run found."
    fi
else
    echo "Orchestration: No runs directory."
fi

echo "========================================"
