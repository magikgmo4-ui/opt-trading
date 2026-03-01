#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/scripts/ui_debug"

while true; do
  echo "=== UI Debug Menu ==="
  echo "1) Sanity check"
  echo "2) Diagnostic complet (pack tgz)"
  echo "3) Ports ouverts (ss -ltnp)"
  echo "4) Services en échec (systemctl --failed)"
  echo "q) Quit"
  echo
  read -r -p "> " choice
  case "$choice" in
    1) bash "$BASE/sanity_ui_debug.sh" ;;
    2) bash "$BASE/ui_diag.sh" ;;
    3) ss -ltnp ;;
    4) systemctl --failed ;;
    q|Q) exit 0 ;;
    *) echo "Choix invalide." ;;
  esac
  echo
done
