#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/opt/trading}"
MAKE_DEFAULT="${MAKE_DEFAULT:-0}"   # set to 1 to point menu-deepseek to hub
ALSO_ALIAS_STUDENT="${ALSO_ALIAS_STUDENT:-0}" # set to 1 to alias menu-student/cmd-student/sanity-student to hub

echo "== deepseek_hub: install shortcuts =="
echo "ROOT: $ROOT"
echo "MAKE_DEFAULT=$MAKE_DEFAULT"
echo "ALSO_ALIAS_STUDENT=$ALSO_ALIAS_STUDENT"

sudo ln -sf "$ROOT/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh" /usr/local/bin/cmd-deepseek_hub
sudo ln -sf "$ROOT/modules/deepseek_hub/scripts/deepseek_hub_menu.sh" /usr/local/bin/menu-deepseek_hub
sudo ln -sf "$ROOT/modules/deepseek_hub/scripts/sanity_check_deepseek_hub.sh" /usr/local/bin/sanity-deepseek_hub

if [ "$MAKE_DEFAULT" = "1" ]; then
  sudo ln -sf "$ROOT/modules/deepseek_hub/scripts/deepseek_hub_menu.sh" /usr/local/bin/menu-deepseek
fi

if [ "$ALSO_ALIAS_STUDENT" = "1" ]; then
  sudo ln -sf "$ROOT/modules/deepseek_hub/scripts/deepseek_hub_menu.sh" /usr/local/bin/menu-student
  sudo ln -sf "$ROOT/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh"  /usr/local/bin/cmd-student
  sudo ln -sf "$ROOT/modules/deepseek_hub/scripts/sanity_check_deepseek_hub.sh" /usr/local/bin/sanity-student
fi

echo "OK: shortcuts installed"
