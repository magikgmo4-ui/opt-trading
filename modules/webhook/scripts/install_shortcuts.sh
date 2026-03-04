#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/webhook/scripts/menu.sh" "$BIN/menu-webhook"
sudo ln -sf "$ROOT/modules/webhook/scripts/cmd.sh" "$BIN/cmd-webhook"
sudo ln -sf "$ROOT/modules/webhook/scripts/sanity_check.sh" "$BIN/sanity-webhook"
echo "OK: installed shortcuts for webhook"
ls -l "$BIN/menu-webhook" "$BIN/cmd-webhook" "$BIN/sanity-webhook"
