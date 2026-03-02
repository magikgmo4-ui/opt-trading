#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE_DIR/scripts/vision_bot_cmd.sh"
SANITY="$BASE_DIR/scripts/vision_bot_sanity.sh"
MENU="$BASE_DIR/scripts/vision_bot_menu.sh"

sudo ln -sf "$CMD" /usr/local/bin/cmd-vision_bot
sudo ln -sf "$SANITY" /usr/local/bin/sanity-vision_bot
sudo ln -sf "$MENU" /usr/local/bin/menu-vision_bot

echo "OK: installed shortcuts:"
ls -lah /usr/local/bin/{cmd-vision_bot,sanity-vision_bot,menu-vision_bot}
