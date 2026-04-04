#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=/dev/null
source "$BASE/app/gateway_env.sh"

require_target_user
command -v tmux >/dev/null 2>&1 || fail "tmux introuvable"
command -v openclaw >/dev/null 2>&1 || fail "openclaw introuvable"
command -v node >/dev/null 2>&1 || fail "node introuvable"
mkdir -p "$LOG_DIR"
openclaw config validate >/dev/null

echo "PASS: gateway_openclaw sanity OK"
print_common
