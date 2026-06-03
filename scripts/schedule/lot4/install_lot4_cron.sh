#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CRON_SNIPPET="$SCRIPT_DIR/lot4_crontab.txt"
MARKER="GO_TELEGRAM_SIGNALS_CAPTURE_EXPANSION_CHILD_01_CRON_01"

if [[ ! -f "$CRON_SNIPPET" ]]; then
    echo "ERROR: lot4_crontab.txt not found at $CRON_SNIPPET" >&2
    exit 1
fi

if crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo "INFO: Lot 4 cron already installed (marker found). Run uninstall first to reinstall."
    exit 0
fi

mkdir -p /home/fantome/opt-trading-clean/data/logs/cron

(crontab -l 2>/dev/null || true; cat "$CRON_SNIPPET") | crontab -

echo "OK: Lot 4 cron entries installed."
echo ""
crontab -l | grep -v '^#' | grep -v '^$' | grep -v '^SHELL\|^REPO\|^LOGDIR'
