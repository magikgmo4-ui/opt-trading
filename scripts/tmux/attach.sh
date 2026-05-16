#!/usr/bin/env bash
# Attach to a TMUX session by name
# Usage: attach.sh [session_name]
#        attach.sh           → list active sessions
#        attach.sh <name>    → attach to session

SESSION="${1:-}"

if [ -z "$SESSION" ]; then
    echo "Active TMUX sessions:"
    tmux list-sessions 2>/dev/null || echo "  (no sessions running)"
    echo ""
    echo "Usage: attach.sh <session_name>"
    echo "Sessions: openclaw-core screeners strict-workers trading-pipeline market-data apps-connectors desk-pro kg-repo localcms-ui"
    exit 0
fi

if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "Session '$SESSION' not running."
    echo "Start it with: bash scripts/tmux/sessions/${SESSION}.sh"
    exit 1
fi

# Detect if inside TMUX already
if [ -n "$TMUX" ]; then
    tmux switch-client -t "$SESSION"
else
    tmux attach-session -t "$SESSION"
fi
