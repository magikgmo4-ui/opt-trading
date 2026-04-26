#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/reseau_ssh/scripts/menu.sh" "$BIN/menu-reseau_ssh_step2"
sudo ln -sf "$ROOT/modules/reseau_ssh/scripts/cmd.sh" "$BIN/cmd-reseau_ssh_step2"
sudo ln -sf "$ROOT/modules/reseau_ssh/scripts/sanity_check.sh" "$BIN/sanity-reseau_ssh_step2"
echo "OK: installed compat shortcuts for reseau_ssh_step2 from canonical module reseau_ssh"
ls -l "$BIN/menu-reseau_ssh_step2" "$BIN/cmd-reseau_ssh_step2" "$BIN/sanity-reseau_ssh_step2"
