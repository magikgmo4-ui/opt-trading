#!/usr/bin/env bash
# openclaw-core session — gateway + bridge + health + logs
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

SESSION="openclaw-core"
TMUX="${TMUX_CMD:-tmux}"

$TMUX new-session -d -s "$SESSION" -n core:gateway 2>/dev/null || true
$TMUX send-keys -t "$SESSION:core:gateway" "cd $PROJECT_ROOT && modules/gateway_openclaw/scripts/gateway_openclaw_cmd.sh attach" Enter

$TMUX new-window -t "$SESSION" -n core:bridge
$TMUX send-keys -t "$SESSION:core:bridge" "cd $PROJECT_ROOT && modules/openclaw_operator_bridge/scripts/cmd.sh start" Enter

$TMUX new-window -t "$SESSION" -n core:logs
$TMUX send-keys -t "$SESSION:core:logs" "tail -f $PROJECT_ROOT/logs/openclaw-core.log 2>/dev/null || echo 'no log yet'" Enter

$TMUX new-window -t "$SESSION" -n core:health
$TMUX send-keys -t "$SESSION:core:health" "while true; do curl -sf http://127.0.0.1:18789/health >/dev/null 2>&1 && echo '[OK] gateway live' || echo '[DOWN] gateway unreachable'; sleep 30; done" Enter
