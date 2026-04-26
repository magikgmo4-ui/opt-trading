#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd -P)"
CANONICAL_INSTALL="$ROOT_DIR/modules/reseau_ssh/scripts/install_canonical_shortcuts.sh"

if [ -x "$CANONICAL_INSTALL" ]; then
  echo "INFO: scripts/reseau_ssh/install_reseau_ssh.sh is deprecated."
  echo "INFO: delegating short-alias installation to canonical module reseau_ssh."
  exec bash "$CANONICAL_INSTALL"
fi

BASE="/opt/trading/scripts/reseau_ssh"
SRC_DIR="$SCRIPT_DIR"

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
echo "WARN: canonical installer missing; legacy shortcuts kept on scripts/reseau_ssh"
