#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Admin Menu (Updated: Ops/Institutional Style)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/desk_pro_cmd.sh"

while true; do
    clear
    echo "=== DESK PRO OPS MENU ==="
    echo ""
    echo "[Health / Status]"
    echo "1. Sanity Check"
    echo "2. Incident Checklist"
    echo "3. Status Global"
    echo "4. Last Run Info"
    echo "5. Tail Latest Log"
    echo ""
    echo "[Execution]"
    echo "6. Run Desk Pro"
    echo "7. Run Desk Pro (Logged)"
    echo "8. Run + Show Dashboard"
    echo ""
    echo "[Dashboard / Exports]"
    echo "9. Dashboard Latest"
    echo "10. Export JSON Latest"
    echo "11. Export HTML Latest"
    echo "12. Copy Latest To /shared"
    echo ""
    echo "[Session Journal]"
    echo "13. Show Session Journal"
    echo "14. Append Session Note"
    echo ""
    echo "0. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1)
            bash "$SCRIPT_DIR/desk_pro_sanity_check.sh"
            read -p "Press Enter to continue..."
            ;;
        2)
            bash "$SCRIPT_DIR/desk_pro_incident_checklist.sh"
            read -p "Press Enter to continue..."
            ;;
        3)
            bash "$CMD" status
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" last-run-info
            read -p "Press Enter to continue..."
            ;;
        5)
            bash "$CMD" tail-latest-log
            read -p "Press Enter to continue..."
            ;;
        6)
            bash "$CMD" run
            read -p "Press Enter to continue..."
            ;;
        7)
            bash "$CMD" run-logged
            read -p "Press Enter to continue..."
            ;;
        8)
            bash "$CMD" run-and-show
            read -p "Press Enter to continue..."
            ;;
        9)
            bash "$CMD" dashboard-latest
            read -p "Press Enter to continue..."
            ;;
        10)
            bash "$CMD" export-json-latest
            read -p "Press Enter to continue..."
            ;;
        11)
            bash "$CMD" export-html-latest
            read -p "Press Enter to continue..."
            ;;
        12)
            bash "$CMD" copy-latest-to-shared
            read -p "Press Enter to continue..."
            ;;
        13)
            bash "$CMD" show-session-journal
            read -p "Press Enter to continue..."
            ;;
        14)
            read -p "Enter note: " note
            bash "$CMD" add-session-note "$note"
            read -p "Press Enter to continue..."
            ;;
        0)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
