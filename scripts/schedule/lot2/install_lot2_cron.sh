#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CRON_SNIPPET="$SCRIPT_DIR/lot2_crontab.txt"
MARKER="GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT2_01"

if [[ ! -f "$CRON_SNIPPET" ]]; then
    echo "ERROR: lot2_crontab.txt not found" >&2; exit 1
fi

if crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo "INFO: Lot 2 cron already installed. Run uninstall first to reinstall."
    exit 0
fi

mkdir -p /opt/trading/data/logs/cron
(crontab -l 2>/dev/null || true; cat "$CRON_SNIPPET") | crontab -

echo "OK: Lot 2 cron entries installed."
crontab -l | grep -v '^#' | grep -v '^$' | grep -v '^SHELL\|^REPO\|^PY\|^LOGDIR'
