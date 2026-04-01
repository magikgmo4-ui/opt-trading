#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CFG="$HOME/.openclaw/openclaw.json"
CFG_D="$HOME/.openclaw/config.d"

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh sanity
  cmd.sh status
  cmd.sh backup
  cmd.sh apply
  cmd.sh validate
  cmd.sh health
  cmd.sh probe
  cmd.sh rollback [backup_dir]
  cmd.sh paths
EOF
}

case "${1:-help}" in
  sanity)
    "$BASE/scripts/sanity.sh"
    ;;
  status)
    echo "Module: openclaw_config_modulaire"
    echo "Config: $CFG"
    echo "Config.d: $CFG_D"
    echo
    ls -lah "$HOME/.openclaw" || true
    echo
    ls -lah "$CFG_D" || true
    ;;
  backup)
    "$BASE/scripts/apply_safe.sh" >/dev/null
    echo "NOTE: apply_safe a déjà créé le backup le plus récent."
    ;;
  apply)
    "$BASE/scripts/apply_safe.sh"
    ;;
  validate)
    openclaw config validate
    ;;
  health)
    openclaw gateway health
    ;;
  probe)
    openclaw gateway probe
    ;;
  rollback)
    shift || true
    "$BASE/scripts/rollback.sh" "${1:-}"
    ;;
  paths)
    printf '%s\n' \
      "BASE=$BASE" \
      "CFG=$CFG" \
      "CFG_D=$CFG_D" \
      "APP=$BASE/app" \
      "DOCS=$BASE/docs"
    ;;
  *)
    help_msg
    exit 1
    ;;
esac
