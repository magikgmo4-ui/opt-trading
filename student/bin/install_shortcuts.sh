#!/usr/bin/env bash
set -euo pipefail

ROOT="/opt/trading/student"

sudo ln -sfn "$ROOT/scripts/deepseek_hub/deepseek_hub_menu.sh" /usr/local/bin/menu-deepseek_hub
sudo ln -sfn "$ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh" /usr/local/bin/cmd-deepseek_hub
sudo ln -sfn "$ROOT/scripts/deepseek_hub/sanity_check_deepseek_hub.sh" /usr/local/bin/sanity-deepseek_hub
sudo ln -sfn "$ROOT/scripts/deepseek_student/menu.sh" /usr/local/bin/menu-deepseek_student
sudo ln -sfn "$ROOT/scripts/deepseek_student/cmd.sh" /usr/local/bin/cmd-deepseek_student
sudo ln -sfn "$ROOT/scripts/deepseek_student/sanity_check.sh" /usr/local/bin/sanity-deepseek_student
sudo ln -sfn "$ROOT/scripts/student_menu.sh" /usr/local/bin/menu-student
sudo ln -sfn "$ROOT/scripts/student_cmd.sh" /usr/local/bin/cmd-student
sudo ln -sfn "$ROOT/scripts/student_sanity_check.sh" /usr/local/bin/sanity-student

echo "OK: canonical student shortcuts installed"
