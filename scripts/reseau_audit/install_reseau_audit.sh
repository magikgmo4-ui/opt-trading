#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/scripts/reseau_audit"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$BASE" "$BASE/lib" "$BASE/windows"
rsync -a --delete --exclude ".git" --exclude "*.zip" "$SRC_DIR/" "$BASE/"
chmod +x "$BASE/"*.sh 2>/dev/null || true
chmod +x "$BASE/windows/"*.ps1 2>/dev/null || true
ln -sf "$BASE/reseau_audit_menu.sh" /usr/local/bin/menu-reseau_audit
ln -sf "$BASE/reseau_audit_cmd.sh"  /usr/local/bin/cmd-reseau_audit
ln -sf "$BASE/sanity_reseau_audit.sh" /usr/local/bin/sanity-reseau_audit
echo "OK: installed to $BASE"
echo "OK: shortcuts: menu-reseau_audit, cmd-reseau_audit, sanity-reseau_audit"
