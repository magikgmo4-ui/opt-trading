#!/usr/bin/env bash
set -euo pipefail

SOCK="/run/fail2ban/fail2ban.sock"

echo "=== Fail2Ban Sanity Check ==="
echo "Host: $(hostname)"
echo "Time: $(date -Is)"
echo

echo "1) systemd status"
systemctl --no-pager -l status fail2ban | head -n 25 || true
echo

echo "2) wait for socket"
for i in $(seq 1 40); do
  if [[ -S "$SOCK" ]]; then
    echo "socket OK: $SOCK"
    break
  fi
  sleep 0.25
done
[[ -S "$SOCK" ]] || { echo "FAIL: socket missing: $SOCK"; exit 1; }
echo

echo "3) ping"
sudo fail2ban-client -s "$SOCK" ping
echo

echo "4) jail list"
sudo fail2ban-client -s "$SOCK" status | sed -n "1,120p"
echo

echo "5) sshd jail"
sudo fail2ban-client -s "$SOCK" status sshd
echo

echo "PASS: fail2ban OK"
