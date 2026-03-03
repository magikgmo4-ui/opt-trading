#!/usr/bin/env bash
set -euo pipefail
while true; do
  echo "=== bot_vision_step2 menu ==="
  echo "1) Sanity"
  echo "2) Analyze latest (CLI)"
  echo "3) Send latest to Telegram (requires TELEGRAM_CHAT_ID)"
  echo "4) Prune old (processed/outbox)"
  echo "5) Service status"
  echo "6) Tail logs"
  echo "q) Quit"
  echo
  read -rp "> " c
  case "$c" in
    1) /usr/local/bin/cmd-bot_vision_step2 sanity ;;
    2) /usr/local/bin/cmd-bot_vision_step2 analyze_latest ;;
    3) /usr/local/bin/cmd-bot_vision_step2 send_latest ;;
    4) /usr/local/bin/cmd-bot_vision_step2 prune_old ;;
    5) /usr/local/bin/cmd-bot_vision_step2 status ;;
    6) /usr/local/bin/cmd-bot_vision_step2 tail ;;
    q|Q) exit 0 ;;
    *) echo "Invalid." ;;
  esac
  echo
done
