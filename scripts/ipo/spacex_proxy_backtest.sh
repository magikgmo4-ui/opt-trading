#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[spacex_proxy_backtest] failed at line ${LINENO}" >&2' ERR
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "=== SPCX V2 — Proxy IPO Backtest ==="

cmd="python3 -m modules.spcx_v2.proxy_backtest"

if [ "${1:-}" = "--all" ]; then
    python3 -c "
from modules.spcx_v2.proxy_backtest import run_all_proxy, write_proxy_report
results = run_all_proxy()
report = write_proxy_report(results)
print(f'Report: {report}')
"
elif [ "${1:-}" = "--symbol" ] && [ -n "${2:-}" ]; then
    SYMBOL="$2"
    CSV="${3:-data/ipo/proxy/${SYMBOL}_ipo.csv}"
    python3 -c "
from modules.spcx_v2.proxy_backtest import run_proxy_backtest, write_proxy_report
result = run_proxy_backtest('$SYMBOL', '$CSV')
report = write_proxy_report({'$SYMBOL': result})
print(f'Symbol: $SYMBOL | Setups: {result[\"candles_replayed\"]}')
print(f'Report: {report}')
"
else
    echo "Usage: spacex_proxy_backtest.sh --all | --symbol SYMBOL [CSV_PATH]"
    exit 1
fi

echo "=== proxy backtest complete ==="
