#!/usr/bin/env bash
set -euo pipefail

while true; do
  echo
  echo "=== Git Sync All ==="
  echo "1) Run sync (report)"
  echo "2) Show last report path"
  echo "3) Show git status"
  echo "4) Show last 10 commits"
  echo "q) Quit"
  read -r -p "> " c
  case "$c" in
    1) cmd-git_sync_all ;;
    2) ls -1t /tmp/git_sync_all/sync_*.txt 2>/dev/null | head -n 1 || echo "No reports yet" ;;
    3) (cd /opt/trading && git status) ;;
    4) (cd /opt/trading && git --no-pager log --oneline -10) ;;
    q) exit 0 ;;
    *) echo "Invalid" ;;
  esac
done
