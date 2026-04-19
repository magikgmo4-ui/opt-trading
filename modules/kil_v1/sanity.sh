#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
WORKSPACE="$(mktemp -d)"
trap 'rm -rf "$WORKSPACE"' EXIT

bash "$SCRIPT_DIR/cmd.sh" help >/dev/null
bash "$SCRIPT_DIR/cmd.sh" sample --workspace "$WORKSPACE" >/dev/null

if [ ! -f "$WORKSPACE/sqlite/kil_v1.db" ]; then
    echo "sanity failed: sqlite/kil_v1.db missing" >&2
    exit 1
fi

echo "kil_v1 sanity ok"
