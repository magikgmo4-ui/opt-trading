#!/data/data/com.termux/files/usr/bin/bash
# Tasker-callable: list tmux sessions on fleet machines
set -Eeuo pipefail
for host in db-layer admin-trading fantome student; do
    echo "=== $host ==="
    ssh -o BatchMode=yes -o ConnectTimeout=5 "$host" "tmux list-sessions -F '#{session_name}' 2>/dev/null || echo '(no sessions)'"
done
