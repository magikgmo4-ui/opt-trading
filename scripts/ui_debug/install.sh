#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MOD_DIR="/opt/trading/scripts/ui_debug"

echo "[ui_debug] installing to: $MOD_DIR"
sudo mkdir -p "$MOD_DIR"
sudo cp -a "$SRC_DIR/"* "$MOD_DIR/"

sudo chmod +x \
  "$MOD_DIR/ui_menu.sh" \
  "$MOD_DIR/ui_cmd.sh" \
  "$MOD_DIR/sanity_ui_debug.sh" \
  "$MOD_DIR/ui_diag.sh" || true

# wrappers in /usr/local/bin
wrap () {
  local name="$1"
  local target="$2"
  sudo tee "/usr/local/bin/$name" >/dev/null <<EOF
#!/usr/bin/env bash
exec bash "$target" "\$@"
EOF
  sudo chmod +x "/usr/local/bin/$name"
}

wrap "menu-ui_debug" "$MOD_DIR/ui_menu.sh"
wrap "cmd-ui_debug" "$MOD_DIR/ui_cmd.sh"
wrap "sanity-ui_debug" "$MOD_DIR/sanity_ui_debug.sh"

echo "[ui_debug] OK: installed shortcuts: menu-ui_debug, cmd-ui_debug, sanity-ui_debug"
