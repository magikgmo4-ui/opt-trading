#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"

require_archived_runtime_opt_in() {
  cat >&2 <<'EOF'
MIMO Open Observer is archived residual runtime.
Active commands are disabled by default.

To run a residual command explicitly, use:
  MIMO_OPEN_OBSERVER_ALLOW_ARCHIVED_RUNTIME=1 bash modules/mimo_open_observer/cmd.sh <command> ...

See:
  modules/mimo_open_observer/LEGACY.md
EOF
  exit 2
}

cd "$ROOT_DIR" || exit 1

cmd="${1:-help}"
shift 2>/dev/null || true

case "$cmd" in
  help|docs-index|sanity) ;;
  detect_once|detect_range|replay|gate_replay|check_window|sample_pending|build_stats|show_stats)
    [[ "${MIMO_OPEN_OBSERVER_ALLOW_ARCHIVED_RUNTIME:-0}" == "1" ]] || require_archived_runtime_opt_in
    ;;
esac

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
  gate_replay       Replay only when the market window is open
  check_window      Check current market window status + next window
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
  gate_replay)
    csv_file=""
    at_ts=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --csv) csv_file="$2"; shift 2 ;;
        --at) at_ts="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    if [[ -z "$csv_file" ]]; then
      echo "Usage: $0 gate_replay --csv <file> [--at <iso_ts>]" >&2
      exit 1
    fi
    if [[ -n "$at_ts" ]]; then
      python3 -m modules.mimo_open_observer.app.runner_detect gate_replay --csv "$csv_file" --at "$at_ts"
    else
      python3 -m modules.mimo_open_observer.app.runner_detect gate_replay --csv "$csv_file"
    fi
    ;;
  check_window)
    python3 -m modules.mimo_open_observer.app.runner_detect check_window
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
