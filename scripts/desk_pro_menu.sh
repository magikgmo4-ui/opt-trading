#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# shellcheck disable=SC1091
source ./scripts/load_env.sh
HOST="${HOST:-$TV_PERF_BASE_URL}"

echo "=== Desk Pro menu ==="
echo "BASE URL: $HOST"
echo
echo "1) Sanity check"
echo "2) Curl health"
echo "3) Curl snapshot"
echo "4) Post sample form (SR W/D)"
echo "5) HTTP test"
echo "6) Show module tree"
echo "q) Quit"
read -r -p "> " choice

case "$choice" in
  1) ./scripts/desk_pro_sanity.sh ;;
  2) HOST="$HOST" ./scripts/desk_pro_cmd.sh health ;;
  3) HOST="$HOST" ./scripts/desk_pro_cmd.sh snapshot ;;
  4) HOST="$HOST" ./scripts/desk_pro_cmd.sh form-sample ;;
  5) HOST="$HOST" ./scripts/desk_pro_http_test.sh ;;
  6) ./scripts/desk_pro_cmd.sh tree ;;
  q|Q) exit 0 ;;
  *) echo "unknown"; exit 1 ;;
esac
