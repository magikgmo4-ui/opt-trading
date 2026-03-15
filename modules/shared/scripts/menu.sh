#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT_PATH="$(readlink -f "$SCRIPT_PATH" 2>/dev/null || echo "$SCRIPT_PATH")"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  echo "== shared (menu)"
  echo "1) ls (root)"
  echo "2) status"
  echo "3) path"
  echo "0) exit"
  printf "> "
  read -r choice
  case "$choice" in
    1) bash "$CMD" ls ;;
    2) bash "$CMD" status ;;
    3) bash "$CMD" path ;;
    0) exit 0 ;;
    *) echo "Unknown choice: $choice" ;;
  esac
  echo
done

