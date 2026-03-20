#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"

install_link() {
  local src="$1"
  local dst="$2"
  if [ -w /usr/local/bin ]; then
    ln -sf "$src" "$dst"
  else
    sudo ln -sf "$src" "$dst"
  fi
}

install_link "$SCRIPT_DIR/cmd.sh" /usr/local/bin/cmd-git_fleet_guard
install_link "$SCRIPT_DIR/menu.sh" /usr/local/bin/menu-git_fleet_guard
install_link "$SCRIPT_DIR/sanity_check.sh" /usr/local/bin/sanity-git_fleet_guard

echo "Installé :"
echo "- /usr/local/bin/cmd-git_fleet_guard"
echo "- /usr/local/bin/menu-git_fleet_guard"
echo "- /usr/local/bin/sanity-git_fleet_guard"
