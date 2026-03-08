#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/lib"
CTX_FILE="$SCRIPT_DIR/examples/example.ctx"

# Check libs
if [ ! -d "$LIB_DIR" ]; then
    echo "Error: Library directory not found at $LIB_DIR"
    exit 1
fi

source "$LIB_DIR/reader.sh"
source "$LIB_DIR/renderer.sh"

case "${1:-help}" in
    status)
        echo "Module: module_contextuals_shell"
        echo "Status: Active"
        echo "Contexts: $(ls "$SCRIPT_DIR/examples/"*.ctx | wc -l 2>/dev/null || echo 0)"
        echo "Libraries: $(ls "$LIB_DIR/"*.sh | wc -l 2>/dev/null || echo 0)"
        ;;
    list-actions)
        echo "Listing actions from example context:"
        render_menu "$CTX_FILE" "Example Actions"
        ;;
    list)
        echo "Listing actions from example context:"
        render_menu "$CTX_FILE" "Example Actions"
        ;;
    validate)
        bash "$SCRIPT_DIR/sanity.sh"
        ;;
    demo)
        bash "$SCRIPT_DIR/menu.sh"
        ;;
    help)
        echo "Usage: $0 {status|list|validate|demo}"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Usage: $0 {status|list|validate|demo}"
        exit 1
        ;;
esac
