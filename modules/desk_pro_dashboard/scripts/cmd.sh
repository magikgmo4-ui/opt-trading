#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"

# Resolve root directory
cd "$ROOT_DIR" || exit 1

# Load config if present
if [ -f "$MODULE_DIR/config/.env" ]; then
    export $(grep -v '^#' "$MODULE_DIR/config/.env" | xargs)
fi

cmd="${1:-help}"
case "$cmd" in
  status|sample|render|render-latest|render-run|export-json|export-html)
    python3 -m modules.desk_pro_dashboard.app.desk_pro_dashboard "$cmd" "${@:2}"
    ;;
  menu)
    exec bash "$MODULE_DIR/scripts/menu.sh"
    ;;
  sanity)
    exec bash "$MODULE_DIR/scripts/sanity_check.sh"
    ;;
  *)
    echo "Usage: cmd.sh status|sample|render|render-latest|render-run|export-json|export-html|menu|sanity"
    exit 1
    ;;
esac
