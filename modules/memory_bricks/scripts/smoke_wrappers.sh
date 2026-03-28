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
INSTALL_SCRIPT="${MODULE_DIR}/scripts/install_shortcuts.sh"

TMP_HOME="$(mktemp -d)"
LOCAL_BIN="${TMP_HOME}/.local/bin"
READONLY_ROOT="${TMP_HOME}/readonly-root"
trap 'rm -rf "${TMP_HOME}"' EXIT

fail() {
  echo "FAIL: $1" >&2
  exit 2
}

expect_contains() {
  local haystack="$1"
  local needle="$2"
  case "${haystack}" in
    *"${needle}"*) ;;
    *) fail "expected output to contain: ${needle}" ;;
  esac
}

expect_symlink() {
  local path="$1"
  [ -L "${path}" ] || fail "expected symlink: ${path}"
}

install_output="$(HOME="${TMP_HOME}" PATH="/usr/bin:/bin" bash "${INSTALL_SCRIPT}")"
expect_contains "${install_output}" "Installed shortcuts:"
expect_contains "${install_output}" "${LOCAL_BIN}/cmd-memory_bricks"
expect_contains "${install_output}" "${LOCAL_BIN}/menu-memory_bricks"
expect_contains "${install_output}" "${LOCAL_BIN}/sanity-memory_bricks"

expect_symlink "${LOCAL_BIN}/cmd-memory_bricks"
expect_symlink "${LOCAL_BIN}/menu-memory_bricks"
expect_symlink "${LOCAL_BIN}/sanity-memory_bricks"

export HOME="${TMP_HOME}"
export PATH="${LOCAL_BIN}:/usr/bin:/bin"
export MEMORY_BRICKS_STATE_ROOT="${READONLY_ROOT}"

cmd_output="$(cmd-memory_bricks query status)"
expect_contains "${cmd_output}" "ROOT: ${READONLY_ROOT}"
expect_contains "${cmd_output}" "ROOT_EXISTS: no"

menu_output="$(printf '4\n' | menu-memory_bricks)"
expect_contains "${menu_output}" "== memory_bricks menu =="
expect_contains "${menu_output}" "ROOT_EXISTS: no"

sanity_output="$(sanity-memory_bricks)"
expect_contains "${sanity_output}" "PASS: memory_bricks sanity OK"

echo "PASS: memory_bricks wrappers smoke OK"
