#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/bot_vision/scripts/menu.sh" "$BIN/menu-bot_vision"
sudo ln -sf "$ROOT/modules/bot_vision/scripts/cmd.sh" "$BIN/cmd-bot_vision"
sudo ln -sf "$ROOT/modules/bot_vision/scripts/sanity_check.sh" "$BIN/sanity-bot_vision"
echo "OK: installed shortcuts for bot_vision"
ls -l "$BIN/menu-bot_vision" "$BIN/cmd-bot_vision" "$BIN/sanity-bot_vision"
