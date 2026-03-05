#!/usr/bin/env bash
set -euo pipefail

SCRIPT="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT="$(readlink -f "$SCRIPT" 2>/dev/null || echo "$SCRIPT")"
fi
BASE="$(cd "$(dirname "$SCRIPT")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"
SANITY="$BASE/scripts/sanity_check.sh"

while true; do
  echo "=== desk_analyze menu ==="
  echo "1) Sanity check"
  echo "2) Preview /analyze (text)"
  echo "3) Preview /analyze (json)"
  echo "4) Send /analyze to Telegram (needs env)"
  echo "5) Print config"
  echo "6) Install global shortcuts (sudo)"
  echo "q) Quit"
  echo
  read -r -p "> " choice
  case "$choice" in
    1) "$SANITY" ;;
    2) "$CMD" preview ;;
    3) "$CMD" preview_json ;;
    4) "$CMD" send ;;
    5) "$CMD" print_config ;;
    6) "$CMD" install_shortcuts ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
  echo
done
