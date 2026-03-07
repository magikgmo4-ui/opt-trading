#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Release Menu (Linux)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

while true; do
    clear
    echo "=== DESK PRO RELEASE OPS MENU ==="
    echo "Repo Root: $ROOT_DIR"
    echo ""
    echo "1. Sanity Check"
    echo "2. Verify Tag"
    echo "3. Show Current HEAD"
    echo "4. Show Recent Tags"
    echo ""
    echo "0. Quit"
    echo "================================="
    read -p "Select option: " choice

    case $choice in
        1)
            bash "$SCRIPT_DIR/desk_pro_release_sanity_check.sh"
            read -p "Press Enter to continue..."
            ;;
        2)
            read -p "Enter Tag Name: " tag
            bash "$SCRIPT_DIR/desk_pro_verify_tag_linux.sh" "$tag"
            read -p "Press Enter to continue..."
            ;;
        3)
            echo "Current HEAD:"
            git show --no-patch --format="%h %cd %s"
            read -p "Press Enter to continue..."
            ;;
        4)
            echo "Recent Tags:"
            git tag -n1 --sort=-v:refname | head -n 10
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
