#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
MODULE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
LOG_FILE="$MODULE_DIR/logs/menu_$(date -u +%Y%m%dT%H%M%SZ).log"

run_and_log() {
  "$SCRIPT_DIR/collector_coingecko_cmd.sh" "$1" 2>&1 | tee -a "$LOG_FILE"
}

while true; do
  cat <<'EOF'

collector_coingecko menu
1) sanity
2) run oneshot
3) status
4) test
0) exit
EOF
  read -r -p "Choose an action: " choice
  case "$choice" in
    1) run_and_log sanity ;;
    2) run_and_log run ;;
    3) run_and_log status ;;
    4) run_and_log test ;;
    0) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
