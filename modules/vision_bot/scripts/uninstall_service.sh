#!/usr/bin/env bash
set -euo pipefail

echo "=== uninstall vision_bot systemd service ==="
date -Is || true

UNIT_DST="/etc/systemd/system/vision_bot.service"

systemctl stop vision_bot.service 2>/dev/null || true
systemctl disable vision_bot.service 2>/dev/null || true

if [[ -f "$UNIT_DST" ]]; then
  rm -f "$UNIT_DST"
  echo "OK: removed $UNIT_DST"
else
  echo "WARN: unit not found: $UNIT_DST"
fi

systemctl daemon-reload
echo "OK: uninstalled."
