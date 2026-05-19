#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/repo_hygiene/scripts/menu.sh" "$BIN/menu-repo_hygiene"
sudo ln -sf "$ROOT/modules/repo_hygiene/scripts/cmd.sh" "$BIN/cmd-repo_hygiene"
sudo ln -sf "$ROOT/modules/repo_hygiene/scripts/sanity_check.sh" "$BIN/sanity-repo_hygiene"
echo "OK: installed shortcuts for repo_hygiene"
ls -l "$BIN/menu-repo_hygiene" "$BIN/cmd-repo_hygiene" "$BIN/sanity-repo_hygiene"
