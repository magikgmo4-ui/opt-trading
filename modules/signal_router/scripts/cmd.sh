#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${SIGNAL_ROUTER_PORT:-18900}"
HOST="${SIGNAL_ROUTER_HOST:-127.0.0.1}"
PID_FILE="/tmp/signal_router.pid"

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh sanity
  cmd.sh health
  cmd.sh test
  cmd.sh start
  cmd.sh stop
  cmd.sh status
  cmd.sh smoke        — POST test signal to running server
EOF
}

case "${1:-help}" in
  sanity)
    bash "$BASE/scripts/sanity.sh"
    ;;

  health)
    echo "MODULE=signal_router"
    curl -sf --max-time 5 "http://$HOST:$PORT/health" 2>/dev/null \
      && echo "" || echo "STATUS=not_running (start with cmd.sh start)"
    ;;

  test)
    cd "$BASE"
    python3 -m unittest tests.test_router -v
    ;;

  start)
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
      echo "signal_router already running (pid=$(cat "$PID_FILE"))"
      exit 0
    fi
    cd "$BASE"
    python3 -m app &
    echo $! > "$PID_FILE"
    sleep 1
    curl -sf --max-time 3 "http://$HOST:$PORT/health" || { echo "FAIL: server did not start"; exit 1; }
    echo "signal_router started (pid=$(cat "$PID_FILE")) on $HOST:$PORT"
    ;;

  stop)
    if [ -f "$PID_FILE" ]; then
      kill "$(cat "$PID_FILE")" 2>/dev/null && echo "signal_router stopped" || echo "process not running"
      rm -f "$PID_FILE"
    else
      echo "no pid file found"
    fi
    ;;

  status)
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
      echo "STATUS=running pid=$(cat "$PID_FILE")"
      curl -sf --max-time 3 "http://$HOST:$PORT/health" || true
    else
      echo "STATUS=stopped"
    fi
    ;;

  smoke)
    echo "POST /webhook test signal..."
    curl -sf --max-time 10 \
      -X POST "http://$HOST:$PORT/webhook" \
      -H "Content-Type: application/json" \
      -d '{"engine":"smoke_v1","signal":"BUY","symbol":"BTCUSDT","tf":"1h","price":65000,"strategy_id":"smoke_test"}' \
      | python3 -m json.tool
    ;;

  help|--help|-h)
    help_msg
    ;;

  *)
    echo "unknown: ${1:-}" >&2; help_msg >&2; exit 1
    ;;
esac
