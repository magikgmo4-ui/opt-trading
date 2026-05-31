#!/usr/bin/env bash
# uninstall_systemd.sh
# Remove systemd service and timer for bot-vision-headless-capture and bot-vision-orchestrator.
set -euo pipefail

echo "Uninstalling bot-vision systemd units..."

# Stop + disable all timers/services
sudo systemctl disable --now bot-vision-orchestrator.timer 2>/dev/null || true
sudo systemctl disable --now bot-vision-headless-capture.timer 2>/dev/null || true
sudo systemctl stop bot-vision-orchestrator.service 2>/dev/null || true
sudo systemctl stop bot-vision-headless-capture.service 2>/dev/null || true

# Remove unit files
sudo rm -f /etc/systemd/system/bot-vision-headless-capture.service
sudo rm -f /etc/systemd/system/bot-vision-headless-capture.timer
sudo rm -f /etc/systemd/system/bot-vision-orchestrator.service
sudo rm -f /etc/systemd/system/bot-vision-orchestrator.timer

sudo systemctl daemon-reload

echo "Units removed. All timers disabled and stopped."
