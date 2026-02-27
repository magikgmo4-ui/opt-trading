#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-help}"
shift || true

ROOT="${VISION_ROOT:-/opt/trading/data/desk_pro/vision}"
PY="${PYTHON:-python3}"

case "$CMD" in
  run)
    $PY -m desk_pro_vision.vision.vision_generate --root "$ROOT" --mode placeholder "$@"
    ;;
  latest)
    echo "Latest:"
    ls -lah "$ROOT/latest" || true
    ;;
  summary)
    cat "$ROOT/latest/summary.json"
    ;;
  log)
    tail -n "${1:-50}" "$ROOT/latest/vision.log.jsonl"
    ;;
  help|*)
    cat <<EOF
Usage: $(basename "$0") <command>

Commands:
  run                Generate a new placeholder run
  latest             Show latest symlink target
  summary            Print latest summary.json
  log [N]            Tail last N lines of vision.log.jsonl (default 50)

Env:
  VISION_ROOT=/opt/trading/data/desk_pro/vision
  PYTHON=python3
EOF
    ;;
esac
