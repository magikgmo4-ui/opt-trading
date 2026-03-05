#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/opt/trading}"
BASE="$ROOT/modules/install_module/scripts"

ln -sf "$BASE/menu.sh" /usr/local/bin/menu-install_module
ln -sf "$BASE/cmd.sh"  /usr/local/bin/cmd-install_module
ln -sf "$BASE/sanity_check.sh" /usr/local/bin/sanity-install_module

echo "OK: shortcuts installed"
ls -lah /usr/local/bin/menu-install_module /usr/local/bin/cmd-install_module /usr/local/bin/sanity-install_module
