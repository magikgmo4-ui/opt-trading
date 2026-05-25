#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

CMD="${1:-help}"
case "$CMD" in
  sanity) bash "$SCRIPT_DIR/sanity.sh" ;;
  test)   python3 -m unittest modules.learning_feeder.tests.test_feeder -v ;;
  feed)   shift; python3 -m modules.learning_feeder.app "$@" ;;
  status) python3 -c "import sys; sys.path.insert(0, '.'); from modules.learning_feeder.app.feeder import LearningFeeder; print('LearningFeeder: OK')" ;;
  help|*) echo "Usage: cmd.sh [sanity|test|feed [options]|status|help]" ;;
esac
