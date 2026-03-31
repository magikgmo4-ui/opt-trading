#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
MODULE_DIR="$(dirname "$SCRIPT_DIR")"
exec bash "$MODULE_DIR/sanity.sh" "$@"
