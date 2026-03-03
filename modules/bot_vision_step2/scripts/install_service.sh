#!/usr/bin/env bash
set -euo pipefail
echo "=== install bot_vision_step2 service ==="
date -Is || true

ROOT="/opt/trading"
MOD="$ROOT/modules/bot_vision_step2"
ENV="$MOD/config/bot_vision.env"

if [[ ! -f "$ENV" ]]; then
  echo "ERR: missing config: $ENV"
  echo "Create it from: $MOD/config/bot_vision.env.example"
  exit 2
fi

VENV="$ROOT/.venvs/bot_vision_step2"
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "[1] create venv: $VENV"
  python3 -m venv "$VENV"
fi

echo "[2] install deps (openai + pillow)"
"$VENV/bin/python" -m pip install -U pip
"$VENV/bin/python" -m pip install -U openai pillow

echo "[3] shortcuts"
bash "$MOD/scripts/install_shortcuts.sh"

echo "[4] install systemd units"
sudo cp -f "$MOD/systemd/bot_vision_step2.service" /etc/systemd/system/bot_vision_step2.service
sudo cp -f "$MOD/systemd/bot_vision_step2_send.service" /etc/systemd/system/bot_vision_step2_send.service
sudo cp -f "$MOD/systemd/bot_vision_step2_send.timer" /etc/systemd/system/bot_vision_step2_send.timer
sudo cp -f "$MOD/systemd/bot_vision_step2_prune.service" /etc/systemd/system/bot_vision_step2_prune.service
sudo cp -f "$MOD/systemd/bot_vision_step2_prune.timer" /etc/systemd/system/bot_vision_step2_prune.timer

sudo chmod 0644 /etc/systemd/system/bot_vision_step2*.service /etc/systemd/system/bot_vision_step2*.timer

sudo systemctl daemon-reload

echo "[5] enable prune timer (safe)"
ENABLE_PRUNE="$(grep -E '^ENABLE_PRUNE_TIMER=' "$ENV" | tail -n 1 | cut -d= -f2- | tr -d ' ' || true)"
if [[ "${ENABLE_PRUNE:-1}" == "1" ]]; then
  sudo systemctl enable --now bot_vision_step2_prune.timer
else
  echo "PRUNE timer disabled."
fi

echo "[6] NOTE: Telegram service is NOT started automatically to avoid conflicting with your Windows NSSM bot."
echo "    Start it only after you stop the Windows bot (same token), or use a new token."
echo "    Commands:"
echo "      sudo systemctl enable --now bot_vision_step2"
echo "      sudo systemctl status bot_vision_step2 --no-pager"

echo "[7] Sender timer is optional (10-min posting from admin-trading)."
echo "    Enable only if ENABLE_SENDER_TIMER=1 and TELEGRAM_CHAT_ID is set."
