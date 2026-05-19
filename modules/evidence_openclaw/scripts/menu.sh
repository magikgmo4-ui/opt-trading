#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  echo
  echo "=== evidence_openclaw ==="
  echo "1) sanity"
  echo "2) detect workspace"
  echo "3) status"
  echo "4) export docs evidence"
  echo "5) print doc prompt"
  echo "6) show evidence files"
  echo "0) quit"
  read -r -p "> " choice
  case "$choice" in
    1) "$CMD" sanity ;;
    2) "$CMD" detect-workspace ;;
    3) "$CMD" status ;;
    4) "$CMD" export-docs ;;
    5) "$CMD" print-doc-prompt ;;
    6) "$CMD" show-files ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
done
