#!/usr/bin/env bash
set -euo pipefail
SOURCE_PATH="${BASH_SOURCE[0]}"
while [ -L "$SOURCE_PATH" ]; do
  SOURCE_DIR="$(cd "$(dirname "$SOURCE_PATH")" && pwd -P)"
  SOURCE_PATH="$(readlink "$SOURCE_PATH")"
  case "$SOURCE_PATH" in
    /*) ;;
    *) SOURCE_PATH="$SOURCE_DIR/$SOURCE_PATH" ;;
  esac
done
SCRIPTS_DIR="$(cd "$(dirname "$SOURCE_PATH")" && pwd -P)"

echo "INFO: reseau_ssh_step2 compat shortcuts are retired."
echo "INFO: installing canonical reseau_ssh shortcuts instead."
exec bash "$SCRIPTS_DIR/install_canonical_shortcuts.sh"
