#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/repo_ownership_guard/scripts/menu.sh" "$BIN/menu-repo_ownership_guard"
sudo ln -sf "$ROOT/modules/repo_ownership_guard/scripts/cmd.sh" "$BIN/cmd-repo_ownership_guard"
sudo ln -sf "$ROOT/modules/repo_ownership_guard/scripts/sanity_check.sh" "$BIN/sanity-repo_ownership_guard"
echo "OK: installed shortcuts for repo_ownership_guard"
ls -l "$BIN/menu-repo_ownership_guard" "$BIN/cmd-repo_ownership_guard" "$BIN/sanity-repo_ownership_guard"
