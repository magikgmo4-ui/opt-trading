#!/usr/bin/env bash
set -euo pipefail
echo "=== install datasheet_writer shortcuts ==="
ROOT="/opt/trading"; BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/datasheet_writer/scripts/cmd.sh" "$BIN/cmd-datasheet_writer"
sudo ln -sf "$ROOT/modules/datasheet_writer/scripts/menu.sh" "$BIN/menu-datasheet_writer"
sudo ln -sf "$ROOT/modules/datasheet_writer/scripts/sanity.sh" "$BIN/sanity-datasheet_writer"
echo "OK"
