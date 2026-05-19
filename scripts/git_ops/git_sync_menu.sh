#!/usr/bin/env bash
set -euo pipefail
# Git Sync Menu (Linux)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

while true; do
    clear
    echo "=== GIT SYNC MENU ==="
    echo "Repo: $ROOT_DIR"
    echo ""
    echo "1. Sanity Check"
    echo "2. Show Git Status"
    echo "3. Pull Update"
    echo "4. Pull Update With Restore Paths"
    echo "5. Show Last Commit"
    echo ""
    echo "0. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1)
            bash "$SCRIPT_DIR/git_sync_sanity_check.sh"
            read -p "Press Enter to continue..."
            ;;
        2)
            git status --short
            read -p "Press Enter to continue..."
            ;;
        3)
            bash "$SCRIPT_DIR/git_pull_update_linux.sh"
            read -p "Press Enter to continue..."
            ;;
        4)
            echo "Enter paths to restore (space-separated):"
            read -p "Paths: " paths
            if [ -n "$paths" ]; then
                bash "$SCRIPT_DIR/git_pull_update_linux.sh" --paths $paths
            else
                echo "No paths entered. Pulling only."
                bash "$SCRIPT_DIR/git_pull_update_linux.sh"
            fi
            read -p "Press Enter to continue..."
            ;;
        5)
            echo "Last Commit:"
            git log -1 --oneline --no-decorate --color=always
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
