#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
LIFECYCLE_CMD="$MODULE_DIR/scripts/lifecycle_compat.sh"

# Resolve root directory
cd "$ROOT_DIR" || exit 1

# Load config if present
if [ -f "$MODULE_DIR/config/.env" ]; then
    export $(grep -v '^#' "$MODULE_DIR/config/.env" | xargs)
fi

usage() {
    echo "Usage: cmd.sh collect|status|sample|export|lifecycle|lifecycle-sample|lifecycle-export|lifecycle-status|menu|sanity"
}

cmd="${1:-help}"
case "$cmd" in
  collect|status|sample|export)
    python3 -m modules.derivatives_collector.app.derivatives_collector "$cmd" "$@"
    ;;
  lifecycle)
    exec bash "$LIFECYCLE_CMD" collect
    ;;
  lifecycle-sample)
    exec bash "$LIFECYCLE_CMD" sample
    ;;
  lifecycle-export)
    exec bash "$LIFECYCLE_CMD" export
    ;;
  lifecycle-status)
    exec bash "$LIFECYCLE_CMD" status
    ;;
  menu)
    exec bash "$MODULE_DIR/scripts/menu.sh"
    ;;
  sanity)
    exec bash "$MODULE_DIR/scripts/sanity_check.sh"
    ;;
  ""|-h|--help|help)
    usage
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac
