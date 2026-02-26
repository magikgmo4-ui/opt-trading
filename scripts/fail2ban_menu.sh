#!/usr/bin/env bash
set -euo pipefail

CMD="/opt/trading/scripts/fail2ban_cmd.sh"

while true; do
  echo
  echo "=== Fail2Ban Menu ==="
  echo "1) Status"
  echo "2) Restart + Sanity"
  echo "3) Logs"
  echo "4) Show bans (sshd)"
  echo "5) Unban IP"
  echo "q) Quit"
  read -r -p "> " choice

  case "$choice" in
    1) "$CMD" status ;;
    2) "$CMD" restart ;;
    3) "$CMD" logs ;;
    4) "$CMD" bans ;;
    5)
      read -r -p "IP to unban: " ip
      "$CMD" unban "$ip"
      ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
