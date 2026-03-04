#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/marketdata/scripts/menu.sh" "$BIN/menu-marketdata"
sudo ln -sf "$ROOT/modules/marketdata/scripts/cmd.sh" "$BIN/cmd-marketdata"
sudo ln -sf "$ROOT/modules/marketdata/scripts/sanity_check.sh" "$BIN/sanity-marketdata"
echo "OK: installed shortcuts for marketdata"
ls -l "$BIN/menu-marketdata" "$BIN/cmd-marketdata" "$BIN/sanity-marketdata"
