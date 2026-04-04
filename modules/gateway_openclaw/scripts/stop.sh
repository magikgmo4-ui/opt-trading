#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=/dev/null
source "$BASE/app/gateway_env.sh"

require_target_user

if has_session; then
  tmux kill-session -t "$SESSION"
  echo "PASS: session stoppée: $SESSION"
else
  echo "NOTE: aucune session active: $SESSION"
fi
