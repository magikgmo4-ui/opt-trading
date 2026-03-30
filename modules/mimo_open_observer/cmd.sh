#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
cmd="${1:-help}"

case "$cmd" in
  help)
    cat <<'EOF'
mimo_open_observer (doc pack v0)

Commands:
  help           Show this help
  docs-index     Show docs index path
  sanity         Run doc-pack sanity
EOF
    ;;
  docs-index)
    echo "$SCRIPT_DIR/docs/00_SESSION_INDEX_MIMO_OPEN_OBSERVER_V0.txt"
    ;;
  sanity)
    bash "$SCRIPT_DIR/sanity.sh"
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    exit 1
    ;;
esac
