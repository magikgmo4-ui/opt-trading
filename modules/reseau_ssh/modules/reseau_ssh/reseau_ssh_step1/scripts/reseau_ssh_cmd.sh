#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INV="$ROOT_DIR/hosts.yaml"
TPL="$ROOT_DIR/templates/ssh_config.template"

cmd="${1:-help}"; shift || true

case "$cmd" in
  show-inv)
    sed -n '1,220p' "$INV"
    ;;
  show-ssh-template)
    sed -n '1,260p' "$TPL"
    ;;
  quick-test)
    echo "Testing ssh to: admin-trading student msi win (if configured)"
    for h in admin-trading student msi win; do
      echo "--- $h ---"
      timeout 5 ssh -o BatchMode=yes -o ConnectTimeout=3 "$h" 'echo OK $(hostname) && exit 0' 2>/dev/null         && echo "OK $h" || echo "WARN $h (no key or not configured yet)"
    done
    ;;
  help|*)
    cat <<EOF
reseau_ssh_cmd.sh <command>

Commands:
  show-inv              Print hosts.yaml (inventory)
  show-ssh-template     Print ssh_config.template
  quick-test            Try non-interactive ssh to aliases (best-effort)

Step 1 is non-destructive: validate & prepare.
EOF
    ;;
esac
