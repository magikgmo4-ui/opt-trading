#!/usr/bin/env bash
set -euo pipefail

MODULE="shared_sshfs_permanent"
LOG_DIR="/opt/trading/journal/tmp"
mkdir -p "$LOG_DIR"
TS="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$LOG_DIR/${MODULE}_menu_${TS}.log"

run() {
  # run cmd and tee output
  echo "[$(date -Is)] $*" | tee -a "$LOG_FILE"
  bash -lc "$*" 2>&1 | tee -a "$LOG_FILE"
  echo | tee -a "$LOG_FILE" >/dev/null
}

header() {
  echo "=== $MODULE menu ==="
  echo "log: $LOG_FILE"
  echo
}

while true; do
  header
  echo "1) Status"
  echo "2) Mount (start service)"
  echo "3) Umount (stop service)"
  echo "4) Restart"
  echo "5) Logs (last 200)"
  echo "6) Edit config"
  echo "7) Test SSH"
  echo "8) List /shared (top)"
  echo "9) Quit"
  echo
  read -r -p "Choose: " choice
  case "${choice:-}" in
    1) run "cmd-$MODULE status" ;;
    2) run "cmd-$MODULE mount" ;;
    3) run "cmd-$MODULE umount" ;;
    4) run "cmd-$MODULE restart" ;;
    5) run "cmd-$MODULE logs" ;;
    6) run "cmd-$MODULE edit-config" ;;
    7) run "cmd-$MODULE test-ssh" ;;
    8) run "cmd-$MODULE ls" ;;
    9) echo "Bye."; exit 0 ;;
    *) echo "Invalid." ;;
  esac
done
