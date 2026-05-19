#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/../app"
MODULES_DIR="$SCRIPT_DIR/../.."

# Python check
PYTHON="python3"
if ! command -v $PYTHON &> /dev/null; then
    PYTHON="python"
fi

cmd="${1:-help}"

case "$cmd" in
    status)
        $PYTHON "$APP_DIR/registry_router.py" status
        ;;
    show-entries)
        $PYTHON "$APP_DIR/registry_router.py" show-entries
        ;;
    open-meta)
        bash "$MODULES_DIR/registry_meta_reader/scripts/cmd.sh" list
        ;;
    open-machines)
        bash "$MODULES_DIR/machines_registry_reader/scripts/cmd.sh" list
        ;;
    open-modules)
        bash "$MODULES_DIR/modules_registry_reader/scripts/cmd.sh" list
        ;;
    open-ui)
        bash "$MODULES_DIR/ui_registry_msi/scripts/cmd.sh" list
        ;;
    open-wrappers)
        bash "$MODULES_DIR/wrappers_registry_reader/scripts/cmd.sh" list
        ;;
    *)
        echo "Usage: $0 {status|show-entries|open-meta|open-machines|open-modules|open-ui|open-wrappers}"
        exit 1
        ;;
esac
