#!/usr/bin/env bash
# Restart a single TMUX session by name
# Usage: restart_session.sh <session_name>
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION="${1:-}"

if [ -z "$SESSION" ]; then
    echo "Usage: restart_session.sh <session_name>"
    echo "Sessions: openclaw-core screeners strict-workers trading-pipeline market-data apps-connectors desk-pro kg-repo localcms-ui"
    exit 1
fi

SESSION_SCRIPT="$SCRIPT_DIR/sessions/${SESSION}.sh"
if [ ! -f "$SESSION_SCRIPT" ]; then
    echo "ERROR: unknown session '$SESSION' (no script: $SESSION_SCRIPT)"
    exit 1
fi

# kil_v1 session guard — never auto-restart
if [ "$SESSION" = "trading-pipeline" ]; then
    echo "WARNING: trading-pipeline contains kil_v1 (safety device)."
    echo "  Restart manually after investigation, not automatically."
    read -r -p "Confirm restart trading-pipeline? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
fi

echo "Restarting session: $SESSION"
tmux kill-session -t "$SESSION" 2>/dev/null && echo "  killed" || echo "  was not running"
sleep 1
bash "$SESSION_SCRIPT"
echo "  restarted: $SESSION"
