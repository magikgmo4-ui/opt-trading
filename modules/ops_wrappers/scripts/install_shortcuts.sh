#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/ops_wrappers/scripts/menu.sh" "$BIN/menu-ops_wrappers"
sudo ln -sf "$ROOT/modules/ops_wrappers/scripts/cmd.sh" "$BIN/cmd-ops_wrappers"
sudo ln -sf "$ROOT/modules/ops_wrappers/scripts/sanity_check.sh" "$BIN/sanity-ops_wrappers"
echo "OK: shortcuts installed"
ls -l "$BIN/menu-ops_wrappers" "$BIN/cmd-ops_wrappers" "$BIN/sanity-ops_wrappers"
