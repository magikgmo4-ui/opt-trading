#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

while true; do
    clear
    echo "=== Modules Registry Reader ==="
    echo "1. Status"
    echo "2. List Modules"
    echo "3. Show Domains"
    echo "4. Show 'desk_pro_runner'"
    echo "5. Show 'probability_engine'"
    echo "6. Export JSON"
    echo "0. Exit"
    echo "======================"
    read -p "Select: " choice
    
    case "$choice" in
        1) bash "$CMD" status ;;
        2) bash "$CMD" list ;;
        3) bash "$CMD" show-domains ;;
        4) bash "$CMD" show desk_pro_runner ;;
        5) bash "$CMD" show probability_engine ;;
        6) bash "$CMD" export-json ;;
        0) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
    read -p "Press Enter..."
done
