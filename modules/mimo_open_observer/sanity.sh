#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

required=(
  "$SCRIPT_DIR/README.md"
  "$SCRIPT_DIR/docs/00_SESSION_INDEX_MIMO_OPEN_OBSERVER_V0.txt"
  "$SCRIPT_DIR/docs/06_PSEUDOCODE_PACK_MIMO_OPEN_OBSERVER_V0.md"
  "$SCRIPT_DIR/config/mimo_open_observer.yaml"
  "$SCRIPT_DIR/registry_patch/modules_registry.entry.yaml"
  "$SCRIPT_DIR/registry_patch/wrappers_registry.entries.yaml"
)

for p in "${required[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing: $p" >&2; exit 1; }
done

echo "PASS: mimo_open_observer doc pack v0 sanity OK"
