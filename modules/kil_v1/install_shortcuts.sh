#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

install_link() {
    local source_path="$1"
    local target_path="$2"
    ln -sfn "$source_path" "$target_path"
}

chmod +x "$SCRIPT_DIR/cmd.sh" "$SCRIPT_DIR/menu.sh" "$SCRIPT_DIR/sanity.sh"

install_link "$SCRIPT_DIR/cmd.sh" "/usr/local/bin/cmd-kil_v1"
install_link "$SCRIPT_DIR/menu.sh" "/usr/local/bin/menu-kil_v1"
install_link "$SCRIPT_DIR/sanity.sh" "/usr/local/bin/sanity-kil_v1"

echo "kil_v1 shortcuts installed"
