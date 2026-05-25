#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

CMD="${1:-help}"

case "$CMD" in
  sanity) bash "$SCRIPT_DIR/sanity.sh" ;;
  test)   python3 -m unittest modules.datasheet_writer.tests.test_writer -v ;;
  write)  shift; python3 -m modules.datasheet_writer.app "$@" ;;
  status) python3 -c "import sys; sys.path.insert(0, '.'); from modules.datasheet_writer.app.writer import DatasheetWriter; print('DatasheetWriter: OK')" ;;
  help|*) echo "Usage: cmd.sh [sanity|test|write [options]|status|help]" ;;
esac
