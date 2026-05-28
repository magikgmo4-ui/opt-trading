#!/data/data/com.termux/files/usr/bin/bash
# Tasker-callable: print SSH + tmux attach command for a session
# Usage: attach_hint.sh <host> <session>
set -Eeuo pipefail
HOST="${1:-}"
SESSION="${2:-}"
if [ -z "$HOST" ] || [ -z "$SESSION" ]; then
    echo "Usage: attach_hint.sh <host> <session>"
    echo "  ex: attach_hint.sh db-layer openclaw-core"
    exit 2
fi
echo "ssh $HOST -t 'tmux attach -t $SESSION || tmux ls'"
echo "Detach: Ctrl+b then d"
