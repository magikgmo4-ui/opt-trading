#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MARKER="GO_TELEGRAM_SIGNALS_CAPTURE_EXPANSION_CHILD_01_CRON_01"

if ! crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo "INFO: Lot 4 cron not installed."
    exit 0
fi

crontab -l 2>/dev/null | sed "/$MARKER/,/^$/d" | crontab -

echo "OK: Lot 4 cron entries removed."
