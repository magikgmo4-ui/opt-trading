#!/usr/bin/env bash
# SESSION 8 — kg-repo (db-layer)
# memory_bricks + learning_feeder (GO-10 unlocked)
set -e
SESSION="kg-repo"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already running"
    exit 0
fi

mkdir -p "$PROJECT_ROOT/logs"

tmux new-session -d -s "$SESSION" -n "memory_bricks"
tmux send-keys -t "$SESSION:memory_bricks" \
    "cd '$PROJECT_ROOT' && bash modules/memory_bricks/cmd.sh run 2>&1 | tee logs/memory_bricks.log" Enter

tmux new-window -t "$SESSION" -n "learning_feeder"
tmux send-keys -t "$SESSION:learning_feeder" \
    "cd '$PROJECT_ROOT' && DRY_RUN=1 bash modules/learning_feeder/scripts/cmd.sh run 2>&1 | tee logs/learning_feeder.log" Enter

tmux new-window -t "$SESSION" -n "health"
tmux send-keys -t "$SESSION:health" \
    "cd '$PROJECT_ROOT' && while true; do python3 -c \"import sys; sys.path.insert(0,'.'); from scripts.tmux.health_check import check_sessions; import json; r=check_sessions(expected=frozenset({'kg-repo'})); print(json.dumps({'ts':r['timestamp'],'status':'ok' if r['all_ok'] else 'partial'}))\" 2>&1; sleep 60; done | tee -a logs/kg_repo_health.log" Enter

tmux select-window -t "$SESSION:memory_bricks"
echo "$SESSION started (windows: memory_bricks learning_feeder health)"
