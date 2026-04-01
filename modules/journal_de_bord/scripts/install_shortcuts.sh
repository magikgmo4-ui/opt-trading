#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/journal_de_bord/scripts/menu.sh" "$BIN/menu-journal_de_bord"
sudo ln -sf "$ROOT/modules/journal_de_bord/scripts/cmd.sh" "$BIN/cmd-journal_de_bord"
sudo ln -sf "$ROOT/modules/journal_de_bord/scripts/sanity_check.sh" "$BIN/sanity-journal_de_bord"
echo "OK: installed shortcuts for journal_de_bord"
ls -l "$BIN/menu-journal_de_bord" "$BIN/cmd-journal_de_bord" "$BIN/sanity-journal_de_bord"
