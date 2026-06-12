#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
cd "$ROOT_DIR" || exit 1

cmd="${1:-help}"
case "$cmd" in
  once|watch|summary)
    python3 -m modules.spcx_v2.runner "--$cmd"
    ;;
  replay)
    python3 -m modules.spcx_v2.runner --replay "${2:-}"
    ;;
  menu)
    exec bash "$MODULE_DIR/scripts/menu.sh"
    ;;
  sanity)
    exec bash "$MODULE_DIR/scripts/sanity_check.sh"
    ;;
  install)
    exec bash "$MODULE_DIR/scripts/install_shortcuts.sh"
    ;;
  *)
    echo "Usage: cmd.sh once|watch|replay FILE|summary|menu|sanity|install"
    exit 1
    ;;
esac
