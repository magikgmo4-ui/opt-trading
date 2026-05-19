#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

CMD_SCRIPT="./modules/engines/scripts/engines_cmd.sh"
SANITY_SCRIPT="./modules/engines/scripts/engines_sanity_check.sh"

while true; do
  echo
  echo "=== Engines Plugin Menu ==="
  echo "1. Sanity Check"
  echo "2. List Engines"
  echo "3. Test Echo Engine"
  echo "q. Quit"
  echo
  read -r -p "Select > " choice

  case "$choice" in
    1) $SANITY_SCRIPT ;;
    2) $CMD_SCRIPT list ;;
    3) $CMD_SCRIPT test ECHO_TEST ;;
    q) exit 0 ;;
    *) echo "Invalid option" ;;
  esac
done
