#!/usr/bin/env bash
set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="/usr/local/bin"

sudo ln -sf "${MODULE_DIR}/scripts/cmd.sh" "${BIN_DIR}/cmd-memory_bricks"
sudo ln -sf "${MODULE_DIR}/scripts/menu.sh" "${BIN_DIR}/menu-memory_bricks"
sudo ln -sf "${MODULE_DIR}/scripts/sanity_check.sh" "${BIN_DIR}/sanity-memory_bricks"

echo "Installed shortcuts:"
echo "- ${BIN_DIR}/cmd-memory_bricks"
echo "- ${BIN_DIR}/menu-memory_bricks"
echo "- ${BIN_DIR}/sanity-memory_bricks"
