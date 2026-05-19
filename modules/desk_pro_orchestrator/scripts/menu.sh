#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Desk Pro Orchestrator Menu"
    echo "================================="
    echo "1. Show Status"
    echo "2. Run Sample Orchestration (All Modules)"
    echo "3. Explain Pipeline Logic"
    echo "4. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1)
            bash "$CMD" status
            read -p "Press Enter to continue..."
            ;;
        2)
            bash "$CMD" sample-run
            read -p "Press Enter to continue..."
            ;;
        3)
            bash "$CMD" explain
            read -p "Press Enter to continue..."
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
