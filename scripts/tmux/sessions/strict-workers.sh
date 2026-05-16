#!/usr/bin/env bash
# SESSION 3 — strict-workers (admin-trading)
# Pipeline workers GO-04→GO-10 — ALL start with DRY_RUN=1 (paper/dry mode)
set -e
SESSION="strict-workers"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already running"
    exit 0
fi

mkdir -p "$PROJECT_ROOT/logs"

# DRY_RUN=1 enforced on all workers — no live trades
DRY_ENV="DRY_RUN=1 PAPER_MODE=1"

tmux new-session -d -s "$SESSION" -n "signal_router"
tmux send-keys -t "$SESSION:signal_router" \
    "cd '$PROJECT_ROOT' && $DRY_ENV bash modules/signal_router/scripts/cmd.sh run 2>&1 | tee logs/signal_router.log" Enter

tmux new-window -t "$SESSION" -n "notification"
tmux send-keys -t "$SESSION:notification" \
    "cd '$PROJECT_ROOT' && $DRY_ENV bash modules/notification_dispatcher/scripts/cmd.sh run 2>&1 | tee logs/notification_dispatcher_worker.log" Enter

tmux new-window -t "$SESSION" -n "proposition"
tmux send-keys -t "$SESSION:proposition" \
    "cd '$PROJECT_ROOT' && $DRY_ENV bash modules/proposition_engine/scripts/cmd.sh run 2>&1 | tee logs/proposition_engine.log" Enter

tmux new-window -t "$SESSION" -n "validation"
tmux send-keys -t "$SESSION:validation" \
    "cd '$PROJECT_ROOT' && $DRY_ENV bash modules/validation_gate/scripts/cmd.sh run 2>&1 | tee logs/validation_gate.log" Enter

tmux new-window -t "$SESSION" -n "executor"
# trade_executor: DRY_RUN=1 enforced — never start live without explicit operator override
tmux send-keys -t "$SESSION:executor" \
    "cd '$PROJECT_ROOT' && DRY_RUN=1 PAPER_MODE=1 bash modules/trade_executor/scripts/cmd.sh run 2>&1 | tee logs/trade_executor.log" Enter

tmux new-window -t "$SESSION" -n "result_tracker"
tmux send-keys -t "$SESSION:result_tracker" \
    "cd '$PROJECT_ROOT' && $DRY_ENV bash modules/result_tracker/scripts/cmd.sh run 2>&1 | tee logs/result_tracker.log" Enter

tmux new-window -t "$SESSION" -n "datasheet"
tmux send-keys -t "$SESSION:datasheet" \
    "cd '$PROJECT_ROOT' && $DRY_ENV bash modules/datasheet_writer/scripts/cmd.sh run 2>&1 | tee logs/datasheet_writer.log" Enter

tmux new-window -t "$SESSION" -n "learning"
tmux send-keys -t "$SESSION:learning" \
    "cd '$PROJECT_ROOT' && $DRY_ENV bash modules/learning_feeder/scripts/cmd.sh run 2>&1 | tee logs/learning_feeder.log" Enter

tmux select-window -t "$SESSION:signal_router"
echo "$SESSION started (8 windows: signal_router notification proposition validation executor result_tracker datasheet learning)"
echo "NOTE: DRY_RUN=1 PAPER_MODE=1 enforced on all workers"
