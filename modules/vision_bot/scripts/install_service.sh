#!/usr/bin/env bash
set -euo pipefail

echo "=== install vision_bot systemd service ==="
date -Is || true

REPO_ROOT="/opt/trading"
UNIT_SRC="$REPO_ROOT/modules/vision_bot/systemd/vision_bot.service"
UNIT_DST="/etc/systemd/system/vision_bot.service"

if [[ ! -f "$UNIT_SRC" ]]; then
  echo "ERR: unit file not found: $UNIT_SRC"
  exit 1
fi

# Ensure dirs exist (so service doesn't fail on first start)
INBOX="/srv/sftp/shared_files/shared/vision_inbox"
OUTBOX="/srv/sftp/shared_files/shared/vision_outbox"
PROCESSED="/srv/sftp/shared_files/shared/vision_processed"
WORKDIR="$REPO_ROOT/_work/vision_bot"
mkdir -p "$INBOX" "$OUTBOX" "$PROCESSED" "$WORKDIR"
chown -R ghost:ghost "$WORKDIR" || true

echo "[1] install unit -> $UNIT_DST"
cp -f "$UNIT_SRC" "$UNIT_DST"
chmod 0644 "$UNIT_DST"

echo "[2] systemd reload"
systemctl daemon-reload

echo "[3] enable + start"
systemctl enable --now vision_bot.service

echo "[4] status"
systemctl --no-pager --full status vision_bot.service | sed -n '1,20p' || true

echo
echo "OK: installed. Useful commands:"
echo "  systemctl status vision_bot --no-pager"
echo "  journalctl -u vision_bot -n 200 --no-pager"
echo "  systemctl restart vision_bot"
echo "  systemctl stop vision_bot"
