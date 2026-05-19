#!/usr/bin/env bash
# SESSION — fleet-status (db-layer)
# Fleet orchestrator status + runtime health monitor
set -e
SESSION="fleet-status"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already running"
    exit 0
fi

mkdir -p "$PROJECT_ROOT/logs"

tmux new-session -d -s "$SESSION" -n "fleet"
tmux send-keys -t "$SESSION:fleet" \
    "cd '$PROJECT_ROOT' && python3 modules/runtime_health/fleet_orchestrator.py --no-telegram 2>&1 | tee -a logs/fleet_orchestrator.log" Enter

tmux new-window -t "$SESSION" -n "health"
tmux send-keys -t "$SESSION:health" \
    "cd '$PROJECT_ROOT' && watch -n 60 'python3 modules/runtime_health/fleet_orchestrator.py --dry-run 2>&1 | tail -10'" Enter

tmux new-window -t "$SESSION" -n "logs"
tmux send-keys -t "$SESSION:logs" \
    "cd '$PROJECT_ROOT' && tail -f logs/fleet_orchestrator.log" Enter

tmux new-window -t "$SESSION" -n "status"
tmux send-keys -t "$SESSION:status" \
    "cd '$PROJECT_ROOT' && watch -n 30 'jq . data/runtime_health/fleet_status.json 2>/dev/null || echo waiting_for_data'" Enter

tmux select-window -t "$SESSION:fleet"
echo "$SESSION started (windows: fleet health logs status)"
