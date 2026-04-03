#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  echo
  echo "=== install_module_openclaw ==="
  echo "1) sanity"
  echo "2) list modules"
  echo "3) status"
  echo "4) install openclaw_config_modulaire"
  echo "5) paths"
  echo "0) quit"
  read -r -p "> " choice
  case "$choice" in
    1) "$CMD" sanity ;;
    2) "$CMD" list ;;
    3) "$CMD" status ;;
    4) "$CMD" install openclaw_config_modulaire ;;
    5) "$CMD" paths ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
done
