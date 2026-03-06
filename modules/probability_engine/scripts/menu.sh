#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Probability Engine Menu"
    echo "================================="
    echo "1. Show Status"
    echo "2. Run Sample (Mock)"
    echo "3. Score Example Input"
    echo "4. Explain Example Input"
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
            # Assuming example input exists relative to where command runs
            # We need to pass absolute path or correct relative path
            EXAMPLE_INPUT="$MODULE_DIR/../config/example_input.json"
            bash "$CMD" score --input "$EXAMPLE_INPUT"
            read -p "Press Enter to continue..."
            ;;
        4)
            EXAMPLE_INPUT="$MODULE_DIR/../config/example_input.json"
            bash "$CMD" explain --input "$EXAMPLE_INPUT"
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
