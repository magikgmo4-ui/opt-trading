#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/scripts/reseau_fix"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$BASE" "$BASE/lib" "$BASE/templates/sshd_config.d" "$BASE/templates/hosts"
rsync -a --delete --exclude ".git" --exclude "*.zip" "$SRC_DIR/" "$BASE/"
chmod +x "$BASE/"*.sh 2>/dev/null || true
chmod +x "$BASE/lib/"*.sh 2>/dev/null || true
ln -sf "$BASE/reseau_fix_menu.sh" /usr/local/bin/menu-reseau_fix
ln -sf "$BASE/reseau_fix_cmd.sh"  /usr/local/bin/cmd-reseau_fix
ln -sf "$BASE/sanity_reseau_fix.sh" /usr/local/bin/sanity-reseau_fix
echo "OK: installed to $BASE"
echo "OK: shortcuts: menu-reseau_fix, cmd-reseau_fix, sanity-reseau_fix"
