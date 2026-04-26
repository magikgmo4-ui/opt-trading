#!/usr/bin/env bash
set -euo pipefail

RESEAU_SSH_ENTRY_SOURCE="${BASH_SOURCE[0]}"
RESEAU_SSH_SOURCE_PATH="${BASH_SOURCE[0]}"
while [ -L "$RESEAU_SSH_SOURCE_PATH" ]; do
  RESEAU_SSH_SOURCE_DIR="$(cd "$(dirname "$RESEAU_SSH_SOURCE_PATH")" && pwd -P)"
  RESEAU_SSH_SOURCE_PATH="$(readlink "$RESEAU_SSH_SOURCE_PATH")"
  case "$RESEAU_SSH_SOURCE_PATH" in
    /*) ;;
    *) RESEAU_SSH_SOURCE_PATH="$RESEAU_SSH_SOURCE_DIR/$RESEAU_SSH_SOURCE_PATH" ;;
  esac
done
RESEAU_SSH_SOURCE_DIR="$(cd "$(dirname "$RESEAU_SSH_SOURCE_PATH")" && pwd -P)"
# shellcheck source=./_reseau_ssh_common.sh
source "$RESEAU_SSH_SOURCE_DIR/_reseau_ssh_common.sh"
# shellcheck source=./_reseau_ssh_wireguard.sh
source "$RESEAU_SSH_SOURCE_DIR/_reseau_ssh_wireguard.sh"

echo "=== reseau_ssh sanity (canonical facade) ==="
reseau_ssh_print_info
echo

[ -d "$RESEAU_SSH_MODULE_DIR" ] || { echo "FAIL: module root missing"; exit 2; }
[ -d "$RESEAU_SSH_TOP_DIR" ] || { echo "FAIL: scripts dir missing"; exit 2; }
[ -d "$RESEAU_SSH_WIREGUARD_DIR" ] || { echo "FAIL: wireguard payload missing"; exit 2; }
[ -x "$RESEAU_SSH_TOP_MENU" ] || { echo "FAIL: top-level menu missing"; exit 2; }
[ -x "$RESEAU_SSH_TOP_CMD" ] || { echo "FAIL: top-level cmd missing"; exit 2; }
[ -f "$RESEAU_SSH_WG_INVENTORY" ] || { echo "FAIL: wireguard inventory missing"; exit 2; }

echo "OK: facade preflight"
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

if [ "${RESEAU_SSH_SKIP_DEEP_SANITY:-0}" = "1" ]; then
  echo "SKIP: wireguard deep sanity disabled by RESEAU_SSH_SKIP_DEEP_SANITY=1"
  exit 0
fi

echo "[wireguard internal sanity]"
reseau_ssh_wireguard_sanity
