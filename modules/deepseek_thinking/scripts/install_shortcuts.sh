#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/deepseek_thinking/scripts/menu.sh" "$BIN/menu-deepseek_thinking"
sudo ln -sf "$ROOT/modules/deepseek_thinking/scripts/cmd.sh" "$BIN/cmd-deepseek_thinking"
sudo ln -sf "$ROOT/modules/deepseek_thinking/scripts/sanity_check.sh" "$BIN/sanity-deepseek_thinking"
echo "OK: installed shortcuts for deepseek_thinking"
ls -l "$BIN/menu-deepseek_thinking" "$BIN/cmd-deepseek_thinking" "$BIN/sanity-deepseek_thinking"
