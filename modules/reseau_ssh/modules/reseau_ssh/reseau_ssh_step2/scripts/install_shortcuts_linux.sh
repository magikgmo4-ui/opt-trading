#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE_DIR/scripts/reseau_ssh_cmd.sh"
MENU="$BASE_DIR/scripts/reseau_ssh_menu.sh"
SANITY="$BASE_DIR/scripts/sanity_check.sh"
sudo ln -sf "$CMD" /usr/local/bin/cmd-reseau_ssh_step2
sudo ln -sf "$MENU" /usr/local/bin/menu-reseau_ssh_step2
sudo ln -sf "$SANITY" /usr/local/bin/sanity-reseau_ssh_step2
echo "OK: installed shortcuts: cmd-reseau_ssh_step2, menu-reseau_ssh_step2, sanity-reseau_ssh_step2"
