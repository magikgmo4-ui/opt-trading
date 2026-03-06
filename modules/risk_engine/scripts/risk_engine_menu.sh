#!/usr/bin/env bash
set -euo pipefail

# Ensure we can find the other scripts relative to this one or from root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

# Fallback to current dir if running from root
CMD_SCRIPT="./modules/risk_engine/scripts/risk_engine_cmd.sh"
SANITY_SCRIPT="./modules/risk_engine/scripts/risk_engine_sanity_check.sh"

while true; do
  echo
  echo "=== Risk Engine Menu ==="
  echo "1. Sanity Check"
  echo "2. Calculate Position Size"
  echo "3. Status"
  echo "q. Quit"
  echo
  read -r -p "Select > " choice

  case "$choice" in
    1) $SANITY_SCRIPT ;;
    2)
       read -r -p "Entry Price: " entry
       read -r -p "Stop Loss: " sl
       read -r -p "Balance: " bal
       $CMD_SCRIPT calc "$entry" "$sl" "$bal"
       ;;
    3) $CMD_SCRIPT status ;;
    q) exit 0 ;;
    *) echo "Invalid option" ;;
  esac
done
