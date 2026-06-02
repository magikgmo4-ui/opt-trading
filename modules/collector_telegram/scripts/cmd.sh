#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
MODULE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd -- "$MODULE_DIR/../.." && pwd)
PYTHON_BIN="python3"

if [ -x "$REPO_ROOT/venv/bin/python" ]; then
  PYTHON_BIN="$REPO_ROOT/venv/bin/python"
fi

export PYTHONPATH="$REPO_ROOT:$MODULE_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

usage() {
  cat <<'EOF'
Usage: cmd.sh <command> [options]

Commands:
  sanity              Validate config and Telegram runtime prerequisites
  run [--channel A]   Run live collection for enabled channels or one alias
  status              Print outputs/status.json if available
  test                Run collector unit tests
EOF
}

command=${1:-}
shift || true

case "$command" in
  sanity)
    exec "$PYTHON_BIN" -m collector_telegram.cli --module-dir "$MODULE_DIR" sanity "$@"
    ;;
  run)
    exec "$PYTHON_BIN" -m collector_telegram.cli --module-dir "$MODULE_DIR" "$@" run
    ;;
  status)
    exec "$PYTHON_BIN" -m collector_telegram.cli --module-dir "$MODULE_DIR" status "$@"
    ;;
  test)
    exec "$PYTHON_BIN" -m pytest "$MODULE_DIR/tests"
    ;;
  ""|-h|--help|help)
    usage
    ;;
  *)
    echo "Unknown command: $command" >&2
    usage >&2
    exit 1
    ;;
esac
