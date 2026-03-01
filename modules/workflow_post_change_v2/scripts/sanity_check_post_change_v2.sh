#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading"
test -d "$BASE" || { echo "FAIL: /opt/trading missing"; exit 1; }
command -v ssh >/dev/null || { echo "FAIL: ssh missing"; exit 1; }
command -v scp >/dev/null || { echo "FAIL: scp missing"; exit 1; }
if [ -x "$BASE/scripts/log_event_to_student.sh" ]; then :; else echo "WARN: log_event_to_student.sh missing"; fi
echo "PASS"
