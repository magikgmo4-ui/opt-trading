#!/usr/bin/env bash
# runtime_healthcheck.sh — wrapper systemd pour healthcheck.py
set -euo pipefail

TRADING_ROOT="/opt/trading"
MODULE_DIR="$TRADING_ROOT/modules/runtime_health"
CONFIG_FILE="$MODULE_DIR/config/runtime_health.yml"
MAP_FILE="$TRADING_ROOT/config/machine_runtime_map.yml"
DATA_DIR="$TRADING_ROOT/data/runtime_health"

# Résolution Python : venv principal, fallback système
PYTHON=""
for candidate in \
  "$TRADING_ROOT/venv/bin/python3" \
  "$TRADING_ROOT/.venvs/bot_vision_step2/bin/python3" \
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

# MACHINE_ROLE peut être forcé via env (ex: systemd EnvironmentFile)
MACHINE_ARGS=()
if [ -n "${MACHINE_ROLE:-}" ]; then
  MACHINE_ARGS+=(--machine "$MACHINE_ROLE")
fi
if [ -f "$MAP_FILE" ]; then
  MACHINE_ARGS+=(--map "$MAP_FILE")
fi

export PYTHONPATH="$TRADING_ROOT${PYTHONPATH:+:$PYTHONPATH}"

exec "$PYTHON" "$MODULE_DIR/healthcheck.py" \
  --config "$CONFIG_FILE" \
  "${MACHINE_ARGS[@]}" \
  "$@"
