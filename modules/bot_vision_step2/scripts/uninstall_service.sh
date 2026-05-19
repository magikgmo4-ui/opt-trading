#!/usr/bin/env bash
set -euo pipefail
echo "=== uninstall bot_vision_step2 ==="
date -Is || true

sudo systemctl stop bot_vision_step2 2>/dev/null || true
sudo systemctl disable bot_vision_step2 2>/dev/null || true
sudo systemctl stop bot_vision_step2_send.timer 2>/dev/null || true
sudo systemctl disable bot_vision_step2_send.timer 2>/dev/null || true
sudo systemctl stop bot_vision_step2_prune.timer 2>/dev/null || true
sudo systemctl disable bot_vision_step2_prune.timer 2>/dev/null || true

sudo rm -f /etc/systemd/system/bot_vision_step2.service            /etc/systemd/system/bot_vision_step2_send.service            /etc/systemd/system/bot_vision_step2_send.timer            /etc/systemd/system/bot_vision_step2_prune.service            /etc/systemd/system/bot_vision_step2_prune.timer

sudo systemctl daemon-reload
echo "OK."
