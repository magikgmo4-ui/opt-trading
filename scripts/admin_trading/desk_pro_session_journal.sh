#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Session Journal
# Manages a simple session journal for operators
# Usage: ./desk_pro_session_journal.sh [show|add-entry] "optional text"

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$ROOT_DIR/data/logs/desk_pro"
mkdir -p "$LOGS_DIR"
JOURNAL_FILE="$LOGS_DIR/session_journal.log"

cmd="${1:-show}"

if [ "$cmd" == "show" ]; then
    echo "=== Desk Pro Session Journal ==="
    if [ -f "$JOURNAL_FILE" ]; then
        cat "$JOURNAL_FILE"
    else
        echo "(Journal is empty)"
    fi
    echo "================================"

elif [ "$cmd" == "add-entry" ]; then
    NOTE="${2:-User Note}"
    TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    USER_NAME=$(whoami)
    ENTRY="[$TIMESTAMP] [$USER_NAME] $NOTE"
    
    echo "$ENTRY" >> "$JOURNAL_FILE"
    echo "Entry added: $ENTRY"

else
    echo "Usage: $0 [show|add-entry \"text\"]"
    exit 1
fi
