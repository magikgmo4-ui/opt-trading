#!/usr/bin/env bash
set -euo pipefail

# Derivatives Analyzer - Interactive Menu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

while true; do
    clear
    echo "=== Derivatives Analyzer Menu ==="
    echo "1. Status"
    echo "2. Analyze Sample"
    echo "3. Explain Logic"
    echo "4. Export Analysis"
    echo "0. Exit"
    echo "================================"
    read -p "Select: " choice
    
    case "$choice" in
        1) bash "$CMD" status ;;
        2) bash "$CMD" analyze ;;
        3) bash "$CMD" explain ;;
        4) bash "$CMD" export ;;
        0) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
    read -p "Press Enter..."
done
