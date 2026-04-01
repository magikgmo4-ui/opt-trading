#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/engines/scripts/menu.sh" "$BIN/menu-engines"
sudo ln -sf "$ROOT/modules/engines/scripts/cmd.sh" "$BIN/cmd-engines"
sudo ln -sf "$ROOT/modules/engines/scripts/sanity_check.sh" "$BIN/sanity-engines"
echo "OK: installed shortcuts for engines"
ls -l "$BIN/menu-engines" "$BIN/cmd-engines" "$BIN/sanity-engines"
