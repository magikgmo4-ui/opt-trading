#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE_DIR/scripts/vision_runtime_cmd.sh"

while true; do
  cat <<'EOF'
=== VISION Runtime Pair ===
1) Sanity pair
2) Show paths
3) Status services/timers
4) Init shared dirs
5) Capture once (vision_bot)
6) Analyze latest (step2)
7) Send latest (step2)
8) Prune old (step2)
9) Show journals
q) Quit
EOF
  read -r -p "> " choice
  case "$choice" in
    1) bash "$CMD" sanity ;;
    2) bash "$CMD" paths ;;
    3) bash "$CMD" status ;;
    4) bash "$CMD" init ;;
    5) bash "$CMD" capture-once ;;
    6) bash "$CMD" analyze-latest ;;
    7) bash "$CMD" send-latest ;;
    8) bash "$CMD" prune-old ;;
    9) bash "$CMD" tail ;;
    q|Q) exit 0 ;;
    *) echo "Unknown choice" ;;
  esac
  echo
done
