#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/scripts/reseau_ssh"
# shellcheck source=/dev/null
source "$BASE/lib/common.sh"

echo "=== reseau_ssh sanity ==="
echo "time: $(date -Is)"
echo

echo "[host]"
hostnamectl 2>/dev/null | sed -n '1,12p' || true
echo

echo "[network]"
ip -4 -o addr show scope global 2>/dev/null || true
ip route 2>/dev/null | head -n 15 || true
echo

echo "[ssh]"
systemctl is-enabled ssh 2>/dev/null || systemctl is-enabled sshd 2>/dev/null || true
systemctl --no-pager status ssh 2>/dev/null | sed -n '1,18p' || systemctl --no-pager status sshd 2>/dev/null | sed -n '1,18p' || true
echo

echo "[ufw]"
ufw status verbose 2>/dev/null || true
echo

echo "[fail2ban]"
systemctl --no-pager status fail2ban 2>/dev/null | sed -n '1,18p' || true
fail2ban-client ping 2>/dev/null || true
fail2ban-client status sshd 2>/dev/null || true
echo

echo "[wireguard]"
wg show 2>/dev/null || true
ip a show wg0 2>/dev/null || true

echo
echo "OK: sanity finished"
