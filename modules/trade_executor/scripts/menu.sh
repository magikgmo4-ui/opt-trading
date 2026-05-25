#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Trade Executor Menu"
    echo "================================="
    echo "1. Run Sanity Check"
    echo "2. Run Tests (28 unit tests)"
    echo "3. Execute Dry-Run Trade"
    echo "4. Show Module Status"
    echo "5. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1)
            bash "$CMD" sanity
            read -p "Press Enter to continue..."
            ;;
        2)
            bash "$CMD" test
            read -p "Press Enter to continue..."
            ;;
        3)
            bash "$CMD" execute --dry-run true --ticker BTCUSDT
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" status
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
