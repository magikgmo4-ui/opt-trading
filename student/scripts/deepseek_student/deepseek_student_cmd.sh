#!/usr/bin/env bash
set -euo pipefail

# Robustly determine script and repo root directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Assuming: modules/deepseek_student/scripts/deepseek_student_cmd.sh
# So ../../.. from SCRIPT_DIR should be repo root
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

CMD="${1:-help}"
MODEL="${2:-deepseek-r1:1.5b}"

case "$CMD" in
  sanity)
    if [ -x "$SCRIPT_DIR/sanity_check_deepseek_student.sh" ]; then
        bash "$SCRIPT_DIR/sanity_check_deepseek_student.sh"
    else
        echo "WARN: canonical deepseek student sanity script not found."
    fi
    ;;
  pull)   ollama pull "$MODEL" ;;
  test)
    tmp="/tmp/ollama_test_${RANDOM}.json"
    payload=$(python3 - <<PY
import json
print(json.dumps({
  "model":"$MODEL",
  "prompt":"Réponds en FRANÇAIS. Donne uniquement une ligne: OK\\nSORTIE FINALE:",
  "stream":False,
  "options":{"num_predict":64}
}))
PY
)
    if ! timeout 180s curl -sS http://127.0.0.1:11434/api/generate -d "$payload" > "$tmp"; then
      echo "TIMEOUT_OR_CURL_ERROR"; rm -f "$tmp"; exit 0
    fi
    if [ ! -s "$tmp" ]; then
      echo "EMPTY_RESPONSE"; rm -f "$tmp"; exit 0
    fi
    python3 - "$tmp" <<PY
import sys, json
d=json.load(open(sys.argv[1],"r",encoding="utf-8"))
resp=(d.get("response") or "").strip()
think=(d.get("thinking") or "").strip()
print(resp if resp else think if think else json.dumps(d, ensure_ascii=False))
PY
    rm -f "$tmp"
    ;;
  roadmap)
    N="${3:-200}"
    export DEEPSEEK_MODEL="$MODEL"
    export EVENT_N="$N"
    # Use robust path to venv activation
    if [ -f "$ROOT_DIR/.venv/bin/activate" ]; then
        . "$ROOT_DIR/.venv/bin/activate"
    elif [ -f "$ROOT_DIR/venv/bin/activate" ]; then
        . "$ROOT_DIR/venv/bin/activate"
    fi
    # Use robust path to python script
    python "$SCRIPT_DIR/roadmap_from_events.py"
    ;;
  *) echo "Usage: cmd-deepseek_student {sanity|pull|test|roadmap} [model] [N]" ;;
esac
