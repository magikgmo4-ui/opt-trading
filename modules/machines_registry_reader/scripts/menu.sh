#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

while true; do
    clear
    echo "=== Machines Registry Reader ==="
    echo "1. Status"
    echo "2. List Machines"
    echo "3. Show Roles"
    echo "4. Show 'msi_db_layer'"
    echo "5. Show 'admin_trading'"
    echo "6. Export JSON"
    echo "0. Exit"
    echo "======================"
    read -p "Select: " choice
    
    case "$choice" in
        1) bash "$CMD" status ;;
        2) bash "$CMD" list ;;
        3) bash "$CMD" show-roles ;;
        4) bash "$CMD" show msi_db_layer ;;
        5) bash "$CMD" show admin_trading ;;
        6) bash "$CMD" export-json ;;
        0) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
    read -p "Press Enter..."
done
