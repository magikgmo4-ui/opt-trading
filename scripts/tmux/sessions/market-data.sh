#!/usr/bin/env bash
# SESSION 5 — market-data (admin-trading)
# Collectors + analyzers + market scanner + hub
set -e
SESSION="market-data"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already running"
    exit 0
fi

mkdir -p "$PROJECT_ROOT/logs"

tmux new-session -d -s "$SESSION" -n "binance"
tmux send-keys -t "$SESSION:binance" \
    "cd '$PROJECT_ROOT' && bash modules/collector_binance_spot/cmd.sh run 2>&1 | tee logs/collector_binance_spot.log" Enter

tmux new-window -t "$SESSION" -n "coingecko"
tmux send-keys -t "$SESSION:coingecko" \
    "cd '$PROJECT_ROOT' && bash modules/collector_coingecko/cmd.sh run 2>&1 | tee logs/collector_coingecko.log" Enter

tmux new-window -t "$SESSION" -n "derivatives"
tmux send-keys -t "$SESSION:derivatives" \
    "cd '$PROJECT_ROOT' && bash modules/derivatives_collector/cmd.sh run 2>&1 | tee logs/derivatives_collector.log" Enter

tmux new-window -t "$SESSION" -n "analyzers"
tmux send-keys -t "$SESSION:analyzers" \
    "cd '$PROJECT_ROOT' && bash modules/derivatives_analyzer/cmd.sh run 2>&1 | tee logs/derivatives_analyzer.log" Enter

tmux new-window -t "$SESSION" -n "scanner"
tmux send-keys -t "$SESSION:scanner" \
    "cd '$PROJECT_ROOT' && bash modules/market_scanner/cmd.sh run 2>&1 | tee logs/market_scanner.log" Enter

tmux new-window -t "$SESSION" -n "hub"
tmux send-keys -t "$SESSION:hub" \
    "cd '$PROJECT_ROOT' && bash modules/marketdata/cmd.sh run 2>&1 | tee logs/marketdata.log" Enter

tmux select-window -t "$SESSION:binance"
echo "$SESSION started (windows: binance coingecko derivatives analyzers scanner hub)"
