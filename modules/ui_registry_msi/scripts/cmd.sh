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
        $PYTHON "$APP_DIR/ui_registry_msi.py" status
        ;;
    list)
        $PYTHON "$APP_DIR/ui_registry_msi.py" list
        ;;
    show-machines)
        $PYTHON "$APP_DIR/ui_registry_msi.py" show-machines
        ;;
    show-categories)
        $PYTHON "$APP_DIR/ui_registry_msi.py" show-categories
        ;;
    show-msi)
        $PYTHON "$APP_DIR/ui_registry_msi.py" show-msi
        ;;
    export-json)
        $PYTHON "$APP_DIR/ui_registry_msi.py" export-json
        ;;
    export-md)
        $PYTHON "$APP_DIR/ui_registry_msi.py" export-md
        ;;
    *)
        echo "Usage: $0 {status|list|show-machines|show-categories|show-msi|export-json|export-md}"
        exit 1
        ;;
esac
