#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Admin Trading - CMD Wrapper
# Delegates to desk_pro_runner via the python module

# Resolve root relative to script
# This script is in scripts/admin_trading/
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR" || exit 1

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found."
    exit 1
fi

cmd="${1:-help}"

case "$cmd" in
  status|run|run-and-show|dashboard-latest|export-json-latest|export-html-latest|explain)
    # Standard runner commands
    python3 -m modules.desk_pro_runner.app.desk_pro_runner "$cmd" "${@:2}"
    ;;
  copy-latest-to-shared)
    # Custom admin helper
    bash "$SCRIPT_DIR/desk_pro_copy_latest_to_shared.sh"
    ;;
  *)
    echo "Usage: desk_pro_cmd.sh status|run|run-and-show|dashboard-latest|export-json-latest|export-html-latest|copy-latest-to-shared|explain"
    exit 1
    ;;
esac
