#!/usr/bin/env bash
set -Eeuo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$MODULE_DIR/../.." && pwd)"
BASE_DIR="/opt/trading"
if [[ ! -d "$BASE_DIR" ]]; then
  BASE_DIR="$ROOT"
fi
PERF_BASE="${PERF_BASE:-http://127.0.0.1:8010}"
PERF_LOG="$BASE_DIR/tmp/perf_dev.log"
APP="$BASE_DIR/modules/simex_bitget_bridge/app/simex_bitget_bridge.py"

python_bin() {
  if [[ -x "/opt/trading/venv/bin/python" ]]; then
    printf '%s\n' "/opt/trading/venv/bin/python"
  elif [[ -x "/opt/trading/.venv/bin/python" ]]; then
    printf '%s\n' "/opt/trading/.venv/bin/python"
  elif [[ -x "$ROOT/.venv/bin/python" ]]; then
    printf '%s\n' "$ROOT/.venv/bin/python"
  else
    printf '%s\n' "python3"
  fi
}

PYTHON_BIN="$(python_bin)"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    printf 'missing command: %s\n' "$1" >&2
    exit 1
  }
}

perf_ready() {
  curl -fsS "$PERF_BASE/perf/summary" >/dev/null 2>&1
}

listener_pid() {
  ss -ltnp '( sport = :8010 )' 2>/dev/null | sed -n 's/.*pid=\([0-9][0-9]*\).*/\1/p' | head -n 1
}

wait_perf_ready() {
  local i
  for i in {1..50}; do
    if perf_ready; then
      return 0
    fi
    sleep 0.2
  done
  printf 'perf not ready at %s\n' "$PERF_BASE" >&2
  exit 1
}

cmd_status() {
  local pid summary
  printf 'PERF_BASE=%s\n' "$PERF_BASE"
  printf 'listener_8010:\n'
  ss -ltnp '( sport = :8010 )' 2>/dev/null || true
  printf 'process_uvicorn_perf:\n'
  pgrep -af 'uvicorn perf\.perf_app:app|python -m uvicorn perf\.perf_app:app' || true
  printf 'summary_head240:\n'
  if summary="$(curl -fsS "$PERF_BASE/perf/summary" 2>/dev/null)"; then
    printf '%.240s\n' "$summary"
  else
    printf 'unavailable\n'
  fi
  pid="$(listener_pid || true)"
  [[ -n "$pid" ]] && printf 'listener_pid=%s\n' "$pid"
}

cmd_perf_start() {
  mkdir -p "$BASE_DIR/tmp"
  if perf_ready; then
    return 0
  fi
  nohup "$PYTHON_BIN" -m uvicorn perf.perf_app:app --host 127.0.0.1 --port 8010 >"$PERF_LOG" 2>&1 &
  wait_perf_ready
}

cmd_perf_stop() {
  local pid
  pid="$(listener_pid || true)"
  if [[ -n "$pid" ]]; then
    kill "$pid" 2>/dev/null || true
    sleep 0.5
    if kill -0 "$pid" 2>/dev/null; then
      kill -TERM "$pid" 2>/dev/null || true
    fi
  fi
}

cmd_perf_logs() {
  if [[ -f "$PERF_LOG" ]]; then
    tail -n "${2:-80}" "$PERF_LOG"
  else
    printf 'log file not found: %s\n' "$PERF_LOG" >&2
    exit 1
  fi
}

cmd_bitget_run() {
  cmd_perf_start
  exec "$PYTHON_BIN" "$APP"
}

cmd_smoke() {
  cmd_perf_start
  BASE="$PERF_BASE" "$BASE_DIR/scripts/smoke.sh"
}

cmd_sanity() {
  require_cmd ss
  require_cmd curl
  "$PYTHON_BIN" -c 'import requests' >/dev/null
  [[ -f "$APP" ]]
  cmd_perf_start
  ss -ltn '( sport = :8010 )' >/dev/null
  curl -fsS "$PERF_BASE/perf/summary" >/dev/null
  printf 'PASS\n'
}

case "${1:-}" in
  status)
    cmd_status
    ;;
  perf-start)
    cmd_perf_start
    ;;
  perf-stop)
    cmd_perf_stop
    ;;
  perf-logs)
    cmd_perf_logs "$@"
    ;;
  bitget-run)
    cmd_bitget_run
    ;;
  smoke)
    cmd_smoke
    ;;
  sanity)
    cmd_sanity
    ;;
  *)
    printf 'Usage: %s {status|perf-start|perf-stop|perf-logs|bitget-run|smoke|sanity}\n' "$0" >&2
    exit 1
    ;;
esac
