#!/usr/bin/env bash
# SESSION 6 — apps-connectors (db-layer)
# Airtable + ClickUp + Sheets sync
set -e
SESSION="apps-connectors"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already running"
    exit 0
fi

mkdir -p "$PROJECT_ROOT/logs"

tmux new-session -d -s "$SESSION" -n "airtable"
tmux send-keys -t "$SESSION:airtable" \
    "cd '$PROJECT_ROOT' && echo 'airtable sync: waiting for task_tracker GO-09' && tail -f /dev/null 2>&1 | tee logs/airtable_sync.log" Enter

tmux new-window -t "$SESSION" -n "clickup"
tmux send-keys -t "$SESSION:clickup" \
    "cd '$PROJECT_ROOT' && echo 'clickup sync: waiting for task_tracker GO-09' && tail -f /dev/null 2>&1 | tee logs/clickup_sync.log" Enter

tmux new-window -t "$SESSION" -n "sheets"
# datasheet_writer Sheets sync — dry_run until Sheets API configured
tmux send-keys -t "$SESSION:sheets" \
    "cd '$PROJECT_ROOT' && DRY_RUN=1 bash modules/datasheet_writer/scripts/cmd.sh run 2>&1 | tee logs/sheets_sync.log" Enter

tmux new-window -t "$SESSION" -n "health"
tmux send-keys -t "$SESSION:health" \
    "cd '$PROJECT_ROOT' && while true; do echo 'apps-connectors health OK' && sleep 300; done 2>&1 | tee -a logs/apps_connectors_health.log" Enter

tmux select-window -t "$SESSION:airtable"
echo "$SESSION started (windows: airtable clickup sheets health)"
