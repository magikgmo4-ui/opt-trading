#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE_DIR/scripts/vision_bot_cmd.sh"
SANITY="$BASE_DIR/scripts/vision_bot_sanity.sh"
MENU="$BASE_DIR/scripts/vision_bot_menu.sh"
PAIR_CMD="$BASE_DIR/scripts/vision_runtime_cmd.sh"
PAIR_SANITY="$BASE_DIR/scripts/vision_runtime_sanity.sh"
PAIR_MENU="$BASE_DIR/scripts/vision_runtime_menu.sh"

sudo ln -sf "$CMD" /usr/local/bin/cmd-vision_bot
sudo ln -sf "$SANITY" /usr/local/bin/sanity-vision_bot
sudo ln -sf "$MENU" /usr/local/bin/menu-vision_bot
sudo ln -sf "$PAIR_CMD" /usr/local/bin/cmd-vision
sudo ln -sf "$PAIR_SANITY" /usr/local/bin/sanity-vision
sudo ln -sf "$PAIR_MENU" /usr/local/bin/menu-vision

echo "OK: installed shortcuts:"
ls -lah /usr/local/bin/{cmd-vision_bot,sanity-vision_bot,menu-vision_bot,cmd-vision,sanity-vision,menu-vision}
