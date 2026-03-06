#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-help}"

usage() {
  echo "Usage: cmd-execution <cmd> [args...]"
  echo
  echo "Commands:"
  echo "  sanity          Run sanity checks"
  echo "  test_paper      Run a paper trade test"
  echo
}

case "$CMD" in
  sanity)
    python3 modules/execution_engine/scripts/execution_engine_sanity_check.sh
    ;;

  test_paper)
    python3 modules/execution_engine/executor.py test
    ;;

  help|--help|-h) usage ;;
  *) usage ;;
esac
