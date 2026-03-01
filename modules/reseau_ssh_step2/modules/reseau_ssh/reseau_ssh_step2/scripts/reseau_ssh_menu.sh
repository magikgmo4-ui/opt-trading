#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$HERE/reseau_ssh_cmd.sh"
while true; do
  echo "=== reseau_ssh Step 2 Menu (WireGuard + Firewall) ==="
  echo "1) Sanity"
  echo "2) Install WireGuard tools"
  echo "3) Generate keys (local)"
  echo "4) Show local public key"
  echo "5) Render config"
  echo "6) Apply config (/etc/wireguard/wg0.conf)"
  echo "7) Bring wg0 up"
  echo "8) wg status"
  echo "9) Bring wg0 down"
  echo "10) Firewall dry-run (UFW)"
  echo "11) Firewall apply (UFW)"
  echo "q) Quit"
  read -rp "> " choice
  case "$choice" in
    1) "$CMD" sanity ;;
    2) "$CMD" wg-install ;;
    3) "$CMD" wg-genkeys ;;
    4) "$CMD" wg-showpub ;;
    5) "$CMD" wg-render ;;
    6) "$CMD" wg-apply ;;
    7) "$CMD" wg-up ;;
    8) "$CMD" wg-status ;;
    9) "$CMD" wg-down ;;
    10) "$CMD" fw-dry-run ;;
    11) "$CMD" fw-apply ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
  echo
done
