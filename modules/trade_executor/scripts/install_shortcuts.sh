#!/usr/bin/env bash
set -euo pipefail
echo "=== install trade_executor shortcuts ==="
date -Is || true
ROOT="/opt/trading"
BIN="/usr/local/bin"

sudo ln -sf "$ROOT/modules/trade_executor/scripts/cmd.sh" "$BIN/cmd-trade_executor"
sudo ln -sf "$ROOT/modules/trade_executor/scripts/menu.sh" "$BIN/menu-trade_executor"
sudo ln -sf "$ROOT/modules/trade_executor/scripts/sanity.sh" "$BIN/sanity-trade_executor"
echo "OK: shortcuts installed for trade_executor."
