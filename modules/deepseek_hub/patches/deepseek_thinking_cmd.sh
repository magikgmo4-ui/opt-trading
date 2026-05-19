#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-help}"
MODEL="${2:-deepseek-r1:1.5b}"
PROMPT="${3:-Explique ton raisonnement en détail sur: état du projet + prochaines étapes.}"
OUTDIR="/opt/trading/_student_archive/thinking"

usage() {
  echo "Usage:"
  echo "  cmd-deepseek_thinking run [model] <sujet>"
  echo "  cmd-deepseek_thinking tail _ [N(default 10)]"
  echo "  cmd-deepseek_thinking roadmap_module [model] <module> [N(default 40)]"
}

case "$CMD" in
  run)
    mkdir -p "$OUTDIR"
    ts="$(TZ=America/Montreal date +%Y%m%d_%H%M%S)"
    tmp="/tmp/ollama_thinking_${RANDOM}.json"
    out="$OUTDIR/thinking_${ts}.md"

    payload="$(jq -n \
      --arg m "$MODEL" \
      --arg s "$PROMPT" \
      '{
        model:$m,
        messages:[{role:"user", content:("RÉPONDS EN FRANÇAIS. THINKING UNIQUEMENT.\nSUJET: " + $s)}],
        think:true,
        stream:false
      }'
    )"

    if ! timeout 600s curl -sS http://127.0.0.1:11434/api/chat -d "$payload" > "$tmp"; then
      echo "TIMEOUT_OR_CURL_ERROR"
      rm -f "$tmp"
      exit 0
    fi

    jq -r '(.message.thinking // "")' "$tmp" > "$out"
    if [ ! -s "$out" ]; then
      {
        echo "NO_THINKING_FIELD_RETURNED"
        echo
        jq -r '(.message.content // "")' "$tmp"
      } > "$out"
    fi

    echo "$out"
    rm -f "$tmp"
    ;;

  tail)
    N="${3:-10}"
    mkdir -p "$OUTDIR"
    files="$(ls -t "$OUTDIR"/thinking_*.md 2>/dev/null | head -n "$N" || true)"
    if [ -z "${files:-}" ]; then
      echo "NO_FILES"
      exit 0
    fi
    echo "$files"
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

  help|--help|-h) usage ;;
  *) usage ;;
esac
