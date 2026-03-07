#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Run Logged
# Executes a run and captures output to a log file
# Updated: Unified timestamp format (UTC), harmonized run ID and log name

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

# Unified Timestamp (UTC): YYYYMMDD_HHMMSS
TIMESTAMP=$(date -u +"%Y%m%d_%H%M%S")
RUN_ID="desk_run_${TIMESTAMP}"
LOG_FILE="$LOGS_DIR/${RUN_ID}.log"

LATEST_LINK="$LOGS_DIR/latest.log"
LATEST_RUN_ID_FILE="$LOGS_DIR/latest_run_id.txt"
LATEST_STATUS_FILE="$LOGS_DIR/latest_status.txt"

echo "=== Desk Pro Run (Logged) ==="
echo "Run ID:  $RUN_ID"
echo "Log:     $LOG_FILE"
echo "Start:   $(date -u)"
echo "----------------------------------------"

# Execute run and tee output to log
# We pass the timestamp/run_id to the runner if supported, or just let it run.
# Since we can't easily force the runner's internal ID without changing python code,
# we focus on aligning the LOG filename with the execution time.
# Ideally, the orchestrator would accept an external run_id, but for this patch
# we accept that the orchestrator might generate its own slightly different ID
# if we don't pass it. However, the LOG is the source of truth for ops.

if bash "$SCRIPT_DIR/desk_pro_cmd.sh" run 2>&1 | tee "$LOG_FILE"; then
    STATUS="SUCCESS"
else
    STATUS="FAILED"
fi

echo "----------------------------------------"
echo "End:     $(date -u)"
echo "Status:  $STATUS"

# Update latest links/info
rm -f "$LATEST_LINK"
ln -s "$LOG_FILE" "$LATEST_LINK"
echo "$RUN_ID" > "$LATEST_RUN_ID_FILE"
echo "$STATUS" > "$LATEST_STATUS_FILE"

# Append to Session Journal
if [ -f "$SCRIPT_DIR/desk_pro_session_journal.sh" ]; then
    bash "$SCRIPT_DIR/desk_pro_session_journal.sh" add-entry "Run $RUN_ID completed with status $STATUS. Log: $LOG_FILE"
fi

echo "Log saved to: $LOG_FILE"
echo "Latest log linked at: $LATEST_LINK"

exit 0
