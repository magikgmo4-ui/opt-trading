#!/usr/bin/env bash
set -euo pipefail

echo "=== Timer status ==="
systemctl list-timers --all 2>/dev/null | grep daily-session || echo "(not found)"

echo ""
echo "=== Service status ==="
systemctl status daily-session.service 2>/dev/null || echo "(not found)"

echo ""
echo "=== Last service logs (journalctl) ==="
journalctl -u daily-session.service --no-pager -n 30 2>/dev/null || echo "(not found)"

echo ""
echo "=== Scheduler logs ==="
SCHEDULER_LOG="/opt/trading/data/logs/scheduler/scheduler.log"
if [[ -f "$SCHEDULER_LOG" ]]; then
    tail -5 "$SCHEDULER_LOG"
else
    echo "(no scheduler log)"
fi

echo ""
echo "=== Latest journal file ==="
LATEST=$(ls -t /opt/trading/data/journal/daily/*.json 2>/dev/null | head -1)
if [[ -n "$LATEST" ]]; then
    echo "File: $LATEST"
    python3 -c "
import json
d = json.load(open('$LATEST'))
print(f'  run_id: {d.get(\"run_id\")}')
print(f'  all_ok: {d.get(\"all_ok\")}')
print(f'  verdict: {d.get(\"validation_verdict\")}')
print(f'  outcome: {d.get(\"result_tracker_outcome\")}')
print(f'  pnl: {d.get(\"pnl_paper\", {}).get(\"net_pnl\")}')
" 2>/dev/null || echo "(parse error)"
else
    echo "(no journal files)"
fi
