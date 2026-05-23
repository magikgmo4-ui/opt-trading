#!/usr/bin/env bash
set -euo pipefail

CANONICAL_SANITY="/opt/trading/modules/reseau_ssh/scripts/sanity_check.sh"

if [[ ! -x "$CANONICAL_SANITY" ]]; then
  echo "ERROR: canonical reseau_ssh sanity missing: $CANONICAL_SANITY" >&2
  exit 2
fi

echo "INFO: legacy reseau_ssh sanity shim delegating to canonical module." >&2
exec bash "$CANONICAL_SANITY" "$@"
