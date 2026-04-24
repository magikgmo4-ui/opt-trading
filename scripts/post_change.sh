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

JOURNAL_BLOCK=""
if [ ! -t 0 ]; then JOURNAL_BLOCK="$(cat || true)"; fi
if [ -n "${JOURNAL_BLOCK// /}" ]; then
  echo "INFO: inline notes received, but local journal capture is retired."
fi

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

if [ $NO_STUDENT_COPY -eq 0 ]; then
  echo "SKIP: student copy retired with local journal removal"
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

echo "OK post_change v2: module=$MODULE"
