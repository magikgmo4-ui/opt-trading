#!/usr/bin/env bash
# trade_executor CLI helper
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

CMD="${1:-help}"

case "$CMD" in
  sanity)
    bash "$SCRIPT_DIR/sanity.sh"
    ;;
  test)
    python3 -m unittest modules.trade_executor.tests.test_executor -v
    ;;
  execute)
    shift
    python3 -m modules.trade_executor.app "$@"
    ;;
  status)
    python3 -c "
import sys; sys.path.insert(0, '.')
from modules.trade_executor.app.executor import TradeExecutor
print('TradeExecutor: OK')
"
    ;;
  help|*)
    echo "Usage: cmd.sh [sanity|test|execute [options]|status|help]"
    ;;
esac
