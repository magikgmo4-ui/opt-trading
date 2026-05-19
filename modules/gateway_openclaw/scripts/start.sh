#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=/dev/null
source "$BASE/app/gateway_env.sh"

require_target_user
mkdir -p "$LOG_DIR"

if has_session; then
  echo "NOTE: session déjà active: $SESSION"
else
  tmux new-session -d -s "$SESSION" "openclaw gateway run >> '$LOG_FILE' 2>&1"
  echo "PASS: session démarrée: $SESSION"
fi

sleep 2
openclaw gateway health || true
openclaw gateway probe || true
