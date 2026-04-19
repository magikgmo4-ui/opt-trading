#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
SRC_DIR="$SCRIPT_DIR/src"
PYTHON="python3"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    PYTHON="python"
fi

export PYTHONPATH="$SRC_DIR${PYTHONPATH:+:$PYTHONPATH}"

cmd="${1:-help}"
shift || true

case "$cmd" in
    run)
        "$PYTHON" -m kil_v1.cli run "$@"
        ;;
    audit)
        "$PYTHON" -m kil_v1.cli audit "$@"
        ;;
    sample)
        "$PYTHON" -m kil_v1.cli sample "$@"
        ;;
    help)
        "$PYTHON" -m kil_v1.cli help
        ;;
    *)
        echo "Unknown command: $cmd" >&2
        "$PYTHON" -m kil_v1.cli help
        exit 1
        ;;
esac
