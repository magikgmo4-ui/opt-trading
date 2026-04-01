#!/usr/bin/env bash
# Generic Menu Runner
# Role: Displays a menu based on a provided .ctx file

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/lib"
DEFAULT_CTX="$SCRIPT_DIR/examples/example.ctx"

# Argument parsing
CTX_FILE="${1:-$DEFAULT_CTX}"

# Validation
if [ ! -f "$CTX_FILE" ]; then
    echo "Error: Context file not found: $CTX_FILE"
    exit 1
fi

if [ ! -d "$LIB_DIR" ]; then
    echo "Error: Library directory not found at $LIB_DIR"
    exit 1
fi

# Load libraries
source "$LIB_DIR/reader.sh"
source "$LIB_DIR/renderer.sh"
source "$LIB_DIR/router.sh"

# Main loop
while true; do
    # Title from filename
    TITLE="Menu: $(basename "$CTX_FILE")"
    
    render_menu "$CTX_FILE" "$TITLE"
    
    read -p "Select option: " choice
    
    if [[ "$choice" == "0" ]]; then
        echo "Exiting."
        exit 0
    fi
    
    if ! route_action "$CTX_FILE" "$choice"; then
        echo "Action failed."
    fi
    
    echo ""
    read -p "Press Enter to continue..."
done
