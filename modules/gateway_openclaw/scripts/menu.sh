#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  echo
  echo "=== gateway_openclaw ==="
  echo "1) sanity"
  echo "2) status"
  echo "3) start"
  echo "4) health"
  echo "5) probe"
  echo "6) logs"
  echo "7) attach"
  echo "8) stop"
  echo "9) paths"
  echo "0) quit"
  read -r -p "> " choice
  case "$choice" in
    1) "$CMD" sanity ;;
    2) "$CMD" status ;;
    3) "$CMD" start ;;
    4) "$CMD" health ;;
    5) "$CMD" probe ;;
    6) "$CMD" logs ;;
    7) "$CMD" attach ;;
    8) "$CMD" stop ;;
    9) "$CMD" paths ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
done
