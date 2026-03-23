#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case "${1:-help}" in
  status)
    echo "hf_free_platform status"
    echo "base_dir=$BASE_DIR"
    ;;
  tree)
    find "$BASE_DIR" -maxdepth 4 -type f | sort
    ;;
  help|*)
    echo "Usage: $0 {status|tree}"
    ;;
esac
