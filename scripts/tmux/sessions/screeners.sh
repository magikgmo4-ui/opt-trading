#!/usr/bin/env bash
# screeners session — tradingview + webhook + bot_vision + telegram
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

SESSION="screeners"
TMUX="${TMUX_CMD:-tmux}"

$TMUX new-session -d -s "$SESSION" -n screeners:tradingview 2>/dev/null || true
$TMUX send-keys -t "$SESSION:screeners:tradingview" "cd $PROJECT_ROOT && echo 'tradingview_observer — watch alerts'" Enter

$TMUX new-window -t "$SESSION" -n screeners:webhook
$TMUX send-keys -t "$SESSION:screeners:webhook" "cd $PROJECT_ROOT && python3 webhook_server.py 2>&1 | tee $PROJECT_ROOT/logs/webhook.log" Enter

$TMUX new-window -t "$SESSION" -n screeners:bot_vision
$TMUX send-keys -t "$SESSION:screeners:bot_vision" "cd $PROJECT_ROOT && modules/bot_vision_step2/scripts/cmd.sh start 2>&1 | tee $PROJECT_ROOT/logs/bot_vision.log" Enter

$TMUX new-window -t "$SESSION" -n screeners:telegram
$TMUX send-keys -t "$SESSION:screeners:telegram" "cd $PROJECT_ROOT && echo 'notification_dispatcher — Telegram bot ready'" Enter
