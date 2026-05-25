#!/usr/bin/env bash
set -euo pipefail
echo "=== install result_tracker shortcuts ==="
date -Is || true
ROOT="/opt/trading"
BIN="/usr/local/bin"

sudo ln -sf "$ROOT/modules/result_tracker/scripts/cmd.sh" "$BIN/cmd-result_tracker"
sudo ln -sf "$ROOT/modules/result_tracker/scripts/menu.sh" "$BIN/menu-result_tracker"
sudo ln -sf "$ROOT/modules/result_tracker/scripts/sanity.sh" "$BIN/sanity-result_tracker"
echo "OK: shortcuts installed for result_tracker."
