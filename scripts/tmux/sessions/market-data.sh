#!/usr/bin/env bash
# market-data session — collectors + analyzers + scanner + hub
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

SESSION="market-data"
TMUX="${TMUX_CMD:-tmux}"

$TMUX new-session -d -s "$SESSION" -n mdata:binance 2>/dev/null || true
$TMUX send-keys -t "$SESSION:mdata:binance" "cd $PROJECT_ROOT && echo 'collector_binance_spot — daemon'" Enter

$TMUX new-window -t "$SESSION" -n mdata:coingecko
$TMUX send-keys -t "$SESSION:mdata:coingecko" "cd $PROJECT_ROOT && echo 'collector_coingecko — daemon'" Enter

$TMUX new-window -t "$SESSION" -n mdata:derivatives
$TMUX send-keys -t "$SESSION:mdata:derivatives" "cd $PROJECT_ROOT && echo 'derivatives_collector — daemon'" Enter

$TMUX new-window -t "$SESSION" -n mdata:analyzers
$TMUX send-keys -t "$SESSION:mdata:analyzers" "cd $PROJECT_ROOT && echo 'derivatives_analyzer + liquidation_analyzer'" Enter

$TMUX new-window -t "$SESSION" -n mdata:scanner
$TMUX send-keys -t "$SESSION:mdata:scanner" "cd $PROJECT_ROOT && echo 'market_scanner — orchestrateur collectors'" Enter

$TMUX new-window -t "$SESSION" -n mdata:hub
$TMUX send-keys -t "$SESSION:mdata:hub" "cd $PROJECT_ROOT && echo 'marketdata — hub données central'" Enter
