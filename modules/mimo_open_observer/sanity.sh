#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

required=(
  "$SCRIPT_DIR/README.md"
  "$SCRIPT_DIR/LEGACY.md"
  "$SCRIPT_DIR/docs/00_SESSION_INDEX_MIMO_OPEN_OBSERVER_V0.txt"
  "$SCRIPT_DIR/config/mimo_open_observer.yaml"
  "$SCRIPT_DIR/registry_patch/modules_registry.entry.yaml"
  "$SCRIPT_DIR/registry_patch/wrappers_registry.entries.yaml"
  "$SCRIPT_DIR/scripts/mimo_open_observer_gate_replay.sh"
  "$SCRIPT_DIR/systemd/mimo_open_observer_gate_replay.service"
  "$SCRIPT_DIR/systemd/mimo_open_observer_gate_replay.timer"
)

for p in "${required[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing archival asset: $p" >&2; exit 1; }
done

if grep -q "archival residue" "$SCRIPT_DIR/README.md"; then
  echo "PASS: README marks archival residue"
else
  echo "FAIL: README does not mark archival residue" >&2
  exit 1
fi

if grep -q "MIMO_OPEN_OBSERVER_ALLOW_ARCHIVED_RUNTIME=1" "$SCRIPT_DIR/LEGACY.md"; then
  echo "PASS: LEGACY.md documents explicit runtime override"
else
  echo "FAIL: LEGACY.md missing runtime override guidance" >&2
  exit 1
fi

echo "PASS: MIMO OPEN OBSERVER archival sanity OK"
