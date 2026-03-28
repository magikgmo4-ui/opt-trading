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
CMD="${MODULE_DIR}/scripts/cmd.sh"
REPO_ROOT="$(cd "${MODULE_DIR}/../.." && pwd)"
DEFAULT_STATE_ROOT="${REPO_ROOT}/_state/memory_bricks"
ACTIVE_STATE_ROOT="${MEMORY_BRICKS_STATE_ROOT:-${DEFAULT_STATE_ROOT}}"

echo "== memory_bricks menu =="
echo "State root: ${ACTIVE_STATE_ROOT}"
echo "1) Create demo brick"
echo "2) List bricks (legacy)"
echo "3) Rebuild index"
echo "4) Query status"
echo "5) Query list"
echo "6) Query show"
echo "7) Query find"
echo "8) Run sanity"
read -rp "Choice: " choice

case "${choice}" in
  1)
    "${CMD}" new --type resume_point --title "Demo brick" --ia chatgpt --machine admin-trading --surface terminal_linux --project opt-trading --module memory_bricks --status open --summary-short "Demo brick for bootstrap." --resume-point "Inspect generated file."
    ;;
  2)
    "${CMD}" list
    ;;
  3)
    "${CMD}" index rebuild
    ;;
  4)
    "${CMD}" query status
    ;;
  5)
    "${CMD}" query list
    ;;
  6)
    read -rp "Brick ID: " brick_id
    "${CMD}" query show --id "${brick_id}"
    ;;
  7)
    read -rp "Search text: " query_text
    "${CMD}" query find --text "${query_text}"
    ;;
  8)
    "${MODULE_DIR}/scripts/sanity_check.sh"
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac
