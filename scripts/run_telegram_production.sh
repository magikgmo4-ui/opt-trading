#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR" && pwd)
LOG_DIR="$REPO_ROOT/data/logs/telegram"
TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")

mkdir -p "$LOG_DIR"

exec 1>>"$LOG_DIR/production_${TIMESTAMP}.log"
exec 2>&1

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Telegram production capture start"

if ! command -v sg &>/dev/null; then
    echo "ERROR: sg command not available (required for opt-trading-secrets group)"
    exit 1
fi

sg opt-trading-secrets -c '
set -a
. /etc/opt-trading/env.d/roles/telegram_collector.env
set +a
echo "--- coinglass_alerts limit=20 ---"
bash scripts/run_telegram_collector.sh --channel coinglass_alerts --limit 20 run 2>&1
echo ""
echo "--- whale_alert_io limit=20 ---"
bash scripts/run_telegram_collector.sh --channel whale_alert_io --limit 20 run 2>&1
echo ""
echo "--- cryptoquant_official limit=20 ---"
bash scripts/run_telegram_collector.sh --channel cryptoquant_official --limit 20 run 2>&1
'

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Telegram production capture end"
