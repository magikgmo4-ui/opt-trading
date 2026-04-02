#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE_DIR/scripts/cmd.sh"

while true; do
  cat <<MENU
=== model_provider_openclaw ===
1) status
2) sanity
3) show orchestrateur
4) show builder
5) show reviewer
6) show lab
7) export json
0) quit
MENU
  read -r -p "> " choice
  case "$choice" in
    1) bash "$CMD" status ;;
    2) bash "$CMD" sanity ;;
    3) bash "$CMD" show-agent orchestrateur ;;
    4) bash "$CMD" show-agent builder ;;
    5) bash "$CMD" show-agent reviewer ;;
    6) bash "$CMD" show-agent lab ;;
    7) bash "$CMD" export-json ;;
    0) exit 0 ;;
    *) echo "Choix invalide." ;;
  esac
  echo
done
