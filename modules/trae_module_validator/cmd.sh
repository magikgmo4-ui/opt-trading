#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="$SCRIPT_DIR/scripts/validate_module.sh"
MODULES_ROOT="$SCRIPT_DIR/.."

# Python check
PYTHON="python3"
if ! command -v $PYTHON &> /dev/null; then
    PYTHON="python"
fi

cmd="${1:-help}"

case "$cmd" in
    validate)
        module_name="${2:-}"
        if [ -z "$module_name" ]; then
            echo "Usage: $0 validate <module_name>"
            exit 1
        fi
        
        target_path="$MODULES_ROOT/$module_name"
        if [ ! -d "$target_path" ]; then
            echo "Error: Module not found: $module_name"
            exit 1
        fi
        
        bash "$VALIDATOR" "$target_path"
        ;;
    validate-all)
        echo "Validating all modules..."
        for d in "$MODULES_ROOT"/*/; do
            if [ -d "$d" ]; then
                mod_name=$(basename "$d")
                # Filter out hidden/technical dirs
                if [[ "$mod_name" == .* ]] || [[ "$mod_name" == __* ]] || [[ "$mod_name" == "scripts" ]]; then
                    continue
                fi
                echo "--- Checking $mod_name ---"
                bash "$VALIDATOR" "$d"
                echo ""
            fi
        done
        ;;
    help)
        echo "Usage: $0 {validate|validate-all}"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Usage: $0 {validate|validate-all}"
        exit 1
        ;;
esac
