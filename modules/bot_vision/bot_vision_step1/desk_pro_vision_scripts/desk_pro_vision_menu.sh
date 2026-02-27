#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/desk_pro_vision_cmd.sh"
SANITY="$SCRIPT_DIR/sanity_desk_pro_vision.sh"

while true; do
  cat <<'MENU'
=== Desk Pro Vision Menu (Step 1) ===
1) Run placeholder vision (new run)
2) Show latest
3) Print summary.json
4) Tail logs
5) Sanity check
q) Quit
MENU
  read -r -p "> " choice
  case "$choice" in
    1) "$CMD" run ;;
    2) "$CMD" latest ;;
    3) "$CMD" summary ;;
    4) read -r -p "Lines (default 50): " n; "$CMD" log "${n:-50}" ;;
    5) "$SANITY" ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
