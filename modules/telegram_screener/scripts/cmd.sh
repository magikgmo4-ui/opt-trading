#!/usr/bin/env bash
set -euo pipefail
MOD="${0%/*}/.."
MOD="$(cd "$MOD" && pwd -P)"
NAME="$(basename "$MOD")"

cmd="${1:-info}"
case "$cmd" in
  info)
    echo "name=$NAME"
    echo "path=$MOD"
    ;;
  readme)
    echo "telegram_screener runtime consumer module"
    ;;
  menu)
    exec bash "$MOD/scripts/menu.sh"
    ;;
  *)
    echo "Usage: cmd-$NAME info|readme|menu"
    exit 1
    ;;
esac
