#!/usr/bin/env bash
# SESSION 4 — trading-pipeline (admin-trading)
# kil_v1 + simex + execution + risk + position engines
# kil_v1: NO auto-restart (safety device)
# trade_executor: manual restart only (safety — avoid double trade)
set -e
SESSION="trading-pipeline"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already running"
    exit 0
fi

mkdir -p "$PROJECT_ROOT/logs"

tmux new-session -d -s "$SESSION" -n "kil_v1"
# kil_v1 = safety device — monitor only, never auto-restart
tmux send-keys -t "$SESSION:kil_v1" \
    "cd '$PROJECT_ROOT' && bash modules/kil_v1/src/kil_v1/cli.py status 2>&1 | tee logs/kil_v1.log" Enter

tmux new-window -t "$SESSION" -n "simex_bridge"
tmux send-keys -t "$SESSION:simex_bridge" \
    "cd '$PROJECT_ROOT' && DRY_RUN=1 bash modules/simex_bitget_bridge/sanity.sh 2>&1 | tee logs/simex_bitget_bridge.log" Enter

tmux new-window -t "$SESSION" -n "execution"
tmux send-keys -t "$SESSION:execution" \
    "cd '$PROJECT_ROOT' && python3 -m modules.execution_engine.app.execution_engine status 2>&1 | tee logs/execution_engine.log" Enter

tmux new-window -t "$SESSION" -n "risk"
tmux send-keys -t "$SESSION:risk" \
    "cd '$PROJECT_ROOT' && python3 -m modules.risk_engine.app.risk_engine status 2>&1 | tee logs/risk_engine.log" Enter

tmux new-window -t "$SESSION" -n "position"
tmux send-keys -t "$SESSION:position" \
    "cd '$PROJECT_ROOT' && echo 'position_engine: monitor mode' && tail -f /dev/null" Enter

tmux select-window -t "$SESSION:kil_v1"
echo "$SESSION started (windows: kil_v1 simex_bridge execution risk position)"
echo "NOTE: kil_v1 = safety device — NEVER auto-restart"
