#!/usr/bin/env bash
set -euo pipefail

REPO=${REPO:-/opt/trading}
BASE_URL=${BASE_URL:-http://127.0.0.1:8010}
LOG=${LOG:-/opt/trading/tmp/uvicorn_8010.log}

usage(){
  echo "Usage: $0 {restart|test|logs}" >&2
}

restart(){
  echo "=== Restart uvicorn on 8010 (perf.perf_app:app) ==="
  sudo pkill -f 'uvicorn perf\.perf_app:app' || true
  sudo pkill -f 'python -m uvicorn perf\.perf_app:app' || true
  sleep 1
  mkdir -p /opt/trading/tmp
  nohup /opt/trading/venv/bin/python -m uvicorn perf.perf_app:app --host 0.0.0.0 --port 8010 > "$LOG" 2>&1 &
  sleep 1
  sudo ss -ltnp | grep ':8010' || { echo "8010 DOWN"; echo "Log: $LOG"; tail -n 80 "$LOG" || true; exit 1; }
  echo "UP. Log: $LOG"
}

test(){
  echo "=== Test /desk/ui contains toolbox ==="
  curl -sS "$BASE_URL/desk/ui" | grep -n "/desk/toolbox" || { echo "ABSENT"; exit 1; }
  echo "OK"
}

logs(){
  tail -n 120 "$LOG" || true
}

cmd=${1:-}
case "$cmd" in
  restart) restart;;
  test) test;;
  logs) logs;;
  *) usage; exit 2;;
esac
