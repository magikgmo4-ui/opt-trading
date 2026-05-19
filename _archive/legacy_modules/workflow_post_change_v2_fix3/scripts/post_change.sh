#!/usr/bin/env bash
set -euo pipefail

MODULE="${1:-}"
TITLE="${2:-}"
MESSAGE="${3:-}"

shift || true; shift || true; shift || true

NO_DEEPSEEK=0
NO_STUDENT_COPY=0
NO_PUSH=0
MODEL="deepseek-r1:1.5b"
N="20"

while [ "${1:-}" != "" ]; do
  case "$1" in
    --no-deepseek) NO_DEEPSEEK=1; shift ;;
    --no-student-copy) NO_STUDENT_COPY=1; shift ;;
    --no-push) NO_PUSH=1; shift ;;
    --model) MODEL="${2:-$MODEL}"; shift 2 ;;
    --n) N="${2:-$N}"; shift 2 ;;
    -h|--help)
      echo "Usage: cmd-post_change <module> \"Title\" \"Message\" [--no-deepseek] [--no-student-copy] [--no-push] [--model MODEL] [--n N]"
      exit 0 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

if [ -z "$MODULE" ] || [ -z "$TITLE" ] || [ -z "$MESSAGE" ]; then
  echo "FAIL: missing args."; exit 2
fi

BASE="/opt/trading"
HOST="$(hostname)"
USER_NAME="$(id -un)"
TS_ISO="$(TZ=America/Montreal date -Iseconds)"
TS_FILE="$(TZ=America/Montreal date +%Y%m%d_%H%M%S)"

JDIR="$BASE/journal/steps"
mkdir -p "$JDIR"
ENTRY="$JDIR/step_${TS_FILE}_${MODULE}.md"

JOURNAL_BLOCK=""
if [ ! -t 0 ]; then JOURNAL_BLOCK="$(cat || true)"; fi

cat >"$ENTRY" <<EOF
# Step — ${MODULE} — ${TS_ISO}

## Meta
- from_host: ${HOST}
- from_user: ${USER_NAME}
- module: ${MODULE}
- title: ${TITLE}

## Message
${MESSAGE}

## Journal (structured)
EOF

if [ -n "${JOURNAL_BLOCK// /}" ]; then
  printf "%s\n" "$JOURNAL_BLOCK" >>"$ENTRY"
else
  echo "*(no extra journal block provided)*" >>"$ENTRY"
fi

echo "OK: wrote journal entry: $ENTRY"

LOG_SCRIPT="$BASE/scripts/log_event_to_student.sh"
PUSH_SCRIPT="$BASE/scripts/push_and_log.sh"
DID_LOG=0

if [ $NO_PUSH -eq 0 ] && [ -x "$PUSH_SCRIPT" ] && [ -d "$BASE/modules/$MODULE" ]; then
  "$PUSH_SCRIPT" "$MODULE" "$TITLE" "$MESSAGE" >/dev/null
  DID_LOG=1
fi

if [ $DID_LOG -eq 0 ]; then
  if [ -x "$LOG_SCRIPT" ]; then "$LOG_SCRIPT" "$MODULE" "$TITLE" "$MESSAGE" >/dev/null
  else echo "WARN: log_event_to_student.sh missing; skipping ndjson log"; fi
fi

# FIX3: no sudo on student; /opt/trading is student-owned in this setup
if [ $NO_STUDENT_COPY -eq 0 ]; then
  STUDENT_DIR="/opt/trading/_student_archive/journals/steps"
  ssh student "mkdir -p '$STUDENT_DIR'"
  scp "$ENTRY" "student:$STUDENT_DIR/"
  echo "OK: copied journal entry to student:$STUDENT_DIR/"
else
  echo "SKIP: student copy disabled"
fi

if [ $NO_DEEPSEEK -eq 0 ]; then
  ssh student "nohup cmd-deepseek_response roadmap_module '$MODEL' '$MODULE' '$N' > /tmp/rr_${MODULE}.log 2>&1 &" || true
  ssh student "nohup cmd-deepseek_thinking  roadmap_module '$MODEL' '$MODULE' '$N' > /tmp/rt_${MODULE}.log 2>&1 &" || true
  echo "OK: triggered deepseek roadmap_module bg (model=$MODEL n=$N)"
else
  echo "SKIP: deepseek trigger disabled"
fi

echo "OK post_change v2 (fix3): module=$MODULE"
