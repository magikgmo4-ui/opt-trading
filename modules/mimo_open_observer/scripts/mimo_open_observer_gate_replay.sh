#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
MODULE_DIR="$(dirname "$SCRIPT_DIR")"
CSV_FILE="${MIMO_GATE_REPLAY_CSV:-$MODULE_DIR/fixtures/sample_xauusd_m1_signal.csv}"

exec bash "$MODULE_DIR/cmd.sh" gate_replay --csv "$CSV_FILE" "$@"
