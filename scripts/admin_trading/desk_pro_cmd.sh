#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Admin Trading - CMD Wrapper
# Delegates to desk_pro_runner via the python module

# Resolve root relative to script (even if symlinked)
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
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
  run-logged)
    # Custom admin helper
    bash "$SCRIPT_DIR/desk_pro_run_logged.sh"
    ;;
  tail-latest-log)
    # Custom admin helper
    bash "$SCRIPT_DIR/desk_pro_tail_latest_log.sh"
    ;;
  last-run-info)
    # Custom admin helper
    bash "$SCRIPT_DIR/desk_pro_last_run_info.sh"
    ;;
  show-session-journal)
    bash "$SCRIPT_DIR/desk_pro_session_journal.sh" show
    ;;
  add-session-note)
    bash "$SCRIPT_DIR/desk_pro_session_journal.sh" add-entry "${2:-}"
    ;;
  *)
    echo "Usage: desk_pro_cmd.sh status|run|run-and-show|dashboard-latest|export-json-latest|export-html-latest|copy-latest-to-shared|run-logged|tail-latest-log|last-run-info|show-session-journal|add-session-note|explain"
    exit 1
    ;;
esac
