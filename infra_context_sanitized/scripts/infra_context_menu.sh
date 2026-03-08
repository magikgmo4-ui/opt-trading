#!/usr/bin/env bash
set -euo pipefail

ROOT="${INFRA_CONTEXT_ROOT:-$HOME/infra-context}"

while true; do
  echo
  echo "=== Infra Context Menu ==="
  echo "1) Sanity check"
  echo "2) Snapshot Linux: admin-trading"
  echo "3) Snapshot Linux: db-layer"
  echo "4) Snapshot Linux: student"
  echo "5) Grep secrets (sanity redaction)"
  echo "6) Export ZIP (sanitized)"
  echo "q) Quit"
  read -r -p "> " choice

  case "$choice" in
    1) bash "$ROOT/scripts/infra_context_sanity_check.sh" "$ROOT" ;;
    2) bash "$ROOT/scripts/infra_context_cmd.sh" snap-linux admin-trading ;;
    3) bash "$ROOT/scripts/infra_context_cmd.sh" snap-linux db-layer ;;
    4) bash "$ROOT/scripts/infra_context_cmd.sh" snap-linux student ;;
    5) bash "$ROOT/scripts/infra_context_cmd.sh" grep-secrets ;;
    6) bash "$ROOT/scripts/infra_context_cmd.sh" zip ;;
    q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
