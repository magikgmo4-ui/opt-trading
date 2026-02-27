#!/usr/bin/env bash
set -euo pipefail
MODULE="${1:-}"
TITLE="${2:-}"
MESSAGE="${3:-}"

if [[ -z "$MODULE" || -z "$TITLE" || -z "$MESSAGE" ]]; then
  echo 'Usage: push_and_log.sh <module> "<title>" "<message>"'
  exit 2
fi

/opt/trading/scripts/push_module_to_student.sh "$MODULE"
/opt/trading/scripts/log_event_to_student.sh "$MODULE" "$TITLE" "$MESSAGE"
