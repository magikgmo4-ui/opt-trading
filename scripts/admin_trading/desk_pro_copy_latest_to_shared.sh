#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Copy Latest to Shared
# Copies key artifacts from the latest run to /shared

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
RUNS_DIR="$ROOT_DIR/data/desk_runs"
SHARED_DIR="/shared/desk_pro/latest"

echo "=== Copy Latest Run to Shared ==="

# 1. Check Source
if [ ! -d "$RUNS_DIR" ]; then
    echo "Error: No runs directory found at $RUNS_DIR"
    exit 1
fi

# Find latest valid run (with summary)
LATEST_RUN=$(find "$RUNS_DIR" -maxdepth 1 -name "desk_run_*" -type d -exec test -e "{}/run_summary.json" \; -print | sort -r | head -n 1)

if [ -z "$LATEST_RUN" ]; then
    echo "Error: No valid run found."
    exit 1
fi

echo "Source Run: $(basename "$LATEST_RUN")"

# 2. Check Target
if [ ! -d "/shared" ]; then
    echo "Warning: /shared does not exist (not on admin-trading?). Skipping copy."
    # For local testing, we might simulate or just exit
    if [ "${DESK_PRO_MOCK_SHARED:-false}" == "true" ]; then
        SHARED_DIR="$ROOT_DIR/data/mock_shared/desk_pro/latest"
        echo "Mocking shared dir at: $SHARED_DIR"
    else
        exit 0
    fi
fi

mkdir -p "$SHARED_DIR"

# 3. Copy Artifacts
echo "Copying to: $SHARED_DIR"

cp "$LATEST_RUN/run_summary.json" "$SHARED_DIR/" 2>/dev/null || true
cp "$LATEST_RUN/portfolio_engine.json" "$SHARED_DIR/" 2>/dev/null || true
cp "$LATEST_RUN/journal_engine.json" "$SHARED_DIR/" 2>/dev/null || true
cp "$LATEST_RUN/perf_engine.json" "$SHARED_DIR/" 2>/dev/null || true

# Also copy exported dashboard if available in root output dir
DASH_DIR="$ROOT_DIR/data/dashboard"
if [ -d "$DASH_DIR" ]; then
    LATEST_HTML=$(find "$DASH_DIR" -name "dashboard_*.html" -type f | sort -r | head -n 1)
    if [ -n "$LATEST_HTML" ]; then
        cp "$LATEST_HTML" "$SHARED_DIR/dashboard_latest.html"
        echo "Copied dashboard: $(basename "$LATEST_HTML")"
    fi
fi

echo "Done."
ls -l "$SHARED_DIR"
