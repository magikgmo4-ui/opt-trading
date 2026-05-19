#!/usr/bin/env bash
# fleet_orchestrator.sh — wrapper systemd pour fleet_orchestrator.py
set -euo pipefail

TRADING_ROOT="/opt/trading"
MODULE_DIR="$TRADING_ROOT/modules/runtime_health"
MAP_FILE="$TRADING_ROOT/config/machine_runtime_map.yml"
DATA_DIR="$TRADING_ROOT/data/runtime_health"

PYTHON=""
for candidate in \
  "$TRADING_ROOT/venv/bin/python3" \
  "/usr/bin/python3" \
  "python3"
do
  if command -v "$candidate" &>/dev/null || [ -x "$candidate" ]; then
    PYTHON="$candidate"
    break
  fi
done

if [ -z "$PYTHON" ]; then
  echo "FATAL: no python3 found" >&2
  exit 1
fi

mkdir -p "$DATA_DIR"

ARGS=()
if [ -f "$MAP_FILE" ]; then
  ARGS+=(--map "$MAP_FILE")
fi
ARGS+=(--data-dir "$DATA_DIR")

export PYTHONPATH="$TRADING_ROOT${PYTHONPATH:+:$PYTHONPATH}"

exec "$PYTHON" "$MODULE_DIR/fleet_orchestrator.py" "${ARGS[@]}" "$@"
