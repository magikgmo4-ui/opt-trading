#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Run Logged
# Executes a run and captures output to a log file

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$ROOT_DIR/data/logs/desk_pro"
mkdir -p "$LOGS_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOGS_DIR/run_$TIMESTAMP.log"
LATEST_LINK="$LOGS_DIR/latest.log"

echo "=== Desk Pro Run (Logged) ==="
echo "Log file: $LOG_FILE"
echo "Starting run..."

# Execute run and tee output to log
# We use the main desk_pro_cmd.sh wrapper to ensure consistent environment
if bash "$SCRIPT_DIR/desk_pro_cmd.sh" run 2>&1 | tee "$LOG_FILE"; then
    echo "Run SUCCESS."
    STATUS="SUCCESS"
else
    echo "Run FAILED."
    STATUS="FAILED"
fi

# Update latest link
rm -f "$LATEST_LINK"
ln -s "$LOG_FILE" "$LATEST_LINK"

echo "Log saved to: $LOG_FILE"
echo "Latest log linked at: $LATEST_LINK"

exit 0
