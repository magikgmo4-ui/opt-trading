#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Desk Pro Runner Menu"
    echo "================================="
    echo "1. Show Status"
    echo "2. Run Orchestration (Full)"
    echo "3. Run & Show Dashboard"
    echo "4. Show Latest Dashboard"
    echo "5. Export Latest (JSON)"
    echo "6. Export Latest (HTML)"
    echo "7. Quit"
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
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
