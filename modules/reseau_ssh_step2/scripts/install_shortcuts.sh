#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/reseau_ssh_step2/scripts/menu.sh" "$BIN/menu-reseau_ssh_step2"
sudo ln -sf "$ROOT/modules/reseau_ssh_step2/scripts/cmd.sh" "$BIN/cmd-reseau_ssh_step2"
sudo ln -sf "$ROOT/modules/reseau_ssh_step2/scripts/sanity_check.sh" "$BIN/sanity-reseau_ssh_step2"
echo "OK: installed shortcuts for reseau_ssh_step2"
ls -l "$BIN/menu-reseau_ssh_step2" "$BIN/cmd-reseau_ssh_step2" "$BIN/sanity-reseau_ssh_step2"
