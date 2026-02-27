#!/usr/bin/env bash
set -euo pipefail

MODULE="${1:-general}"
TITLE="${2:-Change}"
MESSAGE="${3:-Updated something}"
N="${4:-20}"
MODEL="${5:-deepseek-r1:1.5b}"

# 1) snapshot git + event
if command -v cmd-report_after_change >/dev/null 2>&1; then
  cmd-report_after_change "$MODULE" "$TITLE" "$MESSAGE"
elif [[ -x /opt/trading/scripts/log_event_to_student.sh ]]; then
  /opt/trading/scripts/log_event_to_student.sh "$MODULE" "$TITLE" "$MESSAGE"
fi

# 2) DeepSeek roadmap (student) in background (non-blocking)
ssh student "nohup cmd-deepseek_response roadmap_module '$MODEL' '$MODULE' '$N' > /tmp/rr_${MODULE}.log 2>&1 </dev/null &" || true
ssh student "nohup cmd-deepseek_thinking  roadmap_module '$MODEL' '$MODULE' '$N' > /tmp/rt_${MODULE}.log 2>&1 </dev/null &" || true

echo "OK post_change: module=$MODULE"
