#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT_PATH="$(readlink -f "$SCRIPT_PATH" 2>/dev/null || echo "$SCRIPT_PATH")"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

fail=0

check() {
  local name="${1:-}"
  shift || true
  if "$@"; then
    echo "PASS: $name"
  else
    echo "FAIL: $name"
    fail=1
  fi
}

share_base="$(bash "$CMD" path 2>/dev/null | awk -F= '/^share_base=/{print $2}')"
check "share base detected" test -n "${share_base:-}"
if [[ -n "${share_base:-}" ]]; then
  check "share base dir exists" test -d "$share_base"
  check "boot_test readable" test -r "$share_base/boot_test.txt"
fi

exit "$fail"

