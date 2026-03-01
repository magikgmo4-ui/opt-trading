#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/scripts/reseau_ssh"
# shellcheck source=/dev/null
source "$BASE/lib/common.sh"

menu() {
  cat <<'MENU'
=== reseau_ssh — Menu ===
1) Sanity check
2) Bootstrap (packages + UFW + Fail2Ban) [SAFE]
3) SSH hardening SAFE (drop-in)
4) SSH lockdown (disable password auth) [REQUIRES authorized_keys]
5) WireGuard server init (prints pubkey)
6) WireGuard client init (writes wg0.conf + prints pubkey)
7) WireGuard add peer (server)
8) WireGuard show
q) Quit
MENU
}

while true; do
  menu
  read -r -p "> " c
  case "$c" in
    1) cmd-reseau_ssh sanity ;;
    2) sudo cmd-reseau_ssh bootstrap ;;
    3) sudo cmd-reseau_ssh ssh-hardening-safe ;;
    4) sudo cmd-reseau_ssh ssh-lockdown ;;
    5) read -r -p "WG server IP (default 10.66.66.1/24): " ip
       sudo cmd-reseau_ssh wg-server-init "${ip:-10.66.66.1/24}" ;;
    6) read -r -p "Server LAN IP (ex: 192.168.16.xxx): " sip
       read -r -p "Client WG IP (ex: 10.66.66.2/24): " cip
       sudo cmd-reseau_ssh wg-client-init "$sip" "$cip" ;;
    7) read -r -p "Peer name: " n
       read -r -p "Peer pubkey: " k
       read -r -p "Peer WG IP CIDR (ex: 10.66.66.2/32): " ip
       sudo cmd-reseau_ssh wg-add-peer "$n" "$k" "$ip" ;;
    8) cmd-reseau_ssh wg-show ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
  echo
done
