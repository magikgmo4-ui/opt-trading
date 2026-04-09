#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"

cd "$ROOT_DIR" || exit 1

if [ -f "$MODULE_DIR/config/.env" ]; then
    export $(grep -v '^#' "$MODULE_DIR/config/.env" | xargs)
fi

python3 -m modules.derivatives_collector.app.lifecycle_compat "$@"
