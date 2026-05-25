#!/usr/bin/env bash
# result_tracker CLI helper
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
    python3 -m unittest modules.result_tracker.tests.test_tracker -v
    ;;
  track)
    shift
    python3 -m modules.result_tracker.app "$@"
    ;;
  status)
    python3 -c "
import sys; sys.path.insert(0, '.')
from modules.result_tracker.app.tracker import ResultTracker
print('ResultTracker: OK')
"
    ;;
  help|*)
    echo "Usage: cmd.sh [sanity|test|track [options]|status|help]"
    ;;
esac
