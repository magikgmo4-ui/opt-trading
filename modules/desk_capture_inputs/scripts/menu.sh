#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/modules/desk_capture_inputs"
CMD="$BASE/scripts/cmd.sh"

echo "=== Desk Capture Inputs (Step D) ==="
echo "1) Sanity check"
echo "2) Extract once (OpenAI Vision -> JSON)"
echo "3) Print latest"
echo "4) Print config"
echo "q) Quit"
read -r -p "> " choice
case "$choice" in
  1) "$BASE/scripts/sanity_check.sh" ;;
  2) "$CMD" extract_once ;;
  3) "$CMD" print_latest ;;
  4) "$CMD" print_config ;;
  q|Q) exit 0 ;;
  *) echo "?" ;;
esac
