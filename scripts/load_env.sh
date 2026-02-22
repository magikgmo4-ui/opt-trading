#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT/.env}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

: "${TV_PERF_SCHEME:=http}"
: "${TV_PERF_HOST:=127.0.0.1}"
: "${TV_PERF_PORT:=8010}"

export TV_PERF_SCHEME TV_PERF_HOST TV_PERF_PORT
export TV_PERF_BASE_URL="${TV_PERF_SCHEME}://${TV_PERF_HOST}:${TV_PERF_PORT}"
