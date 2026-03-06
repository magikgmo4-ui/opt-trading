#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-help}"

usage() {
  echo "Usage: cmd-position <cmd> [args...]"
  echo
  echo "Commands:"
  echo "  sanity          Run sanity checks"
  echo "  test_lifecycle  Test open/close position"
  echo
}

case "$CMD" in
  sanity)
    python3 modules/position_engine/scripts/position_engine_sanity_check.sh
    ;;

  test_lifecycle)
    python3 modules/position_engine/position_manager.py test
    ;;

  help|--help|-h) usage ;;
  *) usage ;;
esac
