#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Perf Engine Menu"
    echo "================================="
    echo "1. Show Status"
    echo "2. Run Sample Track (Mock)"
    echo "3. Export Sample States"
    echo "4. Explain Sample Logic"
    echo "5. Quit"
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
            bash "$CMD" export
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" explain
            read -p "Press Enter to continue..."
            ;;
        5)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
