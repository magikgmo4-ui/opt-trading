#!/usr/bin/env bash
set -euo pipefail

ROOT="/opt/trading/student"

sudo ln -sfn "$ROOT/scripts/student_menu.sh" /usr/local/bin/menu-student
sudo ln -sfn "$ROOT/scripts/student_cmd.sh" /usr/local/bin/cmd-student
sudo ln -sfn "$ROOT/scripts/student_sanity_check.sh" /usr/local/bin/sanity-student

echo "OK: student shortcuts installed"
