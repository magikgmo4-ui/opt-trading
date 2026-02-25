#!/usr/bin/env bash
set -euo pipefail
REPO="${REPO:-/opt/trading}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8010}"

case "${1:-}" in
  restart)
    echo "=== Restart uvicorn on 8010 (perf.perf_app:app) ==="
    sudo pkill -f "uvicorn perf\.perf_app:app" || true
    sudo pkill -f "python -m uvicorn perf\.perf_app:app" || true
    sleep 1
    cd "$REPO"
    nohup "$REPO/venv/bin/python" -m uvicorn perf.perf_app:app --host 0.0.0.0 --port 8010 > "$REPO/tmp/uvicorn_8010.log" 2>&1 &
    sleep 1
    sudo ss -ltnp | grep ':8010' || true
    echo "Log: $REPO/tmp/uvicorn_8010.log"
    ;;
  test)
    echo "=== Test /desk/ui contains toolbox ==="
    curl -sS "$BASE_URL/desk/ui" | grep -n "/desk/toolbox" || echo "ABSENT"
    ;;
  *)
    echo "Usage: desk_pro_ui_toolbox_fix_cmd.sh {restart|test}"
    exit 2
    ;;
esac
