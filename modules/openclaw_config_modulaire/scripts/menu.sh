#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  echo
  echo "=== openclaw_config_modulaire ==="
  echo "1) sanity"
  echo "2) status"
  echo "3) apply safe"
  echo "4) validate"
  echo "5) health"
  echo "6) probe"
  echo "7) rollback latest"
  echo "8) paths"
  echo "0) quit"
  read -r -p "> " choice
  case "$choice" in
    1) "$CMD" sanity ;;
    2) "$CMD" status ;;
    3) "$CMD" apply ;;
    4) "$CMD" validate ;;
    5) "$CMD" health ;;
    6) "$CMD" probe ;;
    7) "$CMD" rollback ;;
    8) "$CMD" paths ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
done
