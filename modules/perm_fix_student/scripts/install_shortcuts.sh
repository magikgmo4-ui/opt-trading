#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/perm_fix_student/scripts/menu.sh" "$BIN/menu-perm_fix_student"
sudo ln -sf "$ROOT/modules/perm_fix_student/scripts/cmd.sh" "$BIN/cmd-perm_fix_student"
sudo ln -sf "$ROOT/modules/perm_fix_student/scripts/sanity_check.sh" "$BIN/sanity-perm_fix_student"
echo "OK: installed shortcuts for perm_fix_student"
ls -l "$BIN/menu-perm_fix_student" "$BIN/cmd-perm_fix_student" "$BIN/sanity-perm_fix_student"
