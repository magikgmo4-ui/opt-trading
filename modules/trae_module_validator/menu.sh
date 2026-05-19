#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

while true; do
    clear
    echo "=== Trae Module Validator V1 ==="
    echo "1. Validate Module"
    echo "2. Validate All Modules"
    echo "3. Exit"
    echo "================================"
    read -p "Select: " choice
    
    case "$choice" in
        1) 
            read -p "Enter module name: " mod_name
            if [ -n "$mod_name" ]; then
                bash "$CMD" validate "$mod_name"
            else
                echo "Error: Module name required"
            fi
            ;;
        2) 
            bash "$CMD" validate-all 
            ;;
        3) 
            exit 0 
            ;;
        *) 
            echo "Invalid option" 
            ;;
    esac
    read -p "Press Enter..."
done
