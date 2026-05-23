#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

install_wrapper() {
  local name="$1"
  local target="$2"
  cat > "/usr/local/bin/$name" <<EOF
#!/usr/bin/env bash
exec bash "$target" "\$@"
EOF
  chmod +x "/usr/local/bin/$name"
  echo "Installed: /usr/local/bin/$name"
}

install_wrapper "data_center_init"   "$SCRIPT_DIR/cmd.sh"
install_wrapper "data_center_menu"   "$SCRIPT_DIR/menu.sh"
install_wrapper "data_center_check"  "$SCRIPT_DIR/sanity_check.sh"

echo "Shortcuts installed."
