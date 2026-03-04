#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "$ROOT/modules/deepseek_student/scripts/menu.sh" "$BIN/menu-deepseek_student"
sudo ln -sf "$ROOT/modules/deepseek_student/scripts/cmd.sh" "$BIN/cmd-deepseek_student"
sudo ln -sf "$ROOT/modules/deepseek_student/scripts/sanity_check.sh" "$BIN/sanity-deepseek_student"
echo "OK: installed shortcuts for deepseek_student"
ls -l "$BIN/menu-deepseek_student" "$BIN/cmd-deepseek_student" "$BIN/sanity-deepseek_student"
