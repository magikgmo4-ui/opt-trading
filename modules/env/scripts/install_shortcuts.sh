#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/env/scripts/menu.sh" "$BIN/menu-env"
sudo ln -sf "$ROOT/modules/env/scripts/cmd.sh" "$BIN/cmd-env"
sudo ln -sf "$ROOT/modules/env/scripts/sanity_check.sh" "$BIN/sanity-env"
echo "OK: installed shortcuts for env"
ls -l "$BIN/menu-env" "$BIN/cmd-env" "$BIN/sanity-env"
