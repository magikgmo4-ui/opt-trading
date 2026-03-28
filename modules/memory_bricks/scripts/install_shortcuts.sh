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
USER_BIN_DIR="${HOME}/.local/bin"
SYSTEM_BIN_DIR="/usr/local/bin"
BIN_DIR="${USER_BIN_DIR}"
USE_SUDO=0

usage() {
  echo "Usage: $(basename "$0") [--user] [--system] [--bin-dir PATH]"
  echo
  echo "Default mode installs shortcuts into ${USER_BIN_DIR} without sudo."
  echo "Use --system to target ${SYSTEM_BIN_DIR}."
}

while (($# > 0)); do
  case "$1" in
    --user)
      BIN_DIR="${USER_BIN_DIR}"
      USE_SUDO=0
      ;;
    --system)
      BIN_DIR="${SYSTEM_BIN_DIR}"
      USE_SUDO=1
      ;;
    --bin-dir)
      shift
      [ $# -gt 0 ] || { echo "ERROR: --bin-dir requires a path" >&2; exit 2; }
      BIN_DIR="$1"
      USE_SUDO=0
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [ "${USE_SUDO}" -eq 1 ]; then
  sudo mkdir -p "${BIN_DIR}"
  sudo ln -sf "${MODULE_DIR}/scripts/cmd.sh" "${BIN_DIR}/cmd-memory_bricks"
  sudo ln -sf "${MODULE_DIR}/scripts/menu.sh" "${BIN_DIR}/menu-memory_bricks"
  sudo ln -sf "${MODULE_DIR}/scripts/sanity_check.sh" "${BIN_DIR}/sanity-memory_bricks"
else
  mkdir -p "${BIN_DIR}"
  ln -sf "${MODULE_DIR}/scripts/cmd.sh" "${BIN_DIR}/cmd-memory_bricks"
  ln -sf "${MODULE_DIR}/scripts/menu.sh" "${BIN_DIR}/menu-memory_bricks"
  ln -sf "${MODULE_DIR}/scripts/sanity_check.sh" "${BIN_DIR}/sanity-memory_bricks"
fi

echo "Installed shortcuts:"
echo "- ${BIN_DIR}/cmd-memory_bricks"
echo "- ${BIN_DIR}/menu-memory_bricks"
echo "- ${BIN_DIR}/sanity-memory_bricks"

case ":${PATH}:" in
  *":${BIN_DIR}:"*)
    echo "PATH already includes ${BIN_DIR}"
    ;;
  *)
    echo "Add ${BIN_DIR} to PATH to call the shortcuts directly."
    ;;
esac
