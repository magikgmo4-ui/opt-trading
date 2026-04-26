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
ROOT="$(cd "$SCRIPTS_DIR/../../.." && pwd -P)"
BIN="/usr/local/bin"

sudo ln -sf "$ROOT/modules/reseau_ssh/scripts/menu.sh" "$BIN/menu-reseau_ssh"
sudo ln -sf "$ROOT/modules/reseau_ssh/scripts/cmd.sh" "$BIN/cmd-reseau_ssh"
sudo ln -sf "$ROOT/modules/reseau_ssh/scripts/sanity_check.sh" "$BIN/sanity-reseau_ssh"

echo "OK: installed canonical shortcuts for reseau_ssh"
ls -l "$BIN/menu-reseau_ssh" "$BIN/cmd-reseau_ssh" "$BIN/sanity-reseau_ssh"
