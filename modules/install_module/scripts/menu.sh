#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/opt/trading}"
HOST="$(hostname)"

cmd() { "$ROOT/modules/install_module/scripts/cmd.sh" "$@"; }

while true; do
  echo
  echo "=== INSTALL MODULE ==="
  echo "host=$HOST"
  echo "root=$ROOT"
  echo
  if [[ "$HOST" == "admin-trading" ]]; then
    echo "1) List packages in shared"
    echo "2) Install package (by number or filename)"
    echo "3) Sync ALL (git push + pull student/db-layer + bootstrap shortcuts)"
    echo "q) Quit"
  else
    echo "1) List packages in shared"
    echo "2) Install package (by number or filename)"
    echo "3) Sync/Validate (git pull + sanity + bootstrap shortcuts)"
    echo "q) Quit"
  fi
  read -r -p "> " choice
  case "$choice" in
    1)
      cmd list_packages
      ;;
    2)
      read -r -p "Package (num|filename): " sel
      read -r -p "Install shortcuts after install? (sudo) [y/N]: " ys
      if [[ "${ys,,}" == "y" ]]; then
        cmd install "$sel" --sudo
      else
        cmd install "$sel"
      fi
      ;;
    3)
      if [[ "$HOST" == "admin-trading" ]]; then
        cmd sync_all
      else
        cmd sync_validate
      fi
      ;;
    q|quit|exit) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
  echo
  read -r -p "Press Enter..." _
  clear || true
done
