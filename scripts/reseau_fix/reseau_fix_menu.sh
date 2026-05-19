#!/usr/bin/env bash
set -euo pipefail
menu() {
  cat <<'MENU'
=== reseau_fix — Menu ===
1) Status (quick)
2) Apply SAFE baseline (hosts + sshd safe + UFW)
3) Apply LOCKDOWN (disable SSH password auth)
4) Disable db-layer wg0 (optional cleanup)
q) Quit
MENU
}
while true; do
  menu
  read -r -p "> " c
  case "$c" in
    1) cmd-reseau_fix status ;;
    2) sudo cmd-reseau_fix apply-safe ;;
    3) sudo cmd-reseau_fix apply-lockdown ;;
    4) sudo cmd-reseau_fix disable-dblayer-wg0 ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
  echo
done
