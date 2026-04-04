#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

while true; do
  cat <<'EOF'
== DEV VALIDATION HUB ==
1) Sanity
2) Status
3) Pre-PR
4) Ensure venv
5) Install HTTP test deps
6) Run memory_bricks HTTP tests
7) trading_lab_v1 status
0) Exit
EOF
  read -rp "> " choice
  case "$choice" in
    1) bash "$CMD" sanity ;;
    2) bash "$CMD" status ;;
    3) bash "$CMD" pre-pr ;;
    4) read -rp "Venv name [.venv-dev-validation]: " vname; bash "$CMD" ensure-venv "${vname:-.venv-dev-validation}" ;;
    5) read -rp "Venv name [.venv-dev-validation]: " vname; bash "$CMD" install-http-test-deps "${vname:-.venv-dev-validation}" ;;
    6) read -rp "Venv name [.venv-dev-validation]: " vname; bash "$CMD" run-memory-bricks-http-tests "${vname:-.venv-dev-validation}" ;;
    7) bash "$CMD" trading-lab-status ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
  echo
done
