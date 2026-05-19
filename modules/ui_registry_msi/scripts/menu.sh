#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

while true; do
    clear
    echo "=== UI Registry MSI ==="
    echo "1. Status"
    echo "2. List Surfaces"
    echo "3. Show Machines"
    echo "4. Show Categories"
    echo "5. Show MSI (db-layer)"
    echo "6. Export JSON"
    echo "7. Export Markdown"
    echo "0. Exit"
    echo "======================"
    read -p "Select: " choice
    
    case "$choice" in
        1) bash "$CMD" status ;;
        2) bash "$CMD" list ;;
        3) bash "$CMD" show-machines ;;
        4) bash "$CMD" show-categories ;;
        5) bash "$CMD" show-msi ;;
        6) bash "$CMD" export-json ;;
        7) bash "$CMD" export-md ;;
        0) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
    read -p "Press Enter..."
done
