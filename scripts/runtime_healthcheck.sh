#!/usr/bin/env bash
# runtime_healthcheck.sh — wrapper systemd pour healthcheck.py
set -euo pipefail

TRADING_ROOT="/opt/trading"
MODULE_DIR="$TRADING_ROOT/modules/runtime_health"
CONFIG_FILE="$MODULE_DIR/config/runtime_health.yml"
MAP_FILE="$TRADING_ROOT/config/machine_runtime_map.yml"
DATA_DIR="$TRADING_ROOT/data/runtime_health"

# Resolution Python : garder le venv seulement s'il charge PyYAML.
# La machine map depend de yaml ; sans lui le healthcheck retombe sur un
# scope vide/default et STEP 5 reste WARN.
PYTHON=""
PYTHON_REJECTS=()
for candidate in \
  "$TRADING_ROOT/venv/bin/python3" \
  "/usr/bin/python3" \
  "python3"
do
  if command -v "$candidate" &>/dev/null || [ -x "$candidate" ]; then
    if "$candidate" -c "import yaml" >/dev/null 2>&1; then
      PYTHON="$candidate"
      break
    fi
    PYTHON_REJECTS+=("$candidate (missing yaml)")
  fi
done

if [ -z "$PYTHON" ]; then
  echo "FATAL: no python3 with PyYAML found" >&2
  if [ "${#PYTHON_REJECTS[@]}" -gt 0 ]; then
    printf 'Rejected python candidates:\n' >&2
    printf ' - %s\n' "${PYTHON_REJECTS[@]}" >&2
  fi
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
