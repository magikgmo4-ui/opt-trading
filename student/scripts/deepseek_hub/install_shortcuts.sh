#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/opt/trading/student}"
MAKE_DEFAULT="${MAKE_DEFAULT:-0}"   # set to 1 to point menu-deepseek to hub
ALSO_ALIAS_STUDENT="${ALSO_ALIAS_STUDENT:-0}" # set to 1 to alias menu-student/cmd-student/sanity-student to hub

echo "== deepseek_hub: install shortcuts =="
echo "ROOT: $ROOT"
echo "MAKE_DEFAULT=$MAKE_DEFAULT"
echo "ALSO_ALIAS_STUDENT=$ALSO_ALIAS_STUDENT"
echo "NOTE: prefer /opt/trading/student/bin/install_shortcuts.sh as the canonical installer"

sudo ln -sf "$ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh" /usr/local/bin/cmd-deepseek_hub
sudo ln -sf "$ROOT/scripts/deepseek_hub/deepseek_hub_menu.sh" /usr/local/bin/menu-deepseek_hub
sudo ln -sf "$ROOT/scripts/deepseek_hub/sanity_check_deepseek_hub.sh" /usr/local/bin/sanity-deepseek_hub

if [ "$MAKE_DEFAULT" = "1" ]; then
  sudo ln -sf "$ROOT/scripts/deepseek_hub/deepseek_hub_menu.sh" /usr/local/bin/menu-deepseek
fi

if [ "$ALSO_ALIAS_STUDENT" = "1" ]; then
  sudo ln -sf "$ROOT/scripts/student_menu.sh" /usr/local/bin/menu-student
  sudo ln -sf "$ROOT/scripts/student_cmd.sh"  /usr/local/bin/cmd-student
  sudo ln -sf "$ROOT/scripts/student_sanity_check.sh" /usr/local/bin/sanity-student
fi

echo "OK: deepseek_hub shortcuts installed from canonical student root"
echo "NOTE: this installer is module-scoped; use /opt/trading/student/bin/install_shortcuts.sh for full student setup"
