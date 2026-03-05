#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/winscp_transfer/scripts/menu.sh" "$BIN/menu-winscp_transfer"
sudo ln -sf "$ROOT/modules/winscp_transfer/scripts/cmd.sh" "$BIN/cmd-winscp_transfer"
sudo ln -sf "$ROOT/modules/winscp_transfer/scripts/sanity_check.sh" "$BIN/sanity-winscp_transfer"
echo "OK: installed shortcuts for winscp_transfer"
ls -l "$BIN/menu-winscp_transfer" "$BIN/cmd-winscp_transfer" "$BIN/sanity-winscp_transfer"
