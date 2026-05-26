#!/usr/bin/env bash
# desk-pro session — desk_pro + perf + orchestrator
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

SESSION="desk-pro"
TMUX="${TMUX_CMD:-tmux}"

$TMUX new-session -d -s "$SESSION" -n desk:runner 2>/dev/null || true
$TMUX send-keys -t "$SESSION:desk:runner" "cd $PROJECT_ROOT && modules/desk_pro_runner/scripts/cmd.sh run-and-show 2>&1 | tee $PROJECT_ROOT/logs/desk_pro.log" Enter

$TMUX new-window -t "$SESSION" -n desk:orchestrator
$TMUX send-keys -t "$SESSION:desk:orchestrator" "cd $PROJECT_ROOT && echo 'desk_pro_orchestrator — conductor'" Enter

$TMUX new-window -t "$SESSION" -n desk:perf
$TMUX send-keys -t "$SESSION:desk:perf" "cd $PROJECT_ROOT && modules/perf/scripts/perf_cmd.sh start 2>&1 | tee $PROJECT_ROOT/logs/perf.log" Enter

$TMUX new-window -t "$SESSION" -n desk:logs
$TMUX send-keys -t "$SESSION:desk:logs" "tail -f $PROJECT_ROOT/logs/desk_pro.log 2>/dev/null || echo 'no log yet'" Enter
