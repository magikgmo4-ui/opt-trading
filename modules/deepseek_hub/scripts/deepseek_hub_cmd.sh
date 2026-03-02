#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-help}"
MODEL="${2:-deepseek-r1:1.5b}"

usage() {
  echo "Usage: cmd-deepseek_hub <cmd> [model] [args...]"
  echo
  echo "Core:"
  echo "  sanity [model]"
  echo "  status"
  echo "  logs [N(default 120)]"
  echo "  models"
  echo "  pull [model]"
  echo
  echo "Runs (archive to _student_archive):"
  echo "  think [model] <sujet>"
  echo "  response [model] <sujet>"
  echo "  tail_think _ [N(default 10)]"
  echo "  tail_response _ [N(default 10)]"
  echo
  echo "Roadmaps:"
  echo "  roadmap_events [model] [N(default 200)]"
  echo "  roadmap_think_module [model] <module> [N(default 40)]"
  echo "  roadmap_response_module [model] <module> [N(default 40)]"
}

case "$CMD" in
  sanity) sanity-deepseek_hub ;;

  status)
    echo "=== Ollama ==="
    ollama --version || true
    curl -s http://127.0.0.1:11434/api/version || true
    echo
    systemctl --no-pager status ollama || true
    ;;

  logs)
    N="${2:-120}"
    sudo journalctl -u ollama -n "$N" --no-pager || true
    ;;

  models)
    ollama list || true
    ;;

  pull)
    ollama pull "$MODEL"
    ;;

  think)
    SUBJECT="${3:-État du projet + prochaines étapes.}"
    cmd-deepseek_thinking run "$MODEL" "$SUBJECT"
    ;;

  response)
    SUBJECT="${3:-État du projet + prochaines étapes.}"
    cmd-deepseek_response run "$MODEL" "$SUBJECT"
    ;;

  tail_think)
    N="${3:-10}"
    cmd-deepseek_thinking tail _ "$N"
    ;;

  tail_response)
    N="${3:-10}"
    cmd-deepseek_response tail _ "$N"
    ;;

  roadmap_events)
    N="${3:-200}"
    cmd-deepseek_student roadmap "$MODEL" "$N"
    ;;

  roadmap_think_module)
    MOD="${3:-desk_pro}"
    N="${4:-40}"
    cmd-deepseek_thinking roadmap_module "$MODEL" "$MOD" "$N"
    ;;

  roadmap_response_module)
    MOD="${3:-desk_pro}"
    N="${4:-40}"
    cmd-deepseek_response roadmap_module "$MODEL" "$MOD" "$N"
    ;;

  help|--help|-h) usage ;;
  *) usage ;;
esac
