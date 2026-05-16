#!/usr/bin/env bash
# SESSION 7 — desk-pro (admin-trading)
# desk_pro runner + orchestrator + perf
set -e
SESSION="desk-pro"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already running"
    exit 0
fi

mkdir -p "$PROJECT_ROOT/logs"

tmux new-session -d -s "$SESSION" -n "runner"
tmux send-keys -t "$SESSION:runner" \
    "cd '$PROJECT_ROOT' && bash modules/desk_pro_runner/cmd.sh run-and-show 2>&1 | tee logs/desk_pro.log" Enter

tmux new-window -t "$SESSION" -n "orchestrator"
tmux send-keys -t "$SESSION:orchestrator" \
    "cd '$PROJECT_ROOT' && bash modules/desk_pro_orchestrator/cmd.sh run 2>&1 | tee logs/desk_pro_orchestrator.log" Enter

tmux new-window -t "$SESSION" -n "perf"
tmux send-keys -t "$SESSION:perf" \
    "cd '$PROJECT_ROOT' && bash scripts/desk_pro_cmd.sh run 2>&1 | tee logs/perf.log" Enter

tmux new-window -t "$SESSION" -n "logs"
tmux send-keys -t "$SESSION:logs" \
    "cd '$PROJECT_ROOT' && tail -f logs/desk_pro.log" Enter

tmux select-window -t "$SESSION:runner"
echo "$SESSION started (windows: runner orchestrator perf logs)"
