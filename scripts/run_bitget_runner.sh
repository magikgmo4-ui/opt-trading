#!/usr/bin/env bash
set -euo pipefail

cd /opt/trading

# charge l'environnement du projet (inclut TV_WEBHOOK_KEY, OPS_ADMIN_KEY, etc.)
set -a
source /opt/trading/.env
set +a

# defaults (override via env ou via systemd Environment=...)
export TV_WEBHOOK_URL="${TV_WEBHOOK_URL:-http://127.0.0.1:8000/tv}"
export TV_ENGINE="${TV_ENGINE:-COINM_SHORT}"
export SYMBOL="${SYMBOL:-BTCUSDT}"
export TF_SEC="${TF_SEC:-300}"
export POLL_S="${POLL_S:-5}"
export SL_PTS="${SL_PTS:-10}"
export DRY_RUN="${DRY_RUN:-0}"

# state/dedup (override possible)
export STATE_FILE="${STATE_FILE:-/opt/trading/state/bitget_tv_state.json}"
export DEDUP_FILE="${DEDUP_FILE:-/opt/trading/state/bitget_tv_dedup.json}"

# IMPORTANT: runner doit trouver bitget_feed.py (dans /opt/trading/tools)
# normalement le script runner a déjà sys.path.insert(...). sinon on force:
export PYTHONPATH="${PYTHONPATH:-}:/opt/trading/tools"

exec /opt/trading/venv/bin/python -u /opt/trading/tools/bitget_to_tv_runner.py
