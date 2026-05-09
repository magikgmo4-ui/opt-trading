#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$BASE_DIR/../.." && pwd)"

VISION_CMD="$BASE_DIR/scripts/vision_bot_cmd.sh"
VISION_SANITY="$BASE_DIR/scripts/vision_bot_sanity.sh"
STEP2_CMD="$REPO_ROOT/modules/bot_vision_step2/scripts/bot_vision_step2_cmd.sh"
STEP2_SANITY="$REPO_ROOT/modules/bot_vision_step2/scripts/bot_vision_step2_sanity.sh"

echo "=== sanity: unified VISION runtime pair ==="
date -Is || true

[[ -x "$VISION_CMD" ]] || { echo "ERR: missing $VISION_CMD"; exit 1; }
[[ -x "$STEP2_CMD" ]] || { echo "ERR: missing $STEP2_CMD"; exit 1; }
[[ -x "$VISION_SANITY" ]] || { echo "ERR: missing $VISION_SANITY"; exit 1; }
[[ -x "$STEP2_SANITY" ]] || { echo "ERR: missing $STEP2_SANITY"; exit 1; }

echo "[1/2] vision_bot sanity"
bash "$VISION_SANITY"

echo "[2/2] bot_vision_step2 sanity"
bash "$STEP2_SANITY"

echo "OK: unified pair sanity PASS"
