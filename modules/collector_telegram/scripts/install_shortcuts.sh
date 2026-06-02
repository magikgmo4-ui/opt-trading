#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
MODULE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)

install -m 0755 "$SCRIPT_DIR/cmd.sh" /usr/local/bin/cmd-collector_telegram
install -m 0755 "$SCRIPT_DIR/menu.sh" /usr/local/bin/menu-collector_telegram
install -m 0755 "$SCRIPT_DIR/sanity_check.sh" /usr/local/bin/sanity-collector_telegram
ln -sf "$SCRIPT_DIR/install_shortcuts.sh" /usr/local/bin/install-collector_telegram-shortcuts

printf 'Installed collector_telegram shortcuts from %s\n' "$MODULE_DIR"
