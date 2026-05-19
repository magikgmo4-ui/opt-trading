#!/usr/bin/env bash
set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="${BIN_DIR:-/usr/local/bin}"

install_link() {
  local src="$1"
  local dest="$2"
  sudo mkdir -p "$BIN_DIR"
  sudo ln -sf "$src" "$BIN_DIR/$dest"
}

chmod +x "$MODULE_DIR/scripts/"*.sh
install_link "$MODULE_DIR/scripts/deploy_module_multi_machine_cmd.sh"   cmd-deploy_module_multi_machine
install_link "$MODULE_DIR/scripts/deploy_module_multi_machine_menu.sh"  menu-deploy_module_multi_machine
install_link "$MODULE_DIR/scripts/deploy_module_multi_machine_sanity_check.sh" sanity-deploy_module_multi_machine

echo "Installé :"
echo "- $BIN_DIR/cmd-deploy_module_multi_machine"
echo "- $BIN_DIR/menu-deploy_module_multi_machine"
echo "- $BIN_DIR/sanity-deploy_module_multi_machine"
