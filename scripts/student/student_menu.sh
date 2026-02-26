#!/usr/bin/env bash
set -euo pipefail
CMD="/opt/trading/scripts/student/student_cmd.sh"

ask() { local v; printf "%s" "$1" > /dev/tty; IFS= read -r v < /dev/tty; echo "$v"; }
pause() { printf "\n[DONE] Enter=menu | q=quit: " > /dev/tty; IFS= read -r x < /dev/tty; [[ "${x:-}" =~ ^[qQ]$ ]] && exit 0; }

while true; do
  echo
  echo "=== Student Menu ==="
  echo "1) Student sanity check"
  echo "2) SSH status"
  echo "3) Fail2Ban status (sshd)"
  echo "4) Fail2Ban logs"
  echo "5) Fail2Ban restart + sanity"
  echo "6) Recidive status"
  echo "7) Recidive bans"
  echo "8) Recidive unban IP"
  echo "q) Quit"
  echo

  choice="$(ask "> ")"
  case "$choice" in
    1) echo "[RUNNING] sanity"; "$CMD" sanity; pause ;;
    2) echo "[RUNNING] ssh-status"; "$CMD" ssh-status; pause ;;
    3) echo "[RUNNING] fail2ban-status"; "$CMD" fail2ban-status; pause ;;
    4) echo "[RUNNING] fail2ban-logs"; "$CMD" fail2ban-logs; pause ;;
    5) echo "[RUNNING] fail2ban-restart"; "$CMD" fail2ban-restart; pause ;;
    6) echo "[RUNNING] recidive"; "$CMD" recidive; pause ;;
    7) echo "[RUNNING] recidive-bans"; "$CMD" recidive-bans; pause ;;
    8)
      ip="$(ask "IP to unban (recidive): ")"
      echo "[RUNNING] recidive-unban $ip"
      "$CMD" recidive-unban "$ip"
      pause
      ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
