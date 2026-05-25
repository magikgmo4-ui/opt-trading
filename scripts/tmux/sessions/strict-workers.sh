#!/usr/bin/env bash
# strict-workers session — signal_router → proposition → validation → trade → result → datasheet → learning
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

SESSION="strict-workers"
TMUX="${TMUX_CMD:-tmux}"

$TMUX new-session -d -s "$SESSION" -n workers:signal_router 2>/dev/null || true
$TMUX send-keys -t "$SESSION:workers:signal_router" "cd $PROJECT_ROOT && modules/signal_router/scripts/cmd.sh start 2>&1 | tee $PROJECT_ROOT/logs/signal_router.log" Enter

$TMUX new-window -t "$SESSION" -n workers:notification
$TMUX send-keys -t "$SESSION:workers:notification" "cd $PROJECT_ROOT && echo 'notification_dispatcher ready'" Enter

$TMUX new-window -t "$SESSION" -n workers:proposition
$TMUX send-keys -t "$SESSION:workers:proposition" "cd $PROJECT_ROOT && echo 'proposition_engine ready'" Enter

$TMUX new-window -t "$SESSION" -n workers:validation
$TMUX send-keys -t "$SESSION:workers:validation" "cd $PROJECT_ROOT && echo 'validation_gate ready'" Enter

$TMUX new-window -t "$SESSION" -n workers:executor
$TMUX send-keys -t "$SESSION:workers:executor" "cd $PROJECT_ROOT && echo 'trade_executor ready — NO AUTO RESTART'" Enter

$TMUX new-window -t "$SESSION" -n workers:result_tracker
$TMUX send-keys -t "$SESSION:workers:result_tracker" "cd $PROJECT_ROOT && echo 'result_tracker ready'" Enter

$TMUX new-window -t "$SESSION" -n workers:datasheet
$TMUX send-keys -t "$SESSION:workers:datasheet" "cd $PROJECT_ROOT && echo 'datasheet_writer ready'" Enter

$TMUX new-window -t "$SESSION" -n workers:learning
$TMUX send-keys -t "$SESSION:workers:learning" "cd $PROJECT_ROOT && echo 'learning_feeder ready'" Enter
