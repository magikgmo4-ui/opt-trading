#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  echo
  echo "=== trading_realtime_v1 ==="
  echo "1) sanity"
  echo "2) status"
  echo "3) show profile"
  echo "4) show schemas"
  echo "5) show live source"
  echo "6) observe once"
  echo "7) runtime status"
  echo "0) quit"
  printf "choice: "
  read -r choice
  case "$choice" in
    1) "$CMD" sanity ;;
    2) "$CMD" status ;;
    3) "$CMD" show-profile ;;
    4) "$CMD" show-schemas ;;
    5) "$CMD" show-live-source ;;
    6) "$CMD" observe-once ;;
    7) "$CMD" runtime-status ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
done
