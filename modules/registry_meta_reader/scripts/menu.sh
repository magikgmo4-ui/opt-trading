#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

while true; do
    clear
    echo "=== Registry Meta Reader ==="
    echo "1. Status"
    echo "2. List Registries"
    echo "3. Show 'machines_registry'"
    echo "4. Show 'modules_registry'"
    echo "5. Export JSON"
    echo "0. Exit"
    echo "======================"
    read -p "Select: " choice
    
    case "$choice" in
        1) bash "$CMD" status ;;
        2) bash "$CMD" list ;;
        3) bash "$CMD" show machines_registry ;;
        4) bash "$CMD" show modules_registry ;;
        5) bash "$CMD" export-json ;;
        0) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
    read -p "Press Enter..."
done
