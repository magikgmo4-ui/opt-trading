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
    echo "3. Models"
    echo "4. Summary"
    echo ""
    echo "[DeepSeek Usage]"
    echo "5. Think"
    echo "6. Response"
    echo "7. Roadmap Events"
    echo "8. Roadmap Think Module"
    echo "9. Roadmap Response Module"
    echo ""
    echo "[Execution]"
    echo "10. Run Logged (Status)"
    echo "11. Run Logged (Models)"
    echo "12. Tail Latest Log"
    echo ""
    echo "[Docs]"
    echo "13. Show Runbook Path"
    echo "14. Show Quick Reference Path"
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
            bash "$CMD" models
            read -p "Press Enter to continue..."
            ;;
        4)
            bash "$CMD" summary
            read -p "Press Enter to continue..."
            ;;
        5)
            read -p "Enter Think prompt: " prompt
            bash "$CMD" think "$prompt"
            read -p "Press Enter to continue..."
            ;;
        6)
            read -p "Enter Response prompt: " prompt
            bash "$CMD" response "$prompt"
            read -p "Press Enter to continue..."
            ;;
        7)
            read -p "Enter max tokens (optional): " tokens
            bash "$CMD" roadmap-events $tokens
            read -p "Press Enter to continue..."
            ;;
        8)
            read -p "Enter module name: " mod
            bash "$CMD" roadmap-think-module "$mod"
            read -p "Press Enter to continue..."
            ;;
        9)
            read -p "Enter module name: " mod
            bash "$CMD" roadmap-response-module "$mod"
            read -p "Press Enter to continue..."
            ;;
        10)
            bash "$CMD" run-logged status
            read -p "Press Enter to continue..."
            ;;
        11)
            bash "$CMD" run-logged models
            read -p "Press Enter to continue..."
            ;;
        12)
            bash "$CMD" tail-latest-log
            read -p "Press Enter to continue..."
            ;;
        13)
            echo "Runbook: docs/student_deepseek_runbook.md"
            read -p "Press Enter to continue..."
            ;;
        14)
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
