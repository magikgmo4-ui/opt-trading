#!/usr/bin/env bash
set -euo pipefail

SCRIPT="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT="$(readlink -f "$SCRIPT" 2>/dev/null || echo "$SCRIPT")"
fi
BASE="$(cd "$(dirname "$SCRIPT")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"
SANITY="$BASE/scripts/sanity_check.sh"

while true; do
  echo "=== desk_snapshot_ingest menu ==="
  echo "1) Sanity check"
  echo "2) Ingest once (scan inbox)"
  echo "3) Watch (poll inbox) 3s"
  echo "4) Show latest.json"
  echo "5) Tail history.jsonl"
  echo "6) Print config"
  echo "7) Install global shortcuts (sudo)"
  echo "q) Quit"
  echo
  read -r -p "> " choice
  case "$choice" in
    1) "$SANITY" ;;
    2) "$CMD" ingest_once ;;
    3) "$CMD" ingest_watch 3 ;;
    4) "$CMD" show_latest ;;
    5) "$CMD" tail_history ;;
    6) "$CMD" print_config ;;
    7) "$CMD" install_shortcuts ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
  echo
done
