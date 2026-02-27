#!/usr/bin/env bash
set -euo pipefail

while true; do
  echo
  echo "=== Menu DeepSeek (Global) ==="
  echo "1) Sanity (thinking + response)"
  echo "2) THINKING: Run"
  echo "3) THINKING: Tail last 10"
  echo "4) RESPONSE: Run"
  echo "5) RESPONSE: Tail last 10"
  echo "q) Quit"
  read -r -p "> " c
  case "$c" in
    1) sanity-deepseek_thinking && sanity-deepseek_response ;;
    2)
      read -r -p "Model [deepseek-r1:1.5b]: " m; m="${m:-deepseek-r1:1.5b}"
      read -r -p "Sujet: " s
      cmd-deepseek_thinking run "$m" "$s"
      ;;
    3) cmd-deepseek_thinking tail _ 10 ;;
    4)
      read -r -p "Model [deepseek-r1:1.5b]: " m; m="${m:-deepseek-r1:1.5b}"
      read -r -p "Sujet: " s
      cmd-deepseek_response run "$m" "$s"
      ;;
    5) cmd-deepseek_response tail _ 10 ;;
    q) exit 0 ;;
    *) echo "Invalid" ;;
  esac
done
