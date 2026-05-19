#!/usr/bin/env bash
# SESSION 1 — openclaw-core (db-layer)
# Gateway OpenClaw + operator bridge + health monitor
set -e
SESSION="openclaw-core"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already running"
    exit 0
fi

mkdir -p "$PROJECT_ROOT/logs"

tmux new-session -d -s "$SESSION" -n "gateway"
tmux send-keys -t "$SESSION:gateway" \
    "cd '$PROJECT_ROOT' && bash modules/gateway_openclaw/cmd.sh attach 2>&1 | tee logs/gateway_openclaw.log" Enter

tmux new-window -t "$SESSION" -n "bridge"
tmux send-keys -t "$SESSION:bridge" \
    "cd '$PROJECT_ROOT' && bash modules/openclaw_operator_bridge/scripts/cmd.sh attach 2>&1 | tee logs/openclaw_operator_bridge.log" Enter

tmux new-window -t "$SESSION" -n "health"
tmux send-keys -t "$SESSION:health" \
    "cd '$PROJECT_ROOT' && while true; do python3 scripts/tmux/health_check.py 2>&1 | tee -a logs/tmux_health.log; sleep 30; done" Enter

tmux new-window -t "$SESSION" -n "logs"
tmux send-keys -t "$SESSION:logs" \
    "cd '$PROJECT_ROOT' && tail -f logs/gateway_openclaw.log" Enter

tmux select-window -t "$SESSION:gateway"
echo "$SESSION started (windows: gateway bridge health logs)"
