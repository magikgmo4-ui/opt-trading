#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/../app"

# Python check
PYTHON="python3"
if ! command -v $PYTHON &> /dev/null; then
    PYTHON="python"
fi

cmd="${1:-help}"

case "$cmd" in
    status)
        $PYTHON "$APP_DIR/wrappers_registry_reader.py" status
        ;;
    list)
        $PYTHON "$APP_DIR/wrappers_registry_reader.py" list
        ;;
    show-families)
        $PYTHON "$APP_DIR/wrappers_registry_reader.py" show-families
        ;;
    show)
        if [ -z "${2:-}" ]; then
            echo "Usage: $0 show <wrapper_name>"
            exit 1
        fi
        $PYTHON "$APP_DIR/wrappers_registry_reader.py" show "$2"
        ;;
    export-json)
        $PYTHON "$APP_DIR/wrappers_registry_reader.py" export-json
        ;;
    *)
        echo "Usage: $0 {status|list|show-families|show <wrapper>|export-json}"
        exit 1
        ;;
esac
