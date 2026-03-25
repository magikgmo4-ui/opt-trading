#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
MODULE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd -- "$MODULE_DIR/../.." && pwd)

if [ -f "$MODULE_DIR/config/secrets.local.env" ]; then
  set -a
  . "$MODULE_DIR/config/secrets.local.env"
  set +a
fi

export PYTHONPATH="$REPO_ROOT/packages/collectors_core/src:$MODULE_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

usage() {
  cat <<'EOF'
Usage: collector_coingecko_cmd.sh <command>

Approved secret mechanisms:
  export COLLECTOR_COINGECKO__API__KEY=...
  or place COLLECTOR_COINGECKO__API__KEY=... in config/secrets.local.env

Commands:
  sanity   Run config checks and CoinGecko /ping
  run      Run the oneshot CoinGecko collection
  status   Print outputs/status.json if available
  test     Run unit tests
EOF
}

command=${1:-}
case "$command" in
  sanity)
    exec "$SCRIPT_DIR/sanity_check.sh"
    ;;
  run)
    exec python3 -m collector_coingecko.cli --module-dir "$MODULE_DIR" run
    ;;
  status)
    exec python3 -m collector_coingecko.cli --module-dir "$MODULE_DIR" status
    ;;
  test)
    if python3 -c 'import pytest' >/dev/null 2>&1; then
      exec python3 -m pytest "$MODULE_DIR/tests"
    fi
    exec python3 -m unittest discover -s "$MODULE_DIR/tests" -p 'test_*.py'
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
