#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  echo
  echo "=== trading_lab_v1 ==="
  echo "1) sanity"
  echo "2) status"
  echo "3) show profile"
  echo "4) show schemas"
  echo "5) sample event"
  echo "6) sample trade"
  echo "7) materialize samples"
  echo "0) quit"
  read -r -p "> " choice
  case "$choice" in
    1) "$CMD" sanity ;;
    2) "$CMD" status ;;
    3) "$CMD" show-profile ;;
    4) "$CMD" show-schemas ;;
    5) "$CMD" sample-event ;;
    6) "$CMD" sample-trade ;;
    7) "$CMD" materialize-samples ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
done
