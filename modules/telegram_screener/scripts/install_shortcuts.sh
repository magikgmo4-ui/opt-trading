#!/usr/bin/env bash
set -euo pipefail
MOD="${0%/*}/.."
MOD="$(cd "$MOD" && pwd -P)"
ln -sf "$MOD/scripts/cmd.sh" /usr/local/bin/cmd-telegram_screener
ln -sf "$MOD/scripts/menu.sh" /usr/local/bin/menu-telegram_screener
ln -sf "$MOD/scripts/sanity_check.sh" /usr/local/bin/sanity-telegram_screener
echo "installed telegram_screener shortcuts"
