#!/usr/bin/env bash
set -euo pipefail

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
PORT="${MEMORY_BRICKS_API_V2_PORT:-8112}"
HOST="${MEMORY_BRICKS_API_V2_HOST:-127.0.0.1}"

echo "Starting memory_bricks API V2 (read-only) on ${HOST}:${PORT}"
echo "Source root: ${MEMORY_BRICKS_STATE_ROOT:-_state/memory_bricks}"
echo ""
echo "Endpoints:"
echo "  GET http://${HOST}:${PORT}/health"
echo "  GET http://${HOST}:${PORT}/status"
echo ""
echo "Press Ctrl+C to stop."
echo ""

python3 "${MODULE_DIR}/app/api_v2_server.py"
