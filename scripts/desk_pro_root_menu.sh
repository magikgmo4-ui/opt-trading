#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Root Menu (Bash)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/desk_pro_root_cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Desk Pro Root Menu"
    echo "================================="
    echo "1. Status Global"
    echo "2. Run Desk Pro (Full)"
    echo "3. Run + Show Dashboard"
    echo "4. Dashboard Latest"
    echo "5. Export JSON Latest"
    echo "6. Export HTML Latest"
    echo "7. Sanity Check"
    echo "8. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1)
            bash "$CMD" status
            read -p "Press Enter to continue..."
            ;;
        2)
            bash "$CMD" run
            read -p "Press Enter to continue..."
            ;;
        3)
            bash "$CMD" run-and-show
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" dashboard-latest
            read -p "Press Enter to continue..."
            ;;
        5)
            bash "$CMD" export-json-latest
            read -p "Press Enter to continue..."
            ;;
        6)
            bash "$CMD" export-html-latest
            read -p "Press Enter to continue..."
            ;;
        7)
            bash "$SCRIPT_DIR/desk_pro_root_sanity_check.sh"
            read -p "Press Enter to continue..."
            ;;
        8)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
