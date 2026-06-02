#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
MODULE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
LOG_FILE="$MODULE_DIR/logs/menu_$(date -u +%Y%m%dT%H%M%SZ).log"

mkdir -p "$MODULE_DIR/logs"

run_and_log() {
  "$SCRIPT_DIR/cmd.sh" "$@" 2>&1 | tee -a "$LOG_FILE"
}

while true; do
  cat <<'EOF'

collector_telegram menu
1) sanity
2) run enabled channels (limit 100)
3) run coinglass_alerts (limit 5)
4) status
5) test
0) exit
EOF
  read -r -p "Choose an action: " choice
  case "$choice" in
    1) run_and_log sanity ;;
    2) run_and_log run --limit 100 ;;
    3) run_and_log run --channel coinglass_alerts --limit 5 ;;
    4) run_and_log status ;;
    5) run_and_log test ;;
    0) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
