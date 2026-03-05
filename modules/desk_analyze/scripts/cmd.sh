#!/usr/bin/env bash
set -euo pipefail

SCRIPT="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT="$(readlink -f "$SCRIPT" 2>/dev/null || echo "$SCRIPT")"
fi
BASE="$(cd "$(dirname "$SCRIPT")/.." && pwd)"
PY="$BASE/analyze_latest.py"

: "${INDEX_FILE:=/opt/trading/desk/snapshots/latest.json}"
: "${DESK_SYMBOLS:=BTCUSDT.P,XAUUSD,SOLUSDT.P,ETHUSDT.P}"
: "${STALE_MINUTES:=15}"
: "${TIMEZONE:=America/Montreal}"

: "${TELEGRAM_API_BASE:=https://api.telegram.org}"
: "${TELEGRAM_BOT_TOKEN:=}"
: "${TELEGRAM_CHAT_ID:=}"

usage(){
  cat <<EOF
desk_analyze cmd

Usage:
  $0 preview                # status + (optionally) vision if enabled
  $0 preview_no_openai      # status only
  $0 preview_json           # debug json
  $0 send                   # send to TELEGRAM_CHAT_ID (single message)
  $0 print_config
  $0 install_shortcuts (sudo)

OpenAI Vision (optional):
  set DESK_ANALYZE_OPENAI=1 and OPENAI_API_KEY in env (often provided by bot_vision_step2 service)

Env:
  INDEX_FILE, DESK_SYMBOLS, STALE_MINUTES, TIMEZONE
  DESK_ANALYZE_OPENAI, DESK_ANALYZE_MAX_CHARS, OPENAI_API_KEY, OPENAI_MODEL
  TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_API_BASE
EOF
}

preview(){
  TIMEZONE="$TIMEZONE" "$PY" --index "$INDEX_FILE" --symbols "$DESK_SYMBOLS" --stale-minutes "$STALE_MINUTES"
}

preview_no_openai(){
  TIMEZONE="$TIMEZONE" "$PY" --no-openai --index "$INDEX_FILE" --symbols "$DESK_SYMBOLS" --stale-minutes "$STALE_MINUTES"
}

preview_json(){
  TIMEZONE="$TIMEZONE" "$PY" --json --index "$INDEX_FILE" --symbols "$DESK_SYMBOLS" --stale-minutes "$STALE_MINUTES"
}

send(){
  if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]]; then
    echo "ERROR: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set" >&2
    return 2
  fi
  TEXT="$(preview)"
  curl -sS -X POST \
    "${TELEGRAM_API_BASE}/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
    --data-urlencode "text=${TEXT}" \
    --data-urlencode "disable_web_page_preview=true" \
    >/dev/null
  echo "OK: sent /analyze to chat_id=$TELEGRAM_CHAT_ID"
}

print_config(){
  cat <<EOF
BASE=$BASE
PY=$PY
INDEX_FILE=$INDEX_FILE
DESK_SYMBOLS=$DESK_SYMBOLS
STALE_MINUTES=$STALE_MINUTES
TIMEZONE=$TIMEZONE
DESK_ANALYZE_OPENAI=${DESK_ANALYZE_OPENAI:-}
DESK_ANALYZE_MAX_CHARS=${DESK_ANALYZE_MAX_CHARS:-}
OPENAI_MODEL=${OPENAI_MODEL:-}
TELEGRAM_API_BASE=$TELEGRAM_API_BASE
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID:-}
EOF
}

install_shortcuts(){
  sudo "$BASE/scripts/install_shortcuts.sh"
}

cmd="${1:-}"; shift || true
case "$cmd" in
  preview) preview ;;
  preview_no_openai) preview_no_openai ;;
  preview_json) preview_json ;;
  send) send ;;
  print_config) print_config ;;
  install_shortcuts) install_shortcuts ;;
  ""|-h|--help|help) usage ;;
  *) echo "Unknown cmd: $cmd"; usage; exit 2 ;;
esac
