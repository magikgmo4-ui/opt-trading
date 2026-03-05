#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/scripts/scripts/menu.sh" "$BIN/menu-scripts"
sudo ln -sf "$ROOT/modules/scripts/scripts/cmd.sh" "$BIN/cmd-scripts"
sudo ln -sf "$ROOT/modules/scripts/scripts/sanity_check.sh" "$BIN/sanity-scripts"
echo "OK: installed shortcuts for scripts"
ls -l "$BIN/menu-scripts" "$BIN/cmd-scripts" "$BIN/sanity-scripts"
