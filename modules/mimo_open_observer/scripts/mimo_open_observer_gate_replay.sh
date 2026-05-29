#!/usr/bin/env bash
set -euo pipefail

if [[ "${MIMO_OPEN_OBSERVER_ALLOW_ARCHIVED_RUNTIME:-0}" != "1" ]]; then
  cat >&2 <<'EOF'
MIMO Open Observer gate_replay is archived residual runtime.
Scheduler entrypoints are disabled by default.

If you explicitly need this residual behavior:
  MIMO_OPEN_OBSERVER_ALLOW_ARCHIVED_RUNTIME=1 bash modules/mimo_open_observer/scripts/mimo_open_observer_gate_replay.sh ...

See:
  modules/mimo_open_observer/LEGACY.md
EOF
  exit 2
fi

SOURCE_PATH="${BASH_SOURCE[0]}"
while [ -h "${SOURCE_PATH}" ]; do
  SOURCE_DIR="$(cd -P "$(dirname "${SOURCE_PATH}")" && pwd)"
  LINK_TARGET="$(readlink "${SOURCE_PATH}")"
  if [[ "${LINK_TARGET}" != /* ]]; then
    SOURCE_PATH="${SOURCE_DIR}/${LINK_TARGET}"
  else
    SOURCE_PATH="${LINK_TARGET}"
  fi
done

SCRIPT_DIR="$(cd -P "$(dirname "${SOURCE_PATH}")" && pwd)"
MODULE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEFAULT_CSV="${MODULE_DIR}/fixtures/sample_xauusd_m1_signal.csv"
CSV_PATH="${MIMO_GATE_REPLAY_CSV:-${DEFAULT_CSV}}"

if [[ ! -f "${CSV_PATH}" ]]; then
  echo "ERROR: MiMo gate_replay CSV not found: ${CSV_PATH}" >&2
  exit 1
fi

exec bash "${MODULE_DIR}/cmd.sh" gate_replay --csv "${CSV_PATH}" "$@"
