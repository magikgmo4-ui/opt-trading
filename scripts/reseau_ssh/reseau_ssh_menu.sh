#!/usr/bin/env bash
set -euo pipefail

CANONICAL_MENU="/opt/trading/modules/reseau_ssh/scripts/menu.sh"

if [[ ! -x "$CANONICAL_MENU" ]]; then
  echo "ERROR: canonical reseau_ssh menu missing: $CANONICAL_MENU" >&2
  exit 2
fi

echo "INFO: legacy reseau_ssh menu shim delegating to canonical module." >&2
exec bash "$CANONICAL_MENU" "$@"
