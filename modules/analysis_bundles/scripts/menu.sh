#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$MODULE_DIR/scripts/cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Analysis Bundles Menu"
    echo "================================="
    echo "1. Run Sanity Check"
    echo "2. Run Tests"
    echo "3. Produce BTC Core Bundle"
    echo "4. Produce Macro Bundle"
    echo "5. Produce Analysis Verdict"
    echo "6. Data Center Coverage"
    echo "7. Asset Tickets Summary"
    echo "8. Show Module Status"
    echo "9. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1) bash "$CMD" sanity; read -p "Press Enter to continue..." ;;
        2) bash "$CMD" test; read -p "Press Enter to continue..." ;;
        3) bash "$CMD" btc; read -p "Press Enter to continue..." ;;
        4) bash "$CMD" macro; read -p "Press Enter to continue..." ;;
        5) bash "$CMD" verdict; read -p "Press Enter to continue..." ;;
        6) bash "$CMD" datacenter; read -p "Press Enter to continue..." ;;
        7) bash "$CMD" tickets; read -p "Press Enter to continue..." ;;
        8) bash "$CMD" status; read -p "Press Enter to continue..." ;;
        9) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid option."; sleep 1 ;;
    esac
done
