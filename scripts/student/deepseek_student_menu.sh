#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Menu
# Advanced Operator Menu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CMD="$SCRIPT_DIR/deepseek_student_cmd.sh"

while true; do
    clear
    echo "=== DEEPSEEK STUDENT MENU ==="
    echo "Host: $(hostname)"
    echo ""
    echo "[1] UTILISATION QUOTIDIENNE"
    echo "  1. Summary"
    echo "  2. Think"
    echo "  3. Response"
    echo "  4. Roadmap Events"
    echo "  5. Roadmap Think Module"
    echo "  6. Roadmap Response Module"
    echo ""
    echo "[2] RÉSULTATS / ARCHIVES"
    echo "  7. Show Latest Thinking"
    echo "  8. Show Latest Response"
    echo "  9. Show Latest Roadmap"
    echo "  10. Tail Latest Log"
    echo ""
    echo "[3] AUTOMATISATION"
    echo "  11. Run Daily Log Thinking Now"
    echo "  12. Install Daily Timer"
    echo "  13. Show Timer Status"
    echo "  14. Show Daily Timer Logs"
    echo ""
    echo "[4] DEV / DEBUG / MAINTENANCE"
    echo "  15. Sanity Check"
    echo "  16. Status"
    echo "  17. Models"
    echo "  18. Show Paths / Environment"
    echo "  19. Explain / Help"
    echo ""
    echo "  0. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        # [1] UTILISATION QUOTIDIENNE
        1)
            bash "$CMD" summary
            read -p "Press Enter to continue..."
            ;;
        2)
            echo "--- Think ---"
            read -p "Prompt: " prompt
            if [ -n "$prompt" ]; then
                bash "$CMD" think "$prompt"
            fi
            read -p "Press Enter to continue..."
            ;;
        3)
            echo "--- Response ---"
            read -p "Prompt: " prompt
            if [ -n "$prompt" ]; then
                bash "$CMD" response "$prompt"
            fi
            read -p "Press Enter to continue..."
            ;;
        4)
            echo "--- Roadmap Events ---"
            read -p "Max tokens (optional, default 200): " tokens
            bash "$CMD" roadmap-events $tokens
            read -p "Press Enter to continue..."
            ;;
        5)
            echo "--- Roadmap Think Module ---"
            read -p "Module name: " mod
            if [ -n "$mod" ]; then
                bash "$CMD" roadmap-think-module "$mod"
            fi
            read -p "Press Enter to continue..."
            ;;
        6)
            echo "--- Roadmap Response Module ---"
            read -p "Module name: " mod
            if [ -n "$mod" ]; then
                bash "$CMD" roadmap-response-module "$mod"
            fi
            read -p "Press Enter to continue..."
            ;;

        # [2] RÉSULTATS / ARCHIVES
        7)
            bash "$CMD" show-latest-thinking
            read -p "Press Enter to continue..."
            ;;
        8)
            bash "$CMD" show-latest-response
            read -p "Press Enter to continue..."
            ;;
        9)
            bash "$CMD" show-latest-roadmap
            read -p "Press Enter to continue..."
            ;;
        10)
            bash "$CMD" tail-latest-log
            read -p "Press Enter to continue..."
            ;;

        # [3] AUTOMATISATION
        11)
            bash "$CMD" daily-log-thinking
            read -p "Press Enter to continue..."
            ;;
        12)
            bash "$CMD" install-daily-timer
            read -p "Press Enter to continue..."
            ;;
        13)
            bash "$CMD" timer-status
            read -p "Press Enter to continue..."
            ;;
        14)
            bash "$CMD" timer-logs
            read -p "Press Enter to continue..."
            ;;

        # [4] DEV / DEBUG / MAINTENANCE
        15)
            bash "$CMD" sanity
            read -p "Press Enter to continue..."
            ;;
        16)
            bash "$CMD" status
            read -p "Press Enter to continue..."
            ;;
        17)
            bash "$CMD" models
            read -p "Press Enter to continue..."
            ;;
        18)
            bash "$CMD" show-paths
            read -p "Press Enter to continue..."
            ;;
        19)
            bash "$CMD" help
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
