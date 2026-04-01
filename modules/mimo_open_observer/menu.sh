#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

while true; do
  echo ""
  echo "=== MIMO OPEN OBSERVER v0 ==="
  echo "1) Show docs index"
  echo "2) Check market window"
  echo "3) Detect once (fixture)"
  echo "4) Detect range (fixtures)"
  echo "5) Replay from CSV"
  echo "6) Sample pending"
  echo "7) Build stats"
  echo "8) Show stats"
  echo "9) Run sanity"
  echo "0) Exit"
  read -r -p "> " choice

  case "${choice:-0}" in
    1) cat "$SCRIPT_DIR/docs/00_SESSION_INDEX_MIMO_OPEN_OBSERVER_V0.txt" ;;
    2) bash "$SCRIPT_DIR/cmd.sh" check_window ;;
    3) bash "$SCRIPT_DIR/cmd.sh" detect_once ;;
    4) bash "$SCRIPT_DIR/cmd.sh" detect_range ;;
    5)
      read -r -p "CSV path (relative to module): " csv_path
      if [[ -n "$csv_path" ]]; then
        bash "$SCRIPT_DIR/cmd.sh" replay --csv "$csv_path"
      fi
      ;;
    6) bash "$SCRIPT_DIR/cmd.sh" sample_pending ;;
    7) bash "$SCRIPT_DIR/cmd.sh" build_stats ;;
    8) bash "$SCRIPT_DIR/cmd.sh" show_stats ;;
    9) bash "$SCRIPT_DIR/sanity.sh" ;;
    0) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
