#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

echo "mimo_open_observer :: doc pack v0"
echo "1) show docs index"
echo "2) run sanity"
echo "3) exit"
read -r -p "> " choice

case "${choice:-3}" in
  1) echo "$SCRIPT_DIR/docs/00_SESSION_INDEX_MIMO_OPEN_OBSERVER_V0.txt" ;;
  2) bash "$SCRIPT_DIR/sanity.sh" ;;
  *) exit 0 ;;
esac
