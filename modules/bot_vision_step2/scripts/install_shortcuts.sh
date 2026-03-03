#!/usr/bin/env bash
set -euo pipefail
echo "=== install bot_vision_step2 shortcuts ==="
date -Is || true
ROOT="/opt/trading"
BIN="/usr/local/bin"

sudo ln -sf "$ROOT/modules/bot_vision_step2/scripts/bot_vision_step2_cmd.sh" "$BIN/cmd-bot_vision_step2"
sudo ln -sf "$ROOT/modules/bot_vision_step2/scripts/bot_vision_step2_menu.sh" "$BIN/menu-bot_vision_step2"
sudo ln -sf "$ROOT/modules/bot_vision_step2/scripts/bot_vision_step2_sanity.sh" "$BIN/sanity-bot_vision_step2"
echo "OK: shortcuts installed."
