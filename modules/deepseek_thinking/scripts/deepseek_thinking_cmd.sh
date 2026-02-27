#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-help}"
MODEL="${2:-deepseek-r1:1.5b}"
PROMPT="${3:-Explique ton raisonnement en détail sur: état du projet + prochaines étapes.}"
OUTDIR="/opt/trading/_student_archive/thinking"

case "$CMD" in
  run)
    mkdir -p "$OUTDIR"
    ts="$(TZ=America/Montreal date +%Y%m%d_%H%M%S)"
    tmp="/tmp/ollama_thinking_${RANDOM}.json"
    out="$OUTDIR/thinking_${ts}.md"

    payload=$(python3 - <<PY
import json
print(json.dumps({
  "model":"$MODEL",
  "prompt":"RÉPONDS EN FRANÇAIS. THINKING UNIQUEMENT.\nSUJET: $PROMPT",
  "stream":False,
  "options":{"num_predict":900}
}))
PY
)
    if ! timeout 600s curl -sS http://127.0.0.1:11434/api/generate -d "$payload" > "$tmp"; then
      echo "TIMEOUT_OR_CURL_ERROR"
      rm -f "$tmp"
      exit 0
    fi

    python3 - "$tmp" "$out" <<'PY'
import sys, json
tmp_path=sys.argv[1]; out_path=sys.argv[2]
d=json.load(open(tmp_path,"r",encoding="utf-8"))
thinking=(d.get("thinking") or "").strip()
open(out_path,"w",encoding="utf-8").write(thinking + "\n")
print(out_path)
PY
    rm -f "$tmp"
    ;;
  roadmap_module)
    MOD="${3:-desk_pro}"
    N="${4:-40}"
    export DEEPSEEK_MODEL="$MODEL"
    export MOD="$MOD"
    export EVENT_N="$N"
    . /opt/trading/.venv/bin/activate
    python /opt/trading/modules/deepseek_thinking/scripts/roadmap_thinking_by_module.py
    ;;
  *)
    echo "Usage:"
    echo "  cmd-deepseek_thinking run [model] "<sujet>""
    echo "  cmd-deepseek_thinking roadmap_module [model] <module> [N(default 40)]"
    ;;
esac
