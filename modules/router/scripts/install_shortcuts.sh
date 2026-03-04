#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/router/scripts/menu.sh" "$BIN/menu-router"
sudo ln -sf "$ROOT/modules/router/scripts/cmd.sh" "$BIN/cmd-router"
sudo ln -sf "$ROOT/modules/router/scripts/sanity_check.sh" "$BIN/sanity-router"
echo "OK: installed shortcuts for router"
ls -l "$BIN/menu-router" "$BIN/cmd-router" "$BIN/sanity-router"
