#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_USER="${OPENCLAW_GATEWAY_USER:-openclaw}"
TARGET_HOME_DEFAULT="$(getent passwd "$TARGET_USER" 2>/dev/null | cut -d: -f6 || true)"
TARGET_HOME="${OPENCLAW_GATEWAY_HOME:-${TARGET_HOME_DEFAULT:-/home/$TARGET_USER}}"
SESSION="${OPENCLAW_GATEWAY_SESSION:-openclaw-gateway}"
LOG_DIR="${OPENCLAW_GATEWAY_LOG_DIR:-$TARGET_HOME/.openclaw/logs}"
LOG_FILE="${OPENCLAW_GATEWAY_LOG_FILE:-$LOG_DIR/gateway_foreground.log}"
TAIL_LINES="${OPENCLAW_GATEWAY_TAIL_LINES:-80}"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

require_target_user() {
  [ "$(id -un)" = "$TARGET_USER" ] || fail "exécuter ce module sous l'utilisateur $TARGET_USER"
}

has_session() {
  tmux has-session -t "$SESSION" >/dev/null 2>&1
}

print_common() {
  printf '%s\n' \
    "MODULE=gateway_openclaw" \
    "TARGET_USER=$TARGET_USER" \
    "TARGET_HOME=$TARGET_HOME" \
    "SESSION=$SESSION" \
    "LOG_DIR=$LOG_DIR" \
    "LOG_FILE=$LOG_FILE" \
    "TAIL_LINES=$TAIL_LINES"
}
