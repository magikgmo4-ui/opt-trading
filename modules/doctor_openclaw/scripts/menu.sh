#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"
while true; do
  echo
  echo "=== doctor_openclaw ==="
  echo "1) sanity"
  echo "2) quick check"
  echo "3) deep check"
  echo "4) repair safe"
  echo "5) generate token"
  echo "6) validate"
  echo "7) health"
  echo "8) probe"
  echo "9) logs"
  echo "10) status"
  echo "11) dashboard"
  echo "0) quit"
  read -r -p "> " choice
  case "$choice" in
    1) "$CMD" sanity ;;
    2) "$CMD" quick ;;
    3) "$CMD" deep ;;
    4) "$CMD" repair-safe ;;
    5) "$CMD" generate-token ;;
    6) "$CMD" validate ;;
    7) "$CMD" health ;;
    8) "$CMD" probe ;;
    9) "$CMD" logs ;;
    10) "$CMD" status ;;
    11) "$CMD" dashboard ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
done
