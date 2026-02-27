#!/usr/bin/env bash
set -euo pipefail
CMD="${1:-help}"
MODEL="${2:-deepseek-r1:1.5b}"

case "$CMD" in
  sanity) sanity-deepseek_student ;;
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
    . /opt/trading/.venv/bin/activate
    python /opt/trading/modules/deepseek_student/scripts/roadmap_from_events.py
    ;;
  *) echo "Usage: cmd-deepseek_student {sanity|pull|test|roadmap} [model] [N]" ;;
esac
