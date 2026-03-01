#!/usr/bin/env bash
set -euo pipefail

need_root() {
  if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
    echo "ERROR: run as root (sudo)." >&2
    exit 1
  fi
}

run_to_file() {
  local out="$1"; shift
  local cmd="$*"
  {
    echo "### CMD: $cmd"
    echo "### TIME: $(date -Is)"
    echo
    bash -lc "$cmd" 2>&1 || true
  } > "$out"
}

sanitize_wg_conf() {
  local in="$1"
  local out="$2"
  sed -E 's/^(PrivateKey\s*=\s*).+$/\1REDACTED/' "$in" > "$out"
}
