#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/desk_pro/scripts/menu.sh" "$BIN/menu-desk_pro"
sudo ln -sf "$ROOT/modules/desk_pro/scripts/cmd.sh" "$BIN/cmd-desk_pro"
sudo ln -sf "$ROOT/modules/desk_pro/scripts/sanity_check.sh" "$BIN/sanity-desk_pro"
echo "OK: installed shortcuts for desk_pro"
ls -l "$BIN/menu-desk_pro" "$BIN/cmd-desk_pro" "$BIN/sanity-desk_pro"
