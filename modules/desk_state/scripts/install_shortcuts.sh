#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
sudo ln -sf "$BASE/scripts/menu.sh" /usr/local/bin/menu-desk_state
sudo ln -sf "$BASE/scripts/cmd.sh" /usr/local/bin/cmd-desk_state
sudo ln -sf "$BASE/scripts/sanity_check.sh" /usr/local/bin/sanity-desk_state
echo "OK: shortcuts installed"
ls -lah /usr/local/bin/*desk_state | sed -n '1,60p'
