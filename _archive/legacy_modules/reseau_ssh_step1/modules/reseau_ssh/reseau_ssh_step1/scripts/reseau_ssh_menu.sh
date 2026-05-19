#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/reseau_ssh_cmd.sh"
SANITY="$SCRIPT_DIR/sanity_check_reseau_ssh.sh"

while true; do
  cat <<'MENU'
=== reseau_ssh Menu (Step 1) ===
1) Sanity check
2) Show inventory (hosts.yaml)
3) Show ssh_config template
4) Quick SSH test (best-effort)
q) Quit
MENU
  read -r -p "> " choice
  case "$choice" in
    1) "$SANITY" ;;
    2) "$CMD" show-inv ;;
    3) "$CMD" show-ssh-template ;;
    4) "$CMD" quick-test ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
