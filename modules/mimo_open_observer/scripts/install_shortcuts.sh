#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
MODULE_DIR="$(dirname "$SCRIPT_DIR")"

if [[ "${MIMO_OPEN_OBSERVER_INSTALL_LEGACY_SHORTCUTS:-0}" != "1" ]]; then
  cat >&2 <<'EOF'
MIMO Open Observer shortcuts are archived/legacy surfaces.
Installation is blocked by default.

If you explicitly need them for archival access:
  MIMO_OPEN_OBSERVER_INSTALL_LEGACY_SHORTCUTS=1 bash modules/mimo_open_observer/scripts/install_shortcuts.sh

See:
  modules/mimo_open_observer/LEGACY.md
EOF
  exit 2
fi

sudo ln -sfn "$MODULE_DIR/scripts/mimo_open_observer_cmd.sh" /usr/local/bin/cmd-mimo_open_observer
sudo ln -sfn "$MODULE_DIR/scripts/mimo_open_observer_menu.sh" /usr/local/bin/menu-mimo_open_observer
sudo ln -sfn "$MODULE_DIR/scripts/mimo_open_observer_sanity.sh" /usr/local/bin/sanity-mimo_open_observer

echo "OK legacy archival shortcuts installed"
