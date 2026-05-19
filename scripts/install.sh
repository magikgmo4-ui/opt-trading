#!/usr/bin/env bash
set -euo pipefail
echo "=== Install git_sync_all ==="
if [[ "${EUID}" -ne 0 ]]; then
  echo "Run with sudo:"
  echo "  sudo bash scripts/install.sh"
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="/opt/trading"

mkdir -p "$TARGET/scripts"
cp -a "$ROOT/scripts/"*.sh "$TARGET/scripts/"
chmod +x "$TARGET/scripts/"*.sh

ln -sf "$TARGET/scripts/git_sync_all.sh" /usr/local/bin/cmd-git_sync_all
ln -sf "$TARGET/scripts/git_sync_all_menu.sh" /usr/local/bin/menu-git_sync_all

echo "OK: cmd-git_sync_all + menu-git_sync_all installed"
