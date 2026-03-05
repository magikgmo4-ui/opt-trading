#!/usr/bin/env bash
set -euo pipefail

# Resolve real path even when launched via /usr/local/bin symlink
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  echo
  echo "=== OPS HUB menu ==="
  echo "1) List modules + host hints"
  echo "2) List shortcuts"
  echo "3) Bootstrap shortcuts (sudo)"
  echo "4) Run a module menu"
  echo "q) Quit"
  read -r -p "> " ans
  case "$ans" in
    1) bash "$CMD" list ;;
    2) bash "$CMD" shortcuts ;;
    3) bash "$CMD" bootstrap_shortcuts ;;
    4)
      read -r -p "module name (ex: desk_state): " m
      bash "$CMD" run "$m" || true
      ;;
    q|Q) exit 0 ;;
    *) echo "?" ;;
  esac
done
