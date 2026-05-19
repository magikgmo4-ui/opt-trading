#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")/.." && pwd)"

while true; do
    echo ""
    echo "=== Airtable Bridge Menu ==="
    echo "1) Sanity check"
    echo "2) Send trade"
    echo "3) Send signal"
    echo "4) Send backtest"
    echo "5) Send GO status"
    echo "q) Quit"
    echo -n "Choice: "
    read -r choice

    case "$choice" in
        1)
            "$DIR/scripts/sanity_check.sh"
            ;;
        2)
            echo -n "Symbol: "; read -r symbol
            echo -n "Direction (buy/sell): "; read -r direction
            echo -n "Entry price: "; read -r entry
            python3 -c "
import json, sys
sys.path.insert(0, '$DIR/app')
from payloads import TradePayload
from client import send_trade
p = TradePayload(symbol='$symbol', direction='$direction', entry_price=float('$entry'))
result = send_trade(p.to_fields())
print(json.dumps(result, indent=2))
"
            ;;
        3)
            echo -n "Source: "; read -r source
            echo -n "Symbol: "; read -r symbol
            echo -n "Signal: "; read -r signal
            TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
            python3 -c "
import json, sys
sys.path.insert(0, '$DIR/app')
from payloads import SignalPayload
from client import send_signal
p = SignalPayload(source='$source', timestamp='$TS', symbol='$symbol', signal='$signal')
result = send_signal(p.to_fields())
print(json.dumps(result, indent=2))
"
            ;;
        4)
            echo -n "Strategy: "; read -r strategy
            echo -n "Period: "; read -r period
            python3 -c "
import json, sys
sys.path.insert(0, '$DIR/app')
from payloads import BacktestPayload
from client import send_backtest
p = BacktestPayload(strategy='$strategy', period='$period')
result = send_backtest(p.to_fields())
print(json.dumps(result, indent=2))
"
            ;;
        5)
            echo -n "GO ID: "; read -r go_id
            echo -n "Status: "; read -r status
            TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
            python3 -c "
import json, sys
sys.path.insert(0, '$DIR/app')
from payloads import GOStatusPayload
from client import send_go_status
p = GOStatusPayload(go_id='$go_id', status='$status', machine='fantome', updated_at='$TS')
result = send_go_status(p.to_fields())
print(json.dumps(result, indent=2))
"
            ;;
        q|Q)
            echo "Exit."
            break
            ;;
        *)
            echo "Invalid choice"
            ;;
    esac
done
