#!/usr/bin/env bash
set -euo pipefail
echo "=== install analysis_bundles shortcuts ==="
date -Is || true
ROOT="/opt/trading"
BIN="/usr/local/bin"

sudo ln -sf "$ROOT/modules/analysis_bundles/scripts/cmd.sh" "$BIN/cmd-analysis_bundles"
sudo ln -sf "$ROOT/modules/analysis_bundles/scripts/menu.sh" "$BIN/menu-analysis_bundles"
sudo ln -sf "$ROOT/modules/analysis_bundles/scripts/sanity_check.sh" "$BIN/sanity-analysis_bundles"
echo "OK: shortcuts installed for analysis_bundles."
