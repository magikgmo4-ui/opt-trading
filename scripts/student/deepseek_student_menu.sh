#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student Menu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/deepseek_student_cmd.sh"

while true; do
    clear
    echo "=== DEEPSEEK STUDENT MENU ==="
    echo ""
    echo "[Health / Status]"
    echo "1. Sanity Check"
    echo "2. Status"
    echo "3. Summary"
    echo ""
    echo "[Execution]"
    echo "4. Run DeepSeek (Status)"
    echo "5. Run DeepSeek (Sanity)"
    echo "6. Run DeepSeek (Models)"
    echo "7. Tail Latest Log"
    echo ""
    echo "[Docs]"
    echo "8. Show Runbook Path"
    echo "9. Show Quick Reference Path"
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
            bash "$CMD" summary
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" run-logged status
            read -p "Press Enter to continue..."
            ;;
        5)
            bash "$CMD" run-logged sanity
            read -p "Press Enter to continue..."
            ;;
        6)
            bash "$CMD" run-logged models
            read -p "Press Enter to continue..."
            ;;
        7)
            bash "$CMD" tail-latest-log
            read -p "Press Enter to continue..."
            ;;
        8)
            echo "Runbook: docs/student_deepseek_runbook.md"
            read -p "Press Enter to continue..."
            ;;
        9)
            echo "Quick Reference: docs/student_deepseek_quick_reference.md"
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
