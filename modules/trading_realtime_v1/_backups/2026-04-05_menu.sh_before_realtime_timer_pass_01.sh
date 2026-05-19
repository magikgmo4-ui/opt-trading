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
  echo "8) bridge status"
  echo "9) bridge latest"
  echo "10) show last runtime event"
  echo "11) reporting status"
  echo "12) report runtime"
  echo "13) show last runtime report"
  echo "14) export status"
  echo "15) export last runtime report"
  echo "16) export runtime report"
  echo "17) runtime loop status"
  echo "18) runtime loop once"
  echo "19) show last runtime loop run"
  echo "20) guardrails status"
  echo "21) check guardrails"
  echo "22) show last guardrails report"
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
    8) "$CMD" bridge-status ;;
    9) "$CMD" bridge-latest ;;
    10) "$CMD" show-last-runtime-event ;;
    11) "$CMD" reporting-status ;;
    12) "$CMD" report-runtime ;;
    13) "$CMD" show-last-runtime-report ;;
    14) "$CMD" export-status ;;
    15) "$CMD" export-last-runtime-report ;;
    16) "$CMD" export-runtime-report ;;
    17) "$CMD" runtime-loop-status ;;
    18) "$CMD" runtime-loop-once ;;
    19) "$CMD" show-last-runtime-loop-run ;;
    20) "$CMD" guardrails-status ;;
    21) "$CMD" check-guardrails ;;
    22) "$CMD" show-last-guardrails-report ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
done
