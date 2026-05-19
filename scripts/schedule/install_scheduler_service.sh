#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_SRC="$SRC_DIR/daily-session.service"
TIMER_SRC="$SRC_DIR/daily-session.timer"
SERVICE_DST="/etc/systemd/system/daily-session.service"
TIMER_DST="/etc/systemd/system/daily-session.timer"

if [[ $EUID -ne 0 ]]; then
    echo "ERROR: must run as root (sudo)" >&2
    exit 1
fi

if [[ ! -f "$SERVICE_SRC" ]]; then echo "ERROR: $SERVICE_SRC not found" >&2; exit 1; fi
if [[ ! -f "$TIMER_SRC" ]];   then echo "ERROR: $TIMER_SRC not found" >&2;   exit 1; fi

cp "$SERVICE_SRC" "$SERVICE_DST"
cp "$TIMER_SRC" "$TIMER_DST"
chmod 644 "$SERVICE_DST" "$TIMER_DST"

systemctl daemon-reload
systemctl enable daily-session.timer
systemctl start daily-session.timer

echo "OK: daily-session.timer installed, enabled, and started."
systemctl list-timers --all | grep daily-session || true
