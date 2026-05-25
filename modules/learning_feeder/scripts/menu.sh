#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================"
    echo "   Learning Feeder Menu"
    echo "================================"
    echo "1. Run Sanity Check"
    echo "2. Run Tests (29 unit tests)"
    echo "3. Feed Dry-Run Feedback"
    echo "4. Show Module Status"
    echo "5. Quit"
    echo "================================"
    read -p "Select option: " choice
    case $choice in
        1) bash "$CMD" sanity; read -p "Press Enter...";;
        2) bash "$CMD" test; read -p "Press Enter...";;
        3) bash "$CMD" feed --dry-run true; read -p "Press Enter...";;
        4) bash "$CMD" status; read -p "Press Enter...";;
        5) exit 0;;
        *) sleep 1;;
    esac
done
