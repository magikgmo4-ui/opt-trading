#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/audit/scripts/menu.sh" "$BIN/menu-audit"
sudo ln -sf "$ROOT/modules/audit/scripts/cmd.sh" "$BIN/cmd-audit"
sudo ln -sf "$ROOT/modules/audit/scripts/sanity_check.sh" "$BIN/sanity-audit"
echo "OK: installed shortcuts for audit"
ls -l "$BIN/menu-audit" "$BIN/cmd-audit" "$BIN/sanity-audit"
