\
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/reseau_ssh_cmd.sh"

while true; do
  cat <<'MENU'
=== reseau_ssh Step 1b Menu ===
1) Dry-run (show changes)
2) Apply /etc/hosts + ~/.ssh/config
3) Set hostname (Linux)
4) Sanity check + connectivity
q) Quit
MENU
  read -r -p "> " choice
  case "$choice" in
    1) "$CMD" dry-run ;;
    2) "$CMD" apply ;;
    3) read -r -p "Target hostname: " hn; "$CMD" hostname "$hn" ;;
    4) "$CMD" sanity ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
