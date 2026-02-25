#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/opt/trading}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8010}"

usage() {
  cat <<'USAGE'
cmd-desk_pro — Desk Pro commands
Usage:
  cmd-desk_pro sanity
  cmd-desk_pro ui
  cmd-desk_pro health
  cmd-desk_pro logs [n]
  cmd-desk_pro serve [host] [port]

Env:
  REPO=/opt/trading
  BASE_URL=http://127.0.0.1:8010
USAGE
}

sub="${1:-}"
shift || true

cd "$REPO" 2>/dev/null || true

case "$sub" in
  sanity)
    bash "$REPO/scripts/sanity_desk_pro.sh"
    ;;
  ui)
    echo "$BASE_URL/desk/ui"
    ;;
  health)
    if command -v curl >/dev/null 2>&1; then
      curl -sS "$BASE_URL/desk/health" || true
      echo
    else
      echo "curl not found"
      exit 3
    fi
    ;;
  logs)
    n="${1:-200}"
    logdir="$REPO/tmp"
    if [[ -d "$logdir" ]]; then
      ls -1t "$logdir"/*.log 2>/dev/null | head -n 1 | xargs -r tail -n "$n"
    else
      echo "No $logdir directory"
    fi
    ;;
  serve)
    host="${1:-127.0.0.1}"
    port="${2:-8010}"
    # Assumes your repo has the FastAPI entrypoint already wired (as per previous sessions).
    # We keep this generic: if you have a make/runner, call it here.
    if [[ -f "$REPO/scripts/run_api.sh" ]]; then
      bash "$REPO/scripts/run_api.sh" "$host" "$port"
    else
      echo "No scripts/run_api.sh found. Start your API the usual way (uvicorn) then open: $BASE_URL/desk/ui"
      exit 4
    fi
    ;;
  ""|-h|--help|help)
    usage
    ;;
  *)
    echo "Unknown subcommand: $sub"
    usage
    exit 1
    ;;
esac
