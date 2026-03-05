#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  echo
  echo "=== desk_state menu ==="
  echo "1) Build once"
  echo "2) Print latest (head)"
  echo "3) Print schema summary"
  echo "4) Print config"
  echo "q) Quit"
  read -r -p "> " ans
  case "$ans" in
    1) bash "$CMD" build_once ;;
    2) bash "$CMD" print_latest ;;
    3) bash "$CMD" print_schema ;;
    4) bash "$CMD" print_config || true ;;
    q|Q) exit 0 ;;
    *) echo "?" ;;
  esac
done
