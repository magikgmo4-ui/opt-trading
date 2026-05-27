#!/usr/bin/env bash
set -euo pipefail
echo "=== install learning_feeder shortcuts ==="
ROOT="/opt/trading"; BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/learning_feeder/scripts/cmd.sh" "$BIN/cmd-learning_feeder"
sudo ln -sf "$ROOT/modules/learning_feeder/scripts/menu.sh" "$BIN/menu-learning_feeder"
sudo ln -sf "$ROOT/modules/learning_feeder/scripts/sanity.sh" "$BIN/sanity-learning_feeder"
echo "OK"
