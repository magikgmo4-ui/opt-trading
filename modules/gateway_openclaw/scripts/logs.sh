#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=/dev/null
source "$BASE/app/gateway_env.sh"

require_target_user
mkdir -p "$LOG_DIR"
tail -n "$TAIL_LINES" "$LOG_FILE"
