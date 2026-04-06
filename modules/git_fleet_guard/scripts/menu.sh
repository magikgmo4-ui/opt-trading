#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

default_machines="admin-trading,student,db-layer"

while true; do
  cat <<'EOF'
=== git_fleet_guard ===
1) status
2) audit all
3) audit one/many machines
4) show last report (markdown)
5) guided remediation (markdown)
6) quit
EOF
  read -r -p "> " choice || exit 0
  case "$choice" in
    1) "$CMD" status ;;
    2) "$CMD" audit --machines "$default_machines" ;;
    3)
      read -r -p "Machines CSV [student,db-layer]: " machines
      machines="${machines:-student,db-layer}"
      "$CMD" audit --machines "$machines"
      ;;
    4) "$CMD" report --format md ;;
    5) "$CMD" remediate --format md ;;
    6) echo "Sortie."; exit 0 ;;
    *) echo "Choix invalide." ;;
  esac
  echo
done
