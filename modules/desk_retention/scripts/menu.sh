#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  echo
  echo "=== desk_retention menu ==="
  echo "1) Print config"
  echo "2) Dry run"
  echo "3) Prune now"
  echo "4) Install timer (10 min)"
  echo "5) Status timer"
  echo "6) Uninstall timer"
  echo "q) Quit"
  read -r -p "> " ans
  case "$ans" in
    1) bash "$CMD" print_config || true ;;
    2) bash "$CMD" dry_run ;;
    3) bash "$CMD" prune_now ;;
    4) bash "$CMD" install_timer ;;
    5) bash "$CMD" status_timer ;;
    6) bash "$CMD" uninstall_timer ;;
    q|Q) exit 0 ;;
    *) echo "?" ;;
  esac
done
