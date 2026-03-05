#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/shared_files_sftp/scripts/menu.sh" "$BIN/menu-shared_files_sftp"
sudo ln -sf "$ROOT/modules/shared_files_sftp/scripts/cmd.sh" "$BIN/cmd-shared_files_sftp"
sudo ln -sf "$ROOT/modules/shared_files_sftp/scripts/sanity_check.sh" "$BIN/sanity-shared_files_sftp"
echo "OK: installed shortcuts for shared_files_sftp"
ls -l "$BIN/menu-shared_files_sftp" "$BIN/cmd-shared_files_sftp" "$BIN/sanity-shared_files_sftp"
