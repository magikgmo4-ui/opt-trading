#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/app"
INPUT_DIR="$SCRIPT_DIR/inputs"
OUTPUT_DIR="$SCRIPT_DIR/output"

# Python check
PYTHON="python3"
if ! command -v $PYTHON &> /dev/null; then
    PYTHON="python"
fi

cmd="${1:-help}"

case "$cmd" in
    generate)
        mode="${2:-}"
        input_file="${3:-$INPUT_DIR/synthesis_example.txt}"
        
        if [ -z "$mode" ]; then
            echo "Usage: $0 generate <mode> [input_file]"
            echo "Modes: chatgpt_session, trae_module, trae_patch, bundle_transfer"
            exit 1
        fi
        
        "$PYTHON" "$APP_DIR/validated_prompt_factory.py" \
            --input "$input_file" \
            --mode "$mode" \
            --output-dir "$OUTPUT_DIR"
        ;;
    list-modes)
        echo "Available modes:"
        echo "- chatgpt_session"
        echo "- trae_module"
        echo "- trae_patch"
        echo "- bundle_transfer"
        ;;
    validate)
        bash "$SCRIPT_DIR/sanity.sh"
        ;;
    help)
        echo "Usage: $0 {generate|list-modes|validate}"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Usage: $0 {generate|list-modes|validate}"
        exit 1
        ;;
esac
