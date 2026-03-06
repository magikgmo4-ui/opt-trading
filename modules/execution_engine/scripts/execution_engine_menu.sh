#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

CMD_SCRIPT="./modules/execution_engine/scripts/execution_engine_cmd.sh"
SANITY_SCRIPT="./modules/execution_engine/scripts/execution_engine_sanity_check.sh"

while true; do
  echo
  echo "=== Execution Engine Menu ==="
  echo "1. Sanity Check"
  echo "2. Run Paper Execution Test"
  echo "q. Quit"
  echo
  read -r -p "Select > " choice

  case "$choice" in
    1) $SANITY_SCRIPT ;;
    2) $CMD_SCRIPT test_paper ;;
    q) exit 0 ;;
    *) echo "Invalid option" ;;
  esac
done
