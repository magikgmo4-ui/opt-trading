#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== Vision Bot Menu ==="
echo "1) Sanity check"
echo "2) Init inbox/outbox dirs"
echo "3) Run once (process inbox)"
echo "4) Start watch (background)"
echo "5) Stop watch"
echo "6) Tail logs"
echo "q) Quit"
echo
read -rp "> " choice

case "$choice" in
  1) bash "$BASE_DIR/scripts/vision_bot_cmd.sh" sanity ;;
  2) bash "$BASE_DIR/scripts/vision_bot_cmd.sh" init ;;
  3) bash "$BASE_DIR/scripts/vision_bot_cmd.sh" run_once ;;
  4) bash "$BASE_DIR/scripts/vision_bot_cmd.sh" watch ;;
  5) bash "$BASE_DIR/scripts/vision_bot_cmd.sh" stop ;;
  6) bash "$BASE_DIR/scripts/vision_bot_cmd.sh" tail ;;
  q|Q) exit 0 ;;
  *) echo "Invalid choice" ;;
esac
