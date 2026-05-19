#!/usr/bin/env bash
set -euo pipefail

SERVICE_DST="/etc/systemd/system/daily-session.service"
TIMER_DST="/etc/systemd/system/daily-session.timer"

if [[ $EUID -ne 0 ]]; then
    echo "ERROR: must run as root (sudo)" >&2
    exit 1
fi

echo "Stopping and disabling timer..."
systemctl stop daily-session.timer 2>/dev/null || true
systemctl disable daily-session.timer 2>/dev/null || true

echo "Removing service and timer files..."
rm -f "$SERVICE_DST" "$TIMER_DST"

systemctl daemon-reload

echo "OK: daily-session service/timer uninstalled."
