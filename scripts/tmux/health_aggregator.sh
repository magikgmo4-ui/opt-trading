#!/usr/bin/env bash
# Health aggregator — runs every 60s, logs state, notifies Telegram if critical DOWN
# Usage: bash scripts/tmux/health_aggregator.sh [--once]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_FILE="$PROJECT_ROOT/logs/tmux_health.log"
INTERVAL="${TMUX_HEALTH_INTERVAL:-60}"
ONCE="${1:-}"

mkdir -p "$PROJECT_ROOT/logs"

_check_once() {
    local report
    report="$(python3 "$SCRIPT_DIR/health_check.py" 2>&1)"
    local ts
    ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "$ts $report" | tee -a "$LOG_FILE"

    # notify Telegram if critical DOWN
    local needs_alert
    needs_alert="$(echo "$report" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('1' if data.get('needs_alert') else '0')
except Exception:
    print('0')
")"
    if [ "$needs_alert" = "1" ]; then
        local critical_down
        critical_down="$(echo "$report" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(', '.join(data.get('critical_down', [])))
except Exception:
    print('unknown')
")"
        python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
try:
    from modules.notification_dispatcher.app.dispatcher import NotificationDispatcher
    from modules.notification_dispatcher.app.events import PipelineEvent
    d = NotificationDispatcher()
    e = PipelineEvent(
        event_type='pipeline_error',
        payload={'step': 'tmux_health_aggregator', 'error': 'CRITICAL sessions DOWN: $critical_down'},
    )
    d.dispatch(e, dry_run=False)
except Exception as exc:
    print(f'notification failed: {exc}', file=sys.stderr)
" 2>&1 | tee -a "$LOG_FILE"
    fi
}

if [ "$ONCE" = "--once" ]; then
    _check_once
else
    echo "health_aggregator started (interval=${INTERVAL}s) — log: $LOG_FILE"
    while true; do
        _check_once
        sleep "$INTERVAL"
    done
fi
