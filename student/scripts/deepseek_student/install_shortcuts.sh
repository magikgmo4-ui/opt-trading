#!/usr/bin/env bash
set -euo pipefail
ROOT="${ROOT:-/opt/trading/student}"
BIN="/usr/local/bin"
echo "NOTE: prefer /opt/trading/student/bin/install_shortcuts.sh as the canonical installer"
sudo ln -sf "$ROOT/scripts/deepseek_student/menu.sh" "$BIN/menu-deepseek_student"
sudo ln -sf "$ROOT/scripts/deepseek_student/cmd.sh" "$BIN/cmd-deepseek_student"
sudo ln -sf "$ROOT/scripts/deepseek_student/sanity_check.sh" "$BIN/sanity-deepseek_student"
echo "OK: installed shortcuts for deepseek_student"
ls -l "$BIN/menu-deepseek_student" "$BIN/cmd-deepseek_student" "$BIN/sanity-deepseek_student"
echo "NOTE: this installer is module-scoped; use /opt/trading/student/bin/install_shortcuts.sh for full student setup"
