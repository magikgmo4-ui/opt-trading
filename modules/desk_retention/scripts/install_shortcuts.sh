#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"

sudo ln -sf "$BASE/scripts/menu.sh" /usr/local/bin/menu-desk_retention
sudo ln -sf "$BASE/scripts/cmd.sh" /usr/local/bin/cmd-desk_retention
sudo ln -sf "$BASE/scripts/sanity_check.sh" /usr/local/bin/sanity-desk_retention

echo "OK: shortcuts installed"
ls -lah /usr/local/bin/*desk_retention | sed -n '1,60p'
