#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Student Menu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/desk_pro_student_cmd.sh"

while true; do
    clear
    echo "=== DESK PRO STUDENT MENU ==="
    echo ""
    echo "[Health / Status]"
    echo "1. Sanity Check"
    echo "2. Status"
    echo "3. Shared Info"
    echo "4. Summary"
    echo ""
    echo "[Docs]"
    echo "5. Show Runbook Path"
    echo "6. Show Quick Reference Path"
    echo ""
    echo "0. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1)
            bash "$CMD" sanity
            read -p "Press Enter to continue..."
            ;;
        2)
            bash "$CMD" status
            read -p "Press Enter to continue..."
            ;;
        3)
            bash "$CMD" shared-info
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" summary
            read -p "Press Enter to continue..."
            ;;
        5)
            echo "Runbook: docs/student_desk_pro_runbook.md"
            read -p "Press Enter to continue..."
            ;;
        6)
            echo "Quick Reference: docs/student_desk_pro_quick_reference.md"
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
