#!/usr/bin/env bash
# uninstall_bot_vision_headless_systemd.sh
# Remove systemd service and timer for bot_vision_headless.
set -euo pipefail

echo "Uninstalling bot-vision-headless-capture systemd units..."

sudo systemctl disable --now bot-vision-headless-capture.timer 2>/dev/null || true
sudo systemctl stop bot-vision-headless-capture.service 2>/dev/null || true

sudo rm -f /etc/systemd/system/bot-vision-headless-capture.service
sudo rm -f /etc/systemd/system/bot-vision-headless-capture.timer

sudo systemctl daemon-reload

echo "Units removed. Timer disabled and stopped."
