#!/usr/bin/env bash
# Stop all TMUX sessions — reverse order (critical last)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SESSIONS=(
    "localcms-ui"
    "kg-repo"
    "desk-pro"
    "apps-connectors"
    "market-data"
    "trading-pipeline"
    "strict-workers"
    "screeners"
    "openclaw-core"
)

echo "=== TMUX SPINE STOP ==="
for session in "${SESSIONS[@]}"; do
    if tmux has-session -t "$session" 2>/dev/null; then
        tmux kill-session -t "$session"
        echo "  stopped: $session"
    else
        echo "  already stopped: $session"
    fi
done
echo "=== DONE ==="
