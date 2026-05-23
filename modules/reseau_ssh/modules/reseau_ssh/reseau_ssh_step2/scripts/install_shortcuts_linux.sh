#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
REPO_ROOT="$(cd "$BASE_DIR/../../../../.." && pwd -P)"
CANONICAL_COMPAT_INSTALL="$REPO_ROOT/modules/reseau_ssh/scripts/install_shortcuts.sh"

echo "INFO: nested reseau_ssh_step2 installer is compatibility-only."
echo "INFO: delegating step2 alias publication to canonical module reseau_ssh."
exec bash "$CANONICAL_COMPAT_INSTALL"
