#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/scripts/ui_debug"

usage() {
  cat <<'EOF'
cmd-ui_debug — commandes

Usage:
  cmd-ui_debug sanity        # sanity check
  cmd-ui_debug diag          # diagnostic complet (crée /tmp/ui_diag_*.tgz)
  cmd-ui_debug ports         # affiche ports (ss -ltnp)
  cmd-ui_debug failed        # services systemd en échec
EOF
}

cmd="${1:-}"
case "$cmd" in
  sanity) exec bash "$BASE/sanity_ui_debug.sh" ;;
  diag) exec bash "$BASE/ui_diag.sh" ;;
  ports) ss -ltnp ;;
  failed) systemctl --failed ;;
  ""|-h|--help) usage ;;
  *) echo "Unknown: $cmd"; echo; usage; exit 2 ;;
esac
