#!/usr/bin/env bash
# localcms-ui session — localcms consumer + health + logs
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

SESSION="localcms-ui"
TMUX="${TMUX_CMD:-tmux}"

$TMUX new-session -d -s "$SESSION" -n lcms:consumer 2>/dev/null || true
$TMUX send-keys -t "$SESSION:lcms:consumer" "cd $PROJECT_ROOT && modules/localcms/app.py 2>&1 | tee $PROJECT_ROOT/logs/localcms.log" Enter

$TMUX new-window -t "$SESSION" -n lcms:health
$TMUX send-keys -t "$SESSION:lcms:health" "cd $PROJECT_ROOT && while true; do curl -sf http://127.0.0.1:8700/health >/dev/null 2>&1 && echo '[OK] localcms live' || echo '[DOWN] localcms unreachable'; sleep 30; done" Enter

$TMUX new-window -t "$SESSION" -n lcms:logs
$TMUX send-keys -t "$SESSION:lcms:logs" "tail -f $PROJECT_ROOT/logs/localcms.log 2>/dev/null || echo 'no log yet'" Enter
