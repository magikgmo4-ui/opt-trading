#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

while true; do
    clear
    echo "=== Registry Router ==="
    echo "1. Status"
    echo "2. Show Entries"
    echo "3. Open Meta Index"
    echo "4. Open Machines Registry"
    echo "5. Open Modules Registry"
    echo "6. Open UI Registry"
    echo "7. Open Wrappers Registry"
    echo "0. Exit"
    echo "======================="
    read -p "Select: " choice
    
    case "$choice" in
        1) bash "$CMD" status ;;
        2) bash "$CMD" show-entries ;;
        3) bash "$CMD" open-meta ;;
        4) bash "$CMD" open-machines ;;
        5) bash "$CMD" open-modules ;;
        6) bash "$CMD" open-ui ;;
        7) bash "$CMD" open-wrappers ;;
        0) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
    read -p "Press Enter..."
done
