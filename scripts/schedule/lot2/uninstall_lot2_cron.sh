#!/usr/bin/env bash
set -euo pipefail

MARKER="GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT2_01"

if ! crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo "INFO: Lot 2 cron not found. Nothing to remove."
    exit 0
fi

tmp=$(mktemp)
crontab -l 2>/dev/null | awk "/$MARKER/{found=1} !found{print}" > "$tmp"
crontab "$tmp"
rm -f "$tmp"
echo "OK: Lot 2 cron entries removed."
