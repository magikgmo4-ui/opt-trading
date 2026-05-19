#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Tail Latest Log
# Shows the tail of the latest run log

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$ROOT_DIR/data/logs/desk_pro"
LATEST_LINK="$LOGS_DIR/latest.log"

if [ ! -f "$LATEST_LINK" ]; then
    echo "No latest log found at $LATEST_LINK"
    # Try finding newest file
    LATEST_FILE=$(find "$LOGS_DIR" -maxdepth 1 -name "run_*.log" | sort -r | head -n 1)
    if [ -n "$LATEST_FILE" ]; then
        LATEST_LINK="$LATEST_FILE"
        echo "Found newest log: $(basename "$LATEST_LINK")"
    else
        echo "No log files found in $LOGS_DIR"
        exit 1
    fi
fi

echo "=== Tailing Latest Log: $(basename "$(readlink -f "$LATEST_LINK")") ==="
echo "Path: $LATEST_LINK"
echo "----------------------------------------"
tail -n 50 "$LATEST_LINK"
echo "----------------------------------------"
echo "(End of tail)"
