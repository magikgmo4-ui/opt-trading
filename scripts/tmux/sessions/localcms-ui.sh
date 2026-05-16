#!/usr/bin/env bash
# SESSION 9 — localcms-ui (db-layer)
# LocalCMS consumer (FastAPI) + health + logs
set -e
SESSION="localcms-ui"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already running"
    exit 0
fi

mkdir -p "$PROJECT_ROOT/logs"

tmux new-session -d -s "$SESSION" -n "consumer"
tmux send-keys -t "$SESSION:consumer" \
    "cd '$PROJECT_ROOT' && uvicorn modules.localcms.app.main:app --host 127.0.0.1 --port 8700 2>&1 | tee logs/localcms_consumer.log" Enter

tmux new-window -t "$SESSION" -n "health"
tmux send-keys -t "$SESSION:health" \
    "cd '$PROJECT_ROOT' && while true; do curl -sf http://127.0.0.1:8700/health >/dev/null && echo 'localcms-ui health OK' || echo 'localcms-ui health DOWN'; sleep 30; done 2>&1 | tee -a logs/localcms_health.log" Enter

tmux new-window -t "$SESSION" -n "logs"
tmux send-keys -t "$SESSION:logs" \
    "cd '$PROJECT_ROOT' && tail -f logs/localcms_consumer.log" Enter

tmux select-window -t "$SESSION:consumer"
echo "$SESSION started (windows: consumer health logs)"
