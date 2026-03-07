#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Run Logged
# Executes DeepSeek run_all and captures output to a log file

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$ROOT_DIR/data/logs/deepseek_student"
mkdir -p "$LOGS_DIR"

TIMESTAMP=$(date -u +"%Y%m%d_%H%M%S")
RUN_ID="deepseek_run_${TIMESTAMP}"
LOG_FILE="$LOGS_DIR/${RUN_ID}.log"
LATEST_LINK="$LOGS_DIR/latest.log"

DEEPSEEK_HUB_CMD="$ROOT_DIR/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh"

echo "=== DeepSeek Student Run (Logged) ==="
echo "Run ID:  $RUN_ID"
echo "Log:     $LOG_FILE"
echo "Start:   $(date -u)"
echo "----------------------------------------"

if [ ! -x "$DEEPSEEK_HUB_CMD" ]; then
    echo "Error: DeepSeek Hub script not executable: $DEEPSEEK_HUB_CMD"
    exit 1
fi

# Run and capture output (tee)
if bash "$DEEPSEEK_HUB_CMD" run_all 2>&1 | tee "$LOG_FILE"; then
    STATUS="SUCCESS"
else
    STATUS="FAILED"
fi

echo "----------------------------------------"
echo "End:     $(date -u)"
echo "Status:  $STATUS"

# Update latest link
rm -f "$LATEST_LINK"
ln -s "$LOG_FILE" "$LATEST_LINK"

echo "Log saved to: $LOG_FILE"
echo "Latest log linked at: $LATEST_LINK"

exit 0
