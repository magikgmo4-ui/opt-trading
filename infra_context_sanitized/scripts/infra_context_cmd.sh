#!/usr/bin/env bash
set -euo pipefail

ROOT="${INFRA_CONTEXT_ROOT:-$HOME/infra-context}"

usage() {
  cat <<EOF
cmd-infra_context — commands for infra-context repo

Usage:
  cmd-infra_context sanity
  cmd-infra_context snap-linux <machine>
  cmd-infra_context zip
  cmd-infra_context grep-secrets

Machines:
  admin-trading | db-layer | student

EOF
}

machine_dir() {
  echo "$ROOT/machines/$1"
}

case "${1:-}" in
  sanity)
    bash "$ROOT/scripts/infra_context_sanity_check.sh" "$ROOT"
    ;;
  snap-linux)
    m="${2:-}"
    [[ -n "$m" ]] || { echo "Missing machine name"; usage; exit 2; }
    outdir="$(machine_dir "$m")/snapshot"
    bash "$ROOT/scripts/linux_snapshot_sanitized.sh" "$outdir"
    ;;
  zip)
    mkdir -p "$ROOT/exports"
    ts="$(date -Iseconds | tr ':' '-')"
    zipfile="$ROOT/exports/infra_context_sanitized_${ts}.zip"
    (cd "$ROOT" && zip -r "$zipfile" infra_context machines scripts README.md SECURITY_REDACTION_RULES.md .gitignore >/dev/null)
    echo "Wrote: $zipfile"
    ;;
  grep-secrets)
    grep -RniE "token|apikey|api_key|secret|password|bearer|webhook|ngrok|cloudflared|ssh-rsa|PRIVATE KEY" "$ROOT/machines" "$ROOT/scripts" "$ROOT/infra_context" 2>/dev/null || true
    ;;
  *)
    usage
    exit 2
    ;;
esac
