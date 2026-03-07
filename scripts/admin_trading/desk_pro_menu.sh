#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Admin Menu

if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
CMD="$SCRIPT_DIR/desk_pro_cmd.sh"

while true; do
    clear
    echo "================================="
    echo "   Desk Pro Admin Trading"
    echo "================================="
    echo "1. Sanity Check"
    echo "2. Status Global"
    echo "3. Run Desk Pro (Full)"
    echo "4. Run + Show Dashboard"
    echo "5. Dashboard Latest"
    echo "6. Export JSON Latest"
    echo "7. Export HTML Latest"
    echo "8. Copy Latest To /shared"
    echo "9. Run Desk Pro (Logged)"
    echo "10. Tail Latest Log"
    echo "11. Last Run Info"
    echo "12. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1)
            bash "$SCRIPT_DIR/desk_pro_sanity_check.sh"
            read -p "Press Enter to continue..."
            ;;
        2)
            bash "$CMD" status
            read -p "Press Enter to continue..."
            ;;
        3)
            bash "$CMD" run
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" run-and-show
            read -p "Press Enter to continue..."
            ;;
        5)
            bash "$CMD" dashboard-latest
            read -p "Press Enter to continue..."
            ;;
        6)
            bash "$CMD" export-json-latest
            read -p "Press Enter to continue..."
            ;;
        7)
            bash "$CMD" export-html-latest
            read -p "Press Enter to continue..."
            ;;
        8)
            bash "$CMD" copy-latest-to-shared
            read -p "Press Enter to continue..."
            ;;
        9)
            bash "$CMD" run-logged
            read -p "Press Enter to continue..."
            ;;
        10)
            bash "$CMD" tail-latest-log
            read -p "Press Enter to continue..."
            ;;
        11)
            bash "$CMD" last-run-info
            read -p "Press Enter to continue..."
            ;;
        12)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
