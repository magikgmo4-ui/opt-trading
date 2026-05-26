#!/usr/bin/env bash
# trading-pipeline session — kil_v1 + simex + execution + risk + position
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

SESSION="trading-pipeline"
TMUX="${TMUX_CMD:-tmux}"

$TMUX new-session -d -s "$SESSION" -n pipeline:kil_v1 2>/dev/null || true
$TMUX send-keys -t "$SESSION:pipeline:kil_v1" "cd $PROJECT_ROOT && echo 'kil_v1 — kill switch monitor — NO AUTO RESTART'" Enter

$TMUX new-window -t "$SESSION" -n pipeline:simex_bridge
$TMUX send-keys -t "$SESSION:pipeline:simex_bridge" "cd $PROJECT_ROOT && echo 'simex_bitget_bridge — exchange connection monitor'" Enter

$TMUX new-window -t "$SESSION" -n pipeline:execution
$TMUX send-keys -t "$SESSION:pipeline:execution" "cd $PROJECT_ROOT && echo 'execution_engine — monitor'" Enter

$TMUX new-window -t "$SESSION" -n pipeline:risk
$TMUX send-keys -t "$SESSION:pipeline:risk" "cd $PROJECT_ROOT && echo 'risk_engine — monitor'" Enter

$TMUX new-window -t "$SESSION" -n pipeline:position
$TMUX send-keys -t "$SESSION:pipeline:position" "cd $PROJECT_ROOT && echo 'position_engine — monitor'" Enter
