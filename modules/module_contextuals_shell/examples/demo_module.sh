#!/usr/bin/env bash
# Example script showing how to use the context shell library

# 1. Resolve paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LIB_DIR="$MODULE_ROOT/lib"
CTX_FILE="$MODULE_ROOT/examples/example.ctx"

# 2. Source libraries
# Ensure we can find the libs
if [ ! -d "$LIB_DIR" ]; then
    echo "Error: Library directory not found at $LIB_DIR"
    exit 1
fi

source "$LIB_DIR/reader.sh"
source "$LIB_DIR/renderer.sh"
source "$LIB_DIR/router.sh"

# 3. Define local functions used in context
demo_hello() {
    echo "Bonjour ! Ceci est une fonction locale définie dans le script appelant."
}

# 4. Main loop
main() {
    echo "=== Demo Module Contextuals ==="
    echo "Reading context from: $CTX_FILE"
    
    while true; do
        # Render menu
        render_menu "$CTX_FILE" "Menu Démo"
        
        # Read user input
        read -p "Votre choix : " choice
        
        # Handle exit
        if [[ "$choice" == "0" ]]; then
            echo "Au revoir."
            exit 0
        fi
        
        # Route action
        # Note: route_action iterates again to find the N-th item
        if ! route_action "$CTX_FILE" "$choice"; then
            echo "Action failed or invalid selection."
        fi
        
        echo ""
        read -p "Appuyez sur Entrée..."
    done
}

main "$@"
