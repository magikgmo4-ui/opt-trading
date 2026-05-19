#!/usr/bin/env bash
set -euo pipefail

# Install global shortcuts (symlinks) in /usr/local/bin
# Requires sudo.
#
# Usage:
#   sudo ./scripts/install_workflow_ai_shortcuts.sh

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="/usr/local/bin"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing: $1"; exit 1; }; }
need ln
need chmod

echo "[install] ROOT=$ROOT"
echo "[install] BIN=$BIN"

sudo ln -sf "$ROOT/scripts/workflow_ai_menu.sh" "$BIN/menu-workflow_ai"
sudo ln -sf "$ROOT/scripts/workflow_ai_cmd.sh" "$BIN/cmd-workflow_ai"
sudo ln -sf "$ROOT/scripts/workflow_ai_sanity_check.sh" "$BIN/sanity-workflow_ai"

echo "OK: $BIN/menu-workflow_ai"
echo "OK: $BIN/cmd-workflow_ai"
echo "OK: $BIN/sanity-workflow_ai"
