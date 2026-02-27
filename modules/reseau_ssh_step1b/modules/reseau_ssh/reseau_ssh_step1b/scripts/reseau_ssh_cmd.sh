\
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cmd="${1:-help}"; shift || true

case "$cmd" in
  dry-run) "$ROOT_DIR/scripts/apply_linux.sh" ;;
  apply)   "$ROOT_DIR/scripts/apply_linux.sh" --apply ;;
  hostname) "$ROOT_DIR/scripts/apply_hostname_linux.sh" "$@" ;;
  sanity)  "$ROOT_DIR/scripts/sanity_check.sh" ;;
  show-hosts) sed -n '1,120p' "$ROOT_DIR/templates/hosts.block" ;;
  show-ssh)   sed -n '1,220p' "$ROOT_DIR/templates/ssh_config.linux" ;;
  help|*)
    cat <<EOF
cmd-reseau_ssh (Step 1b)
  dry-run
  apply
  hostname <admin-trading|db-layer|student>
  sanity
  show-hosts
  show-ssh
EOF
    ;;
esac
