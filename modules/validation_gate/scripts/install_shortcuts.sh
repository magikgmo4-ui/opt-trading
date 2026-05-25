#!/usr/bin/env bash
set -euo pipefail
echo "=== install validation_gate shortcuts ==="
date -Is || true
ROOT="/opt/trading"
BIN="/usr/local/bin"

sudo ln -sf "$ROOT/modules/validation_gate/scripts/cmd.sh" "$BIN/cmd-validation_gate"
sudo ln -sf "$ROOT/modules/validation_gate/scripts/menu.sh" "$BIN/menu-validation_gate"
sudo ln -sf "$ROOT/modules/validation_gate/scripts/sanity.sh" "$BIN/sanity-validation_gate"
echo "OK: shortcuts installed for validation_gate."
