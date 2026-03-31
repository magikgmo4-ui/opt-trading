#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"

cd "$ROOT_DIR" || exit 1

cmd="${1:-help}"
shift 2>/dev/null || true

case "$cmd" in
  help)
    cat <<'EOF'
mimo_open_observer v0

Commands:
  help              Show this help
  docs-index        Show docs index path
  sanity            Run sanity check
  detect_once       Detect FVG on one fixture (--fixture NAME)
  detect_range      Detect FVG on all fixtures
  replay --csv FILE Replay full pipeline from CSV (detect + sample + stats)
  sample_pending    Enrich pending raw events with outcomes
  build_stats       Build stats from enriched events
  show_stats        Display stats summary
EOF
    ;;
  docs-index)
    echo "$MODULE_DIR/docs/00_SESSION_INDEX_MIMO_OPEN_OBSERVER_V0.txt"
    ;;
  sanity)
    exec bash "$MODULE_DIR/sanity.sh"
    ;;
  detect_once)
    fixture=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --fixture) fixture="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    if [[ -n "$fixture" ]]; then
      python3 -m modules.mimo_open_observer.app.runner_detect detect_once --fixture "$fixture"
    else
      python3 -m modules.mimo_open_observer.app.runner_detect detect_once
    fi
    ;;
  detect_range)
    python3 -m modules.mimo_open_observer.app.runner_detect detect_range
    ;;
  replay)
    csv_file=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --csv) csv_file="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    if [[ -z "$csv_file" ]]; then
      echo "Usage: $0 replay --csv <file>" >&2
      exit 1
    fi
    python3 -m modules.mimo_open_observer.app.runner_detect replay --csv "$csv_file"
    ;;
  sample_pending)
    python3 -m modules.mimo_open_observer.app.runner_sample sample_pending
    ;;
  build_stats)
    python3 -m modules.mimo_open_observer.app.runner_stats build_stats
    ;;
  show_stats)
    python3 -m modules.mimo_open_observer.app.runner_stats show_stats
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    echo "Run '$0 help' for available commands." >&2
    exit 1
    ;;
esac
