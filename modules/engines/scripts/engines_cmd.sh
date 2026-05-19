#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-help}"

usage() {
  echo "Usage: cmd-engines <cmd> [args...]"
  echo
  echo "Commands:"
  echo "  sanity          Run sanity checks"
  echo "  list            List all registered engines"
  echo "  test <engine>   Test run a specific engine (with dummy payload)"
  echo
}

case "$CMD" in
  sanity)
    python3 modules/engines/scripts/engines_sanity_check.sh
    ;;

  list)
    # Simple one-liner to print keys from registry
    python3 -c "from modules.engines.registry import list_engines; print('\n'.join(list_engines()))"
    ;;

  test)
    ENGINE="${2:-ECHO_TEST}"
    python3 -c "from modules.engines.router import route_event; print(route_event('$ENGINE', {'test': 'true'}))"
    ;;

  help|--help|-h) usage ;;
  *) usage ;;
esac
