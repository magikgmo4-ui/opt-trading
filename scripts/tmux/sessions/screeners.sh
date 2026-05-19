#!/usr/bin/env bash
# SESSION 2 — screeners (admin-trading)
# TradingView observer + webhook + bot_vision + notification_dispatcher
set -e
SESSION="screeners"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already running"
    exit 0
fi

mkdir -p "$PROJECT_ROOT/logs"

tmux new-session -d -s "$SESSION" -n "tradingview"
tmux send-keys -t "$SESSION:tradingview" \
    "cd '$PROJECT_ROOT' && bash modules/tradingview_observer/cmd.sh run 2>&1 | tee logs/tradingview_observer.log" Enter

tmux new-window -t "$SESSION" -n "webhook"
tmux send-keys -t "$SESSION:webhook" \
    "cd '$PROJECT_ROOT' && bash modules/webhook/cmd.sh run 2>&1 | tee logs/webhook.log" Enter

tmux new-window -t "$SESSION" -n "bot_vision"
tmux send-keys -t "$SESSION:bot_vision" \
    "cd '$PROJECT_ROOT' && bash modules/bot_vision/cmd.sh run 2>&1 | tee logs/bot_vision.log" Enter

tmux new-window -t "$SESSION" -n "telegram"
tmux send-keys -t "$SESSION:telegram" \
    "cd '$PROJECT_ROOT' && bash modules/notification_dispatcher/scripts/cmd.sh run 2>&1 | tee logs/notification_dispatcher.log" Enter

tmux select-window -t "$SESSION:tradingview"
echo "$SESSION started (windows: tradingview webhook bot_vision telegram)"
