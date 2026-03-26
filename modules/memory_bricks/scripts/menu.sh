#!/usr/bin/env bash
set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="${MODULE_DIR}/scripts/cmd.sh"

echo "== memory_bricks menu =="
echo "1) Create demo brick"
echo "2) List bricks"
echo "3) Rebuild index"
echo "4) Run sanity"
read -rp "Choice: " choice

case "${choice}" in
  1)
    "${CMD}" new --type resume_point --title "Demo brick" --ia chatgpt --machine admin-trading --surface terminal_linux --project opt-trading --module memory_bricks --status open --summary-short "Demo brick for bootstrap." --resume-point "Inspect generated file."
    ;;
  2)
    "${CMD}" list
    ;;
  3)
    "${CMD}" index rebuild
    ;;
  4)
    "${MODULE_DIR}/scripts/sanity_check.sh"
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac
