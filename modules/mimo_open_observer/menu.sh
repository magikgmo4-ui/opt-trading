#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

while true; do
  echo ""
  echo "=== MIMO OPEN OBSERVER v0 ==="
  echo "1) Show docs index"
  echo "2) Detect once (fixture)"
  echo "3) Detect range (fixtures)"
  echo "4) Replay from CSV"
  echo "5) Sample pending"
  echo "6) Build stats"
  echo "7) Show stats"
  echo "8) Run sanity"
  echo "9) Exit"
  read -r -p "> " choice

  case "${choice:-9}" in
    1) cat "$SCRIPT_DIR/docs/00_SESSION_INDEX_MIMO_OPEN_OBSERVER_V0.txt" ;;
    2) bash "$SCRIPT_DIR/cmd.sh" detect_once ;;
    3) bash "$SCRIPT_DIR/cmd.sh" detect_range ;;
    4)
      read -r -p "CSV path (relative to module): " csv_path
      if [[ -n "$csv_path" ]]; then
        bash "$SCRIPT_DIR/cmd.sh" replay --csv "$csv_path"
      fi
      ;;
    5) bash "$SCRIPT_DIR/cmd.sh" sample_pending ;;
    6) bash "$SCRIPT_DIR/cmd.sh" build_stats ;;
    7) bash "$SCRIPT_DIR/cmd.sh" show_stats ;;
    8) bash "$SCRIPT_DIR/sanity.sh" ;;
    9) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
