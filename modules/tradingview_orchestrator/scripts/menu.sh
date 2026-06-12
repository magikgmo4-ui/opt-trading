#!/usr/bin/env bash
set -euo pipefail

MOD="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MOD/scripts/cmd.sh"

while true; do
  echo ""
  echo "=== TradingView Orchestrator ==="
  echo "  1) Snapshot (full read)"
  echo "  2) Alert list"
  echo "  3) Screenshot"
  echo "  4) Run job packet (read)"
  echo "  5) Run job packet (write — gate required)"
  echo "  6) Generate job packet template"
  echo "  7) Sanity check"
  echo "  q) Quit"
  echo ""
  read -rp "Choice: " choice
  case "$choice" in
    1) bash "$CMD" snapshot ;;
    2) bash "$CMD" alert-list ;;
    3) bash "$CMD" screenshot ;;
    4) read -rp "Packet path: " p; bash "$CMD" run "$p" ;;
    5) read -rp "Packet path: " p; bash "$CMD" run "$p" --gate-approved ;;
    6) read -rp "Job type: " t; bash "$CMD" new "$t" ;;
    7) bash "$CMD" sanity ;;
    q|Q) exit 0 ;;
    *) echo "Unknown choice" ;;
  esac
done
