#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"
while true; do
  echo
  echo "=== configure_openclaw ==="
  echo "1) sanity"
  echo "2) status"
  echo "3) validate"
  echo "4) config file"
  echo "5) configure wizard"
  echo "6) dashboard"
  echo "7) agents list"
  echo "8) agents add"
  echo "9) set identity from workspace"
  echo "10) config get"
  echo "11) config set"
  echo "12) config unset"
  echo "0) quit"
  read -r -p "> " choice
  case "$choice" in
    1) "$CMD" sanity ;;
    2) "$CMD" status ;;
    3) "$CMD" validate ;;
    4) "$CMD" config-file ;;
    5) "$CMD" wizard ;;
    6) "$CMD" dashboard ;;
    7) "$CMD" agents-list ;;
    8) read -r -p "agent name > " an; "$CMD" agents-add "$an" ;;
    9) read -r -p "workspace path > " wp; "$CMD" set-identity-from-workspace "$wp" ;;
    10) read -r -p "config path > " cp; "$CMD" get "$cp" ;;
    11) read -r -p "config path > " cp; read -r -p "value > " cv; "$CMD" set "$cp" "$cv" ;;
    12) read -r -p "config path > " cp; "$CMD" unset "$cp" ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
done
