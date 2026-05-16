#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${LOCALCMS_PORT:-8700}"
APP="modules.localcms.app.main:app"

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh sanity         — run validation checks
  cmd.sh status         — show module status
  cmd.sh run            — start LocalCMS FastAPI (uvicorn)
  cmd.sh stop           — stop LocalCMS process
  cmd.sh health         — curl health endpoint
EOF
}

case "${1:-help}" in
  sanity)
    echo "=== LocalCMS Sanity ==="
    echo "Module: localcms"
    echo "App: $APP"
    echo "Port: $PORT"
    echo "Menu: $(python3 -c "import json; m=json.load(open('scripts/ai/menu/opt_trading_menu.json')); print(f'{len(m[\"menu\"])} domains')")"
    echo "Sessions: 9 (openclaw-core, screeners, strict-workers, trading-pipeline, market-data, apps-connectors, desk-pro, kg-repo, localcms-ui)"
    python3 -c "
import sys
sys.path.insert(0, '.')
from modules.localcms.app.main import app
print(f'FastAPI routes: {len(app.routes)}')
print('OK')
"
    ;;
  status)
    echo "Module: localcms"
    echo "Port: $PORT"
    echo "App: $APP"
    if curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
      echo "Status: RUNNING"
      curl -s "http://127.0.0.1:$PORT/health" | python3 -m json.tool
    else
      echo "Status: STOPPED"
    fi
    ;;
  run)
    echo "Starting LocalCMS on port $PORT..."
    cd "$BASE/../.."
    exec uvicorn "$APP" --host 127.0.0.1 --port "$PORT" --reload
    ;;
  stop)
    pkill -f "uvicorn $APP" 2>/dev/null && echo "LocalCMS stopped" || echo "LocalCMS not running"
    ;;
  health)
    curl -s "http://127.0.0.1:$PORT/health" | python3 -m json.tool
    ;;
  *)
    help_msg
    exit 1
    ;;
esac
