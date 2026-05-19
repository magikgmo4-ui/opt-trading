#!/usr/bin/env bash
# install_bot_vision_headless_systemd.sh
# Install systemd service and timer for bot_vision_headless.
set -euo pipefail

ROOT="${ROOT:-/opt/trading}"
SRC="$ROOT/modules/bot_vision/headless_capture/systemd"
DST="/etc/systemd/system"

echo "Installing bot-vision-headless-capture systemd units..."

sudo install -m 0644 "$SRC/bot-vision-headless-capture.service" "$DST/bot-vision-headless-capture.service"
sudo install -m 0644 "$SRC/bot-vision-headless-capture.timer" "$DST/bot-vision-headless-capture.timer"

sudo systemctl daemon-reload

echo "Units installed. To activate timer:"
echo "  sudo systemctl enable --now bot-vision-headless-capture.timer"
echo "To test once:"
echo "  sudo systemctl start bot-vision-headless-capture.service"
