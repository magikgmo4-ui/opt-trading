#!/usr/bin/env bash
set -euo pipefail

MODULE="${1:-general}"
TITLE="${2:-}"
MESSAGE="${3:-}"

if [[ -z "$TITLE" || -z "$MESSAGE" ]]; then
  echo 'Usage: log_event_to_student.sh <module|general> "<title>" "<message>"'
  echo 'Example: log_event_to_student.sh desk_pro "Fix routes" "Changed /desk/ui endpoint + added sanity check"'
  exit 2
fi

TS="$(TZ=America/Montreal date -Iseconds)"
HOST="$(hostname)"
USER="$(whoami)"

# Minimal JSON escaping (safe enough for our use: replace " with \")
TITLE_ESC="${TITLE//\"/\\\"}"
MESSAGE_ESC="${MESSAGE//\"/\\\"}"

JSON="{\"ts\":\"${TS}\",\"from_host\":\"${HOST}\",\"from_user\":\"${USER}\",\"module\":\"${MODULE}\",\"title\":\"${TITLE_ESC}\",\"message\":\"${MESSAGE_ESC}\"}"

ssh student "mkdir -p /opt/trading/_student_archive/events && \
  echo '${JSON}' >> /opt/trading/_student_archive/events/events.ndjson && \
  echo '${JSON}' >> /opt/trading/_student_archive/events/${MODULE}.ndjson"
echo "==> logged to student: ${MODULE} @ ${TS}"
