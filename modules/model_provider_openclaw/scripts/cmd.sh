#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
APP="$BASE_DIR/app/model_provider_openclaw.py"

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") status
  $(basename "$0") sanity
  $(basename "$0") show-agent <agent>
  $(basename "$0") export-json
USAGE
}

cmd="${1:-}"
case "$cmd" in
  status)
    exec "$PYTHON_BIN" "$APP" status
    ;;
  sanity)
    exec "$PYTHON_BIN" "$APP" sanity
    ;;
  show-agent)
    shift || true
    exec "$PYTHON_BIN" "$APP" show-agent "${1:-}"
    ;;
  export-json)
    exec "$PYTHON_BIN" "$APP" export-json
    ;;
  *)
    usage
    exit 1
    ;;
esac
