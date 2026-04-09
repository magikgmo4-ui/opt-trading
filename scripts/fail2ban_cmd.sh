#!/usr/bin/env bash
set -euo pipefail
SOCK="/run/fail2ban/fail2ban.sock"
w(){ for i in $(seq 1 40); do [ -S "$SOCK" ] && return 0; sleep 0.25; done; echo "no socket"; exit 1; }
c(){ sudo /usr/bin/fail2ban-client -s "$SOCK" "$@"; }

case "${1:-}" in
  status)   w; c status | sed -n "1,120p"; echo; c status sshd ;;
  restart)  sudo /bin/systemctl restart fail2ban; w; /opt/trading/scripts/fail2ban_sanity_check.sh ;;
  logs)     sudo journalctl -u fail2ban -b --no-pager -n 120 ;;
  bans)     w; c status sshd | sed -n "1,220p" ;;
  unban)    w; c set sshd unbanip "${2:?missing ip}"; c status sshd | sed -n "1,140p" ;;
  recidive) w; c status recidive || true ;;
  recidive-bans) w; c status recidive | sed -n "1,220p" || true ;;
  recidive-unban) w; c set recidive unbanip "${2:?missing ip}" || true; c status recidive | sed -n "1,160p" || true ;;
  *) echo "usage: cmd-fail2ban {status|restart|logs|bans|unban IP|recidive|recidive-bans|recidive-unban IP}"; exit 2 ;;
esac
