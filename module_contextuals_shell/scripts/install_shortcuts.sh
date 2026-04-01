#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/module_contextuals_shell/scripts/menu.sh" "$BIN/menu-module_contextuals_shell"
sudo ln -sf "$ROOT/modules/module_contextuals_shell/scripts/cmd.sh" "$BIN/cmd-module_contextuals_shell"
sudo ln -sf "$ROOT/modules/module_contextuals_shell/scripts/sanity_check.sh" "$BIN/sanity-module_contextuals_shell"
echo "OK: installed shortcuts for module_contextuals_shell"
ls -l "$BIN/menu-module_contextuals_shell" "$BIN/cmd-module_contextuals_shell" "$BIN/sanity-module_contextuals_shell"
