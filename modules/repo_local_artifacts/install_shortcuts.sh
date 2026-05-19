#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

sudo ln -sf "$ROOT_DIR/scripts/repo_local_artifacts_menu.sh"   /usr/local/bin/menu-repo_local_artifacts
sudo ln -sf "$ROOT_DIR/scripts/repo_local_artifacts_cmd.sh"    /usr/local/bin/cmd-repo_local_artifacts
sudo ln -sf "$ROOT_DIR/scripts/repo_local_artifacts_sanity.sh" /usr/local/bin/sanity-repo_local_artifacts

echo "OK: shortcuts installed: menu-repo_local_artifacts / cmd-repo_local_artifacts / sanity-repo_local_artifacts"
