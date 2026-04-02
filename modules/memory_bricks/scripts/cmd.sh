#!/usr/bin/env bash
set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${MODULE_DIR}:${PYTHONPATH:-}"

python3 "${MODULE_DIR}/app/cli.py" "$@"
