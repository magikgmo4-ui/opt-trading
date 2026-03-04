#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/reseau_ssh_step1b/scripts/menu.sh" "$BIN/menu-reseau_ssh_step1b"
sudo ln -sf "$ROOT/modules/reseau_ssh_step1b/scripts/cmd.sh" "$BIN/cmd-reseau_ssh_step1b"
sudo ln -sf "$ROOT/modules/reseau_ssh_step1b/scripts/sanity_check.sh" "$BIN/sanity-reseau_ssh_step1b"
echo "OK: installed shortcuts for reseau_ssh_step1b"
ls -l "$BIN/menu-reseau_ssh_step1b" "$BIN/cmd-reseau_ssh_step1b" "$BIN/sanity-reseau_ssh_step1b"
