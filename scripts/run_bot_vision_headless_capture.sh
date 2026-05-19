#!/usr/bin/env bash
# run_bot_vision_headless_capture.sh
# Wrapper for headless capture — called by systemd timer.
set -euo pipefail

MODULE_DIR="/opt/trading/modules/bot_vision/headless_capture"
PROFILE="${PROFILE:-$MODULE_DIR/profiles.example.json}"
OUT_DIR="${OUT_DIR:-/srv/sftp/shared_files/shared/vision_inbox}"

cd "$MODULE_DIR"

export BOT_VISION_OUT="$OUT_DIR"

exec /usr/bin/node "$MODULE_DIR/capture_headless.js" \
  --profile "$PROFILE" \
  --once
