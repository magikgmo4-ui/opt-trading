#!/usr/bin/env bash
set -euo pipefail
menu() {
  cat <<'MENU'
=== reseau_audit — Menu (NON destructif) ===
1) Collect bundle (root)
2) Show latest archive path
q) Quit
MENU
}
latest_tgz() {
  local host
  host="$(hostname -s 2>/dev/null || hostname)"
  ls -1t /opt/trading/_reseau_audit/${host}_*.tgz 2>/dev/null | head -n1 || true
}
while true; do
  menu
  read -r -p "> " c
  case "$c" in
    1) sudo cmd-reseau_audit collect ;;
    2) latest_tgz ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
  echo
done
