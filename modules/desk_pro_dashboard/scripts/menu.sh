#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Desk Pro Dashboard Menu"
    echo "================================="
    echo "1. Show Status"
    echo "2. Run Sample (Legacy)"
    echo "3. Render Latest Run"
    echo "4. Export JSON (Latest)"
    echo "5. Export HTML (Latest)"
    echo "6. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1)
            bash "$CMD" status
            read -p "Press Enter to continue..."
            ;;
        2)
            bash "$CMD" sample
            read -p "Press Enter to continue..."
            ;;
        3)
            bash "$CMD" render-latest
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" export-json
            read -p "Press Enter to continue..."
            ;;
        5)
            bash "$CMD" export-html
            read -p "Press Enter to continue..."
            ;;
        6)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
