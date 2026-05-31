#!/usr/bin/env bash
# install_systemd.sh
# Install systemd service + timer for bot-vision-headless-capture and bot-vision-orchestrator.
set -euo pipefail

ROOT="${ROOT:-/opt/trading}"
SRC="$ROOT/modules/bot_vision/headless_capture/systemd"
DST="/etc/systemd/system"

echo "Installing bot-vision systemd units..."

# Capture (oneshot — standalone headless capture)
sudo install -m 0644 "$SRC/bot-vision-headless-capture.service" "$DST/bot-vision-headless-capture.service"
sudo install -m 0644 "$SRC/bot-vision-headless-capture.timer" "$DST/bot-vision-headless-capture.timer"

# Orchestrator (full pipeline — capture → analyze → validate → filter → dispatch)
sudo install -m 0644 "$SRC/bot-vision-orchestrator.service" "$DST/bot-vision-orchestrator.service"
sudo install -m 0644 "$SRC/bot-vision-orchestrator.timer" "$DST/bot-vision-orchestrator.timer"

sudo systemctl daemon-reload

echo "Units installed."
echo "To enable orchestrator (full A-08/A-09 pipeline):"
echo "  sudo systemctl enable --now bot-vision-orchestrator.timer"
echo ""
echo "To enable standalone capture only:"
echo "  sudo systemctl enable --now bot-vision-headless-capture.timer"
echo ""
echo "To test once:"
echo "  sudo systemctl start bot-vision-orchestrator.service"
