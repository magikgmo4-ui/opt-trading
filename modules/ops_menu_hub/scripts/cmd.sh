#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
H="$BASE/ops_menu_hub.sh"

usage() {
  cat <<'EOF'
Usage: cmd.sh <command>

Commands:
  list
  shortcuts
  bootstrap_shortcuts
  run <module>
EOF
}

CMD="${1:-}"
[ -z "$CMD" ] && { usage; exit 1; }

case "$CMD" in
  list) bash "$H" list ;;
  shortcuts) bash "$H" shortcuts ;;
  bootstrap_shortcuts) bash "$H" bootstrap_shortcuts ;;
  run) bash "$H" run "${2:-}" ;;
  *) echo "Unknown: $CMD"; usage; exit 1 ;;
esac
