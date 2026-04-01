#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Liquidation Analyzer Menu"
    echo "================================="
    echo "1. Show Status"
    echo "2. Run Sample Analysis (Mock)"
    echo "3. Analyze Custom Input"
    echo "4. Export Results"
    echo "5. Explain Analysis Logic"
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
            DEFAULT_INPUT="$MODULE_DIR/../config/sample_liquidations.json"
            read -p "Enter input file path (default: $DEFAULT_INPUT): " INPUT_PATH
            INPUT_PATH="${INPUT_PATH:-$DEFAULT_INPUT}"
            bash "$CMD" analyze --input "$INPUT_PATH"
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" export
            read -p "Press Enter to continue..."
            ;;
        5)
            DEFAULT_INPUT="$MODULE_DIR/../config/sample_liquidations.json"
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
