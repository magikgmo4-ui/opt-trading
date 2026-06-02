#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT/.env}"

load_one_env() {
  local path="$1"
  if [[ -f "$path" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$path"
    set +a
  fi
}

load_one_env "$ENV_FILE"

if [[ "$ENV_FILE" == "$ROOT/.env" ]]; then
  load_one_env "$ROOT/.env.local"
  load_one_env "$ROOT/.env.telegram.local"
fi

: "${TV_PERF_SCHEME:=http}"
: "${TV_PERF_HOST:=127.0.0.1}"
: "${TV_PERF_PORT:=8010}"

export TV_PERF_SCHEME TV_PERF_HOST TV_PERF_PORT
export TV_PERF_BASE_URL="${TV_PERF_SCHEME}://${TV_PERF_HOST}:${TV_PERF_PORT}"
