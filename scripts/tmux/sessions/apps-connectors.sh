#!/usr/bin/env bash
# apps-connectors session — airtable + clickup + sheets
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

SESSION="apps-connectors"
TMUX="${TMUX_CMD:-tmux}"

$TMUX new-session -d -s "$SESSION" -n apps:airtable 2>/dev/null || true
$TMUX send-keys -t "$SESSION:apps:airtable" "cd $PROJECT_ROOT && echo 'airtable sync — task_tracker'" Enter

$TMUX new-window -t "$SESSION" -n apps:clickup
$TMUX send-keys -t "$SESSION:apps:clickup" "cd $PROJECT_ROOT && echo 'clickup sync — task_tracker'" Enter

$TMUX new-window -t "$SESSION" -n apps:sheets
$TMUX send-keys -t "$SESSION:apps:sheets" "cd $PROJECT_ROOT && echo 'sheets sync — datasheet_writer'" Enter

$TMUX new-window -t "$SESSION" -n apps:health
$TMUX send-keys -t "$SESSION:apps:health" "cd $PROJECT_ROOT && while true; do echo '[health] apps connectors OK — $(date -u +%H:%M:%S)'; sleep 300; done" Enter
