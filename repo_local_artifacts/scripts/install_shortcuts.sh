#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/repo_local_artifacts/scripts/menu.sh" "$BIN/menu-repo_local_artifacts"
sudo ln -sf "$ROOT/modules/repo_local_artifacts/scripts/cmd.sh" "$BIN/cmd-repo_local_artifacts"
sudo ln -sf "$ROOT/modules/repo_local_artifacts/scripts/sanity_check.sh" "$BIN/sanity-repo_local_artifacts"
echo "OK: installed shortcuts for repo_local_artifacts"
ls -l "$BIN/menu-repo_local_artifacts" "$BIN/cmd-repo_local_artifacts" "$BIN/sanity-repo_local_artifacts"
