#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="${BIN_DIR:-/usr/local/bin}"
install -d "$BIN_DIR"
ln -sf "$BASE_DIR/scripts/menu.sh" "$BIN_DIR/menu-model_provider_openclaw"
ln -sf "$BASE_DIR/scripts/cmd.sh" "$BIN_DIR/cmd-model_provider_openclaw"
ln -sf "$BASE_DIR/scripts/sanity.sh" "$BIN_DIR/sanity-model_provider_openclaw"
echo "Shortcuts installed in $BIN_DIR"
