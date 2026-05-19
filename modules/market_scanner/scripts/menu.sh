#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Market Scanner Menu"
    echo "================================="
    echo "1. Show Status"
    echo "2. Run Sample Scan (Mock)"
    echo "3. Scan Custom Input"
    echo "4. Export Scan Results"
    echo "5. Explain Scan Logic"
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
            # Default to sample if empty
            DEFAULT_INPUT="$MODULE_DIR/../config/sample_markets.json"
            read -p "Enter input file path (default: $DEFAULT_INPUT): " INPUT_PATH
            INPUT_PATH="${INPUT_PATH:-$DEFAULT_INPUT}"
            bash "$CMD" scan --input "$INPUT_PATH"
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" export
            read -p "Press Enter to continue..."
            ;;
        5)
            DEFAULT_INPUT="$MODULE_DIR/../config/sample_markets.json"
            read -p "Enter input file path (default: $DEFAULT_INPUT): " INPUT_PATH
            INPUT_PATH="${INPUT_PATH:-$DEFAULT_INPUT}"
            bash "$CMD" explain --input "$INPUT_PATH"
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
