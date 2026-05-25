#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "==============================="
    echo "   Datasheet Writer Menu"
    echo "==============================="
    echo "1. Run Sanity Check"
    echo "2. Run Tests (13 unit tests)"
    echo "3. Write Dry-Run Record"
    echo "4. Show Module Status"
    echo "5. Quit"
    echo "==============================="
    read -p "Select option: " choice
    case $choice in
        1) bash "$CMD" sanity; read -p "Press Enter...";;
        2) bash "$CMD" test; read -p "Press Enter...";;
        3) bash "$CMD" write --dry-run true; read -p "Press Enter...";;
        4) bash "$CMD" status; read -p "Press Enter...";;
        5) exit 0;;
        *) sleep 1;;
    esac
done
