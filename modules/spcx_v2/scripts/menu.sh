#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "========================================"
echo "  SPCX V2 — Paper Runner Menu"
echo "========================================"
echo ""
echo "  1) Run once (detect + log)"
echo "  2) Watch mode (continuous)"
echo "  3) Replay from file"
echo "  4) Show summary"
echo "  5) Sanity check"
echo "  6) Install shortcuts"
echo "  0) Exit"
echo ""
read -rp "Choice: " choice

case "$choice" in
  1) bash "$MODULE_DIR/scripts/cmd.sh" once ;;
  2) bash "$MODULE_DIR/scripts/cmd.sh" watch ;;
  3) read -rp "JSONL file path: " f; bash "$MODULE_DIR/scripts/cmd.sh" replay "$f" ;;
  4) bash "$MODULE_DIR/scripts/cmd.sh" summary ;;
  5) bash "$MODULE_DIR/scripts/cmd.sh" sanity ;;
  6) bash "$MODULE_DIR/scripts/cmd.sh" install ;;
  0) exit 0 ;;
  *) echo "Invalid choice" ;;
esac
