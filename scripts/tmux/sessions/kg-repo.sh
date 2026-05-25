#!/usr/bin/env bash
# kg-repo session — memory_bricks + learning_feeder
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

SESSION="kg-repo"
TMUX="${TMUX_CMD:-tmux}"

$TMUX new-session -d -s "$SESSION" -n kg:memory_bricks 2>/dev/null || true
$TMUX send-keys -t "$SESSION:kg:memory_bricks" "cd $PROJECT_ROOT && echo 'memory_bricks — learning store daemon'" Enter

$TMUX new-window -t "$SESSION" -n kg:learning_feeder
$TMUX send-keys -t "$SESSION:kg:learning_feeder" "cd $PROJECT_ROOT && echo 'learning_feeder ready'" Enter

$TMUX new-window -t "$SESSION" -n kg:health
$TMUX send-keys -t "$SESSION:kg:health" "cd $PROJECT_ROOT && while true; do echo '[health] kg-repo OK — $(date -u +%H:%M:%S)'; sleep 30; done" Enter
