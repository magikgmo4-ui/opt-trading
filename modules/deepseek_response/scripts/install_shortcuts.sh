#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/deepseek_response/scripts/menu.sh" "$BIN/menu-deepseek_response"
sudo ln -sf "$ROOT/modules/deepseek_response/scripts/cmd.sh" "$BIN/cmd-deepseek_response"
sudo ln -sf "$ROOT/modules/deepseek_response/scripts/sanity_check.sh" "$BIN/sanity-deepseek_response"
echo "OK: installed shortcuts for deepseek_response"
ls -l "$BIN/menu-deepseek_response" "$BIN/cmd-deepseek_response" "$BIN/sanity-deepseek_response"
