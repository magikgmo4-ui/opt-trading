#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/lib"
CTX_FILE="$SCRIPT_DIR/examples/example.ctx"
# Modules root is the parent directory of this module
MODULES_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check libs
if [ ! -d "$LIB_DIR" ]; then
    echo "Error: Library directory not found at $LIB_DIR"
    exit 1
fi

source "$LIB_DIR/reader.sh"
source "$LIB_DIR/renderer.sh"
source "$LIB_DIR/discovery.sh"

case "${1:-help}" in
    status)
        echo "Module: module_contextuals_shell"
        echo "Status: Active"
        echo "Version: V2 (Discovery Enabled)"
        echo "Contexts: $(ls "$SCRIPT_DIR/examples/"*.ctx 2>/dev/null | wc -l || echo 0)"
        echo "Libraries: $(ls "$LIB_DIR/"*.sh 2>/dev/null | wc -l || echo 0)"
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
    # V2 Discovery Commands
    discover)
        echo "Discovering modules in $MODULES_ROOT..."
        echo "----------------------------------------"
        # Using a subshell to iterate over the result of discover_modules function
        # But discover_modules prints to stdout. We can just loop over the output.
        for mod in $(discover_modules "$MODULES_ROOT"); do
            inspect_module "$mod" "$MODULES_ROOT"
            echo "----------------------------------------"
        done
        ;;
    list-modules)
        discover_modules "$MODULES_ROOT"
        ;;
    show-module)
        if [ -z "$2" ]; then
            echo "Usage: $0 show-module <module_name>"
            exit 1
        fi
        inspect_module "$2" "$MODULES_ROOT"
        ;;
    show-scripts)
        if [ -z "$2" ]; then
            echo "Usage: $0 show-scripts <module_name>"
            exit 1
        fi
        list_module_scripts "$2" "$MODULES_ROOT"
        ;;
    show-contextuals)
        if [ -z "$2" ]; then
            echo "Usage: $0 show-contextuals <module_name>"
            exit 1
        fi
        list_module_contextuals "$2" "$MODULES_ROOT"
        ;;
    show-commands)
        if [ -z "$2" ]; then
            echo "Usage: $0 show-commands <module_name>"
            exit 1
        fi
        list_module_commands "$2" "$MODULES_ROOT"
        ;;
    help)
        echo "Usage: $0 {status|list|validate|demo|discover|list-modules|show-module|show-scripts|show-contextuals|show-commands}"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Usage: $0 {status|list|validate|demo|discover|list-modules|show-module|show-scripts|show-contextuals|show-commands}"
        exit 1
        ;;
esac
