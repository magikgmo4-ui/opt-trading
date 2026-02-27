#!/usr/bin/env bash
set -euo pipefail

while true; do
  echo
  echo "=== Menu DeepSeek RESPONSE (student) ==="
  echo "1) Sanity"
  echo "2) Run response (ask a subject)"
  echo "3) Tail last 10 response files"
  echo "q) Quit"
  read -r -p "> " c
  case "$c" in
    1) sanity-deepseek_response ;;
    2)
      read -r -p "Model [deepseek-r1:1.5b]: " m; m="${m:-deepseek-r1:1.5b}"
      read -r -p "Sujet: " s
      cmd-deepseek_response run "$m" "$s"
      ;;
    3) cmd-deepseek_response tail _ 10 ;;
    q) exit 0 ;;
    *) echo "Invalid" ;;
  esac
done
