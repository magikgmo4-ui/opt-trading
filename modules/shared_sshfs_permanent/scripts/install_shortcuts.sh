#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/shared_sshfs_permanent/scripts/menu.sh" "$BIN/menu-shared_sshfs_permanent"
sudo ln -sf "$ROOT/modules/shared_sshfs_permanent/scripts/cmd.sh" "$BIN/cmd-shared_sshfs_permanent"
sudo ln -sf "$ROOT/modules/shared_sshfs_permanent/scripts/sanity_check.sh" "$BIN/sanity-shared_sshfs_permanent"
echo "OK: installed shortcuts for shared_sshfs_permanent"
ls -l "$BIN/menu-shared_sshfs_permanent" "$BIN/cmd-shared_sshfs_permanent" "$BIN/sanity-shared_sshfs_permanent"
