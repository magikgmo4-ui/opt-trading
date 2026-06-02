#!/usr/bin/env bash
set -euo pipefail
MARKER="GO_OPENCLAW_DBLAYER_WORKERS_CHILD_CLOSEOUT_LOT2B_LOT3_01_LOT3"
SNIPPET="$(cd "$(dirname "$0")" && pwd)/lot3_crontab.txt"
if crontab -l 2>/dev/null | grep -q "$MARKER"; then echo "INFO: already installed."; exit 0; fi
mkdir -p /opt/trading/data/logs/cron
(crontab -l 2>/dev/null || true; echo "# $MARKER"; cat "$SNIPPET") | crontab -
echo "OK: Lot 3 installed."; crontab -l | grep -c '^\*\|^[0-9]'
