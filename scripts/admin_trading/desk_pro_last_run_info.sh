#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Last Run Info
# Summarizes the latest execution details

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

# 1. Check Runs (Orchestrator Output)
if [ -d "$RUNS_DIR" ]; then
    LATEST_RUN=$(find "$RUNS_DIR" -maxdepth 1 -name "desk_run_*" -type d -exec test -e "{}/run_summary.json" \; -print | sort -r | head -n 1)
    if [ -n "$LATEST_RUN" ]; then
        echo "Latest Orchestration Run:"
        echo "  ID: $(basename "$LATEST_RUN")"
        echo "  Path: $LATEST_RUN"
        echo "  Summary File: $(test -f "$LATEST_RUN/run_summary.json" && echo "Present" || echo "Missing")"
        echo "  Portfolio File: $(test -f "$LATEST_RUN/portfolio_engine.json" && echo "Present" || echo "Missing")"
    else
        echo "Orchestration: No valid run found."
    fi
else
    echo "Orchestration: No runs directory."
fi

echo "----------------------------------------"

# 2. Check Logs (Execution Log)
LATEST_LOG="$LOGS_DIR/latest.log"
if [ -L "$LATEST_LOG" ]; then
    TARGET=$(readlink -f "$LATEST_LOG")
    echo "Latest Execution Log:"
    echo "  File: $(basename "$TARGET")"
    echo "  Path: $TARGET"
    echo "  Size: $(du -h "$TARGET" | cut -f1)"
    echo "  Last Modified: $(date -r "$TARGET" "+%Y-%m-%d %H:%M:%S")"
else
    echo "Logs: No latest log link found."
fi

echo "========================================"
