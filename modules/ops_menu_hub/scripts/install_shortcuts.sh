#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
sudo ln -sf "$BASE/scripts/menu.sh" /usr/local/bin/menu-ops_menu_hub
sudo ln -sf "$BASE/scripts/cmd.sh" /usr/local/bin/cmd-ops_menu_hub
sudo ln -sf "$BASE/scripts/sanity_check.sh" /usr/local/bin/sanity-ops_menu_hub
echo "OK: canonical shortcuts installed"
ls -lah /usr/local/bin/*ops_menu_hub | sed -n '1,60p'
