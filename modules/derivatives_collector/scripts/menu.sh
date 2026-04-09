#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Derivatives Collector Menu"
    echo "================================="
    echo "1. Run Collection (Historical)"
    echo "2. Run Sample (Historical Mock)"
    echo "3. Export Data (Historical)"
    echo "4. Show Status (Historical)"
    echo "5. Run Lifecycle Collection"
    echo "6. Run Lifecycle Sample"
    echo "7. Run Lifecycle Export"
    echo "8. Show Lifecycle Status"
    echo "9. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1)
            bash "$CMD" collect
            read -p "Press Enter to continue..."
            ;;
        2)
            bash "$CMD" sample
            read -p "Press Enter to continue..."
            ;;
        3)
            bash "$CMD" export
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" status
            read -p "Press Enter to continue..."
            ;;
        5)
            bash "$CMD" lifecycle
            read -p "Press Enter to continue..."
            ;;
        6)
            bash "$CMD" lifecycle-sample
            read -p "Press Enter to continue..."
            ;;
        7)
            bash "$CMD" lifecycle-export
            read -p "Press Enter to continue..."
            ;;
        8)
            bash "$CMD" lifecycle-status
            read -p "Press Enter to continue..."
            ;;
        9)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
