#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd -P)"
CANONICAL_INSTALL="$ROOT_DIR/modules/reseau_ssh/scripts/install_canonical_shortcuts.sh"

# Keep this legacy entrypoint only as a thin delegator to the canonical installer.
if [ -x "$CANONICAL_INSTALL" ]; then
  echo "INFO: scripts/reseau_ssh/install_reseau_ssh.sh is deprecated."
  echo "INFO: delegating short-alias installation to canonical module reseau_ssh."
  exec bash "$CANONICAL_INSTALL"
fi

echo "ERROR: canonical installer missing: $CANONICAL_INSTALL" >&2
echo "ERROR: legacy fallback installation is retired." >&2
exit 2
