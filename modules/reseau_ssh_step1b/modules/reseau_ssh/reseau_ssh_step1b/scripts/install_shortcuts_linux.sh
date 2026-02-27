\
#!/usr/bin/env bash
set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_SCRIPTS="/opt/trading/scripts"
sudo mkdir -p "$TARGET_SCRIPTS"

sudo cp -a "$MODULE_DIR/scripts/reseau_ssh_menu.sh" "$TARGET_SCRIPTS/reseau_ssh_menu.sh"
sudo cp -a "$MODULE_DIR/scripts/reseau_ssh_cmd.sh"  "$TARGET_SCRIPTS/reseau_ssh_cmd.sh"
sudo cp -a "$MODULE_DIR/scripts/sanity_check.sh"    "$TARGET_SCRIPTS/sanity_reseau_ssh.sh"
sudo chmod +x "$TARGET_SCRIPTS/reseau_ssh_menu.sh" "$TARGET_SCRIPTS/reseau_ssh_cmd.sh" "$TARGET_SCRIPTS/sanity_reseau_ssh.sh"

sudo ln -sf "$TARGET_SCRIPTS/reseau_ssh_menu.sh" /usr/local/bin/menu-reseau_ssh
sudo ln -sf "$TARGET_SCRIPTS/reseau_ssh_cmd.sh"  /usr/local/bin/cmd-reseau_ssh
sudo ln -sf "$TARGET_SCRIPTS/sanity_reseau_ssh.sh" /usr/local/bin/sanity-reseau_ssh

echo "OK: shortcuts installed"
