#!/usr/bin/env bash
set -euo pipefail

BASE="/opt/trading/scripts/reseau_ssh"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$BASE"
mkdir -p "$BASE/templates" "$BASE/windows" "$BASE/journal" "$BASE/lib"

# copy all module files (except git-irrelevant)
rsync -a --delete \
  --exclude ".git" \
  --exclude "*.zip" \
  "$SRC_DIR/" "$BASE/"

chmod +x "$BASE/"*.sh || true
chmod +x "$BASE/windows/"*.ps1 2>/dev/null || true

# global shortcuts
ln -sf "$BASE/reseau_ssh_menu.sh" /usr/local/bin/menu-reseau_ssh
ln -sf "$BASE/reseau_ssh_cmd.sh"  /usr/local/bin/cmd-reseau_ssh
ln -sf "$BASE/sanity_reseau_ssh.sh" /usr/local/bin/sanity-reseau_ssh

echo "OK: installed to $BASE"
echo "OK: shortcuts: menu-reseau_ssh, cmd-reseau_ssh, sanity-reseau_ssh"
