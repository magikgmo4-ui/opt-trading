#!/usr/bin/env bash
set -euo pipefail

BASE="/opt/trading/modules/desk_capture_inputs"
VENV="/opt/trading/.venvs/desk_capture_inputs"
PY="$VENV/bin/python"

if [[ -f "$BASE/config/desk_capture_inputs.env" ]]; then
  # shellcheck disable=SC1091
  source "$BASE/config/desk_capture_inputs.env"
fi

usage() {
  cat <<'EOF'
Usage:
  cmd.sh extract_once
  cmd.sh print_latest
  cmd.sh print_config
EOF
}

cmd="${1:-}"
case "$cmd" in
  extract_once)
    exec "$PY" -m modules.desk_capture_inputs.extract_tv_inputs
    ;;
  print_latest)
    sed -n '1,240p' /opt/trading/desk/inputs/tv_inputs_latest.json || true
    ;;
  print_config)
    echo "OPENAI_MODEL=${OPENAI_MODEL:-}"
    echo "OPENAI_API_BASE=${OPENAI_API_BASE:-}"
    echo "MERGE_BACK_TO_SNAPSHOTS=${MERGE_BACK_TO_SNAPSHOTS:-}"
    echo "TF_DEFAULT=${TF_DEFAULT:-}"
    echo "MAX_LEVELS=${MAX_LEVELS:-}"
    ;;
  *)
    usage
    exit 2
    ;;
esac
