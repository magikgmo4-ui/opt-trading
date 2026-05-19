#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

while true; do
    clear
    echo "=== Wrappers Registry Reader ==="
    echo "1. Status"
    echo "2. List Wrappers"
    echo "3. Show Families"
    echo "4. Show 'menu-ui_registry_msi'"
    echo "5. Show 'cmd-desk_pro_runner'"
    echo "6. Export JSON"
    echo "0. Exit"
    echo "======================"
    read -p "Select: " choice
    
    case "$choice" in
        1) bash "$CMD" status ;;
        2) bash "$CMD" list ;;
        3) bash "$CMD" show-families ;;
        4) bash "$CMD" show menu-ui_registry_msi ;;
        5) bash "$CMD" show cmd-desk_pro_runner ;;
        6) bash "$CMD" export-json ;;
        0) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
    read -p "Press Enter..."
done
