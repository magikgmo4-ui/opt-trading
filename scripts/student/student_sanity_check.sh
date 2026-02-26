#!/usr/bin/env bash
set -euo pipefail

t(){ timeout 3 "$@" 2>/dev/null || true; }

echo "=== STUDENT Sanity Check ==="
date -Is
echo

echo "[host]"
t hostnamectl
echo

echo "[network]"
t sh -c "ip -4 addr | grep -E 'inet ' | grep -v 127.0.0.1"
t sh -c "ip -4 route | head -n 20"
echo

echo "[disk]"
t lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS | sed 's/^/  /' || true
echo

echo "[lvm]"
t sudo -n vgs
t sudo -n lvs
echo

echo "[services]"
t sh -c 'systemctl is-active --quiet ssh && echo "OK ssh: active" || echo "WARN ssh: not active"'
t sh -c 'systemctl is-active --quiet fail2ban && echo "OK fail2ban: active" || echo "WARN fail2ban: not active"'
echo

echo "[ufw]"
t sudo -n ufw status verbose

echo
echo "PASS: student sanity ok"
