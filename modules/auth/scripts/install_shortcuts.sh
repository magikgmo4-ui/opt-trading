#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/auth/scripts/menu.sh" "$BIN/menu-auth"
sudo ln -sf "$ROOT/modules/auth/scripts/cmd.sh" "$BIN/cmd-auth"
sudo ln -sf "$ROOT/modules/auth/scripts/sanity_check.sh" "$BIN/sanity-auth"
echo "OK: installed shortcuts for auth"
ls -l "$BIN/menu-auth" "$BIN/cmd-auth" "$BIN/sanity-auth"
