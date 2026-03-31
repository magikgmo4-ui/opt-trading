#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
MODULE_DIR="$(dirname "$SCRIPT_DIR")"

sudo ln -sfn "$MODULE_DIR/scripts/mimo_open_observer_cmd.sh" /usr/local/bin/cmd-mimo_open_observer
sudo ln -sfn "$MODULE_DIR/scripts/mimo_open_observer_menu.sh" /usr/local/bin/menu-mimo_open_observer
sudo ln -sfn "$MODULE_DIR/scripts/mimo_open_observer_sanity.sh" /usr/local/bin/sanity-mimo_open_observer

echo "OK shortcuts installed"
