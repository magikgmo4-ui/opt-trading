#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANONICAL_INSTALL="$BASE_DIR/../../../scripts/install_canonical_shortcuts.sh"

echo "INFO: reseau_ssh_step2 shortcut publication is retired."
echo "INFO: delegating to canonical reseau_ssh shortcut installer."
exec bash "$CANONICAL_INSTALL"
