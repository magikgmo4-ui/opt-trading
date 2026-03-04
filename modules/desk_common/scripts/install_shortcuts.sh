#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/desk_common/scripts/menu.sh" "$BIN/menu-desk_common"
sudo ln -sf "$ROOT/modules/desk_common/scripts/cmd.sh" "$BIN/cmd-desk_common"
sudo ln -sf "$ROOT/modules/desk_common/scripts/sanity_check.sh" "$BIN/sanity-desk_common"
echo "OK: installed shortcuts for desk_common"
ls -l "$BIN/menu-desk_common" "$BIN/cmd-desk_common" "$BIN/sanity-desk_common"
