#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$ROOT/scripts/simex_cmd.sh"

while true; do
  printf '\n=== SIMEX MENU ===\n'
  printf '1) Status\n'
  printf '2) Perf start\n'
  printf '3) Perf stop\n'
  printf '4) Perf logs\n'
  printf '5) Bitget run\n'
  printf '6) Smoke\n'
  printf '7) Sanity\n'
  printf 'q) Quit\n'
  read -r -p 'Choice: ' c
  case "$c" in
    1) "$CMD" status ;;
    2) "$CMD" perf-start ;;
    3) "$CMD" perf-stop ;;
    4) "$CMD" perf-logs ;;
    5) "$CMD" bitget-run ;;
    6) "$CMD" smoke ;;
    7) "$CMD" sanity ;;
    q|Q) exit 0 ;;
    *) printf 'Unknown choice\n' ;;
  esac
done
