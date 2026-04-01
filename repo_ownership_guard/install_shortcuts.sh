#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

sudo ln -sf "$ROOT_DIR/scripts/repo_ownership_guard_menu.sh"   /usr/local/bin/menu-repo_ownership_guard
sudo ln -sf "$ROOT_DIR/scripts/repo_ownership_guard_cmd.sh"    /usr/local/bin/cmd-repo_ownership_guard
sudo ln -sf "$ROOT_DIR/scripts/repo_ownership_guard_sanity.sh" /usr/local/bin/sanity-repo_ownership_guard

echo "OK: shortcuts installed: menu-repo_ownership_guard / cmd-repo_ownership_guard / sanity-repo_ownership_guard"
