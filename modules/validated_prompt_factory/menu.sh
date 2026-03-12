#!/usr/bin/env bash
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
CMD="$SCRIPT_DIR/cmd.sh"

while true; do
    clear
    echo "=== Validated Prompt Factory ==="
    echo "1. Generate ChatGPT Prompt"
    echo "2. Generate Trae Module Prompt"
    echo "3. Generate Trae Patch Prompt"
    echo "4. Generate Bundle Transfer Prompt"
    echo "5. List Modes"
    echo "6. Validate"
    echo "0. Exit"
    echo "================================"
    read -p "Select: " choice
    
    case "$choice" in
        1) bash "$CMD" generate chatgpt_session ;;
        2) bash "$CMD" generate trae_module ;;
        3) bash "$CMD" generate trae_patch ;;
        4) bash "$CMD" generate bundle_transfer ;;
        5) bash "$CMD" list-modes ;;
        6) bash "$CMD" validate ;;
        0) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
    read -p "Press Enter..."
done
